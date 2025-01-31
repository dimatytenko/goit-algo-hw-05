# Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів(стаття 1, стаття 2).
# Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті,
# та іншого — вигаданого(вибір підрядків за вашим бажанням). На основі отриманих даних визначте найшвидший алгоритм для кожного тексту окремо та в цілому.

from timeit import default_timer as timer


def build_bad_char_table(pattern):
    table = {}
    pattern_length = len(pattern)
    for i in range(pattern_length - 1):
        table[pattern[i]] = pattern_length - 1 - i
    return table


def boyer_moore(text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)
    if pattern_length > text_length:
        return -1

    # Створюємо таблицю зміщень для символів
    bad_char = build_bad_char_table(pattern)

    shift = 0
    while shift <= text_length - pattern_length:
        mismatch = False
        for i in range(pattern_length - 1, -1, -1):
            if pattern[i] != text[shift + i]:
                mismatch = True
                break

        if not mismatch:
            return shift

        # Зміщення
        if shift + pattern_length < text_length:
            char = text[shift + pattern_length - 1]
            shift += bad_char.get(char, pattern_length)
        else:
            return -1
    return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    if not pattern or not text:
        return -1

    lps = compute_lps(pattern)

    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return i - j

        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def rabin_karp(text, pattern):
    if not pattern or not text:
        return -1

    # Використовуємо просте число як основу
    d = 256
    q = 101

    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length > text_length:
        return -1

    # Обчислюємо хеш першого вікна тексту та патерну
    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(pattern_length - 1):
        h = (h * d) % q

    for i in range(pattern_length):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q

    # Проходимо по тексту
    for i in range(text_length - pattern_length + 1):
        if pattern_hash == text_hash:
            # Перевіряємо символи
            match = True
            for j in range(pattern_length):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return i

        if i < text_length - pattern_length:
            text_hash = (
                d * (text_hash - ord(text[i]) * h) + ord(text[i + pattern_length])) % q
            if text_hash < 0:
                text_hash += q

    return -1


def test_algorithm(algorithm, text, pattern, num_runs=100):
    start = timer()
    for _ in range(num_runs):
        algorithm(text, pattern)
    end = timer()
    return (end - start) / num_runs


def main():
    # Зчитуємо тексти з файлів
    with open('article1.txt', 'r', encoding='utf-8') as f:
        text1 = f.read()
    with open('article2.txt', 'r', encoding='utf-8') as f:
        text2 = f.read()

    # Підрядки для пошуку
    existing_pattern = "алгоритми"  # існуючий підрядок
    non_existing_pattern = "xyz123"  # неіснуючий підрядок

    algorithms = [
        ("Boyer-Moore", boyer_moore),
        ("KMP", kmp_search),
        ("Rabin-Karp", rabin_karp)
    ]

    # Тестування на першому тексті
    print("\nТестування на першому тексті:")
    print("\nІснуючий підрядок:", existing_pattern)
    for name, algo in algorithms:
        time = test_algorithm(algo, text1, existing_pattern)
        print(f"{name}: {time:.6f} секунд")

    print("\nНеіснуючий підрядок:", non_existing_pattern)
    for name, algo in algorithms:
        time = test_algorithm(algo, text1, non_existing_pattern)
        print(f"{name}: {time:.6f} секунд")

    # Тестування на другому тексті
    print("\nТестування на другому тексті:")
    print("\nІснуючий підрядок:", existing_pattern)
    for name, algo in algorithms:
        time = test_algorithm(algo, text2, existing_pattern)
        print(f"{name}: {time:.6f} секунд")

    print("\nНеіснуючий підрядок:", non_existing_pattern)
    for name, algo in algorithms:
        time = test_algorithm(algo, text2, non_existing_pattern)
        print(f"{name}: {time:.6f} секунд")


if __name__ == "__main__":
    main()
