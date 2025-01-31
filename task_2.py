# Реалізуйте двійковий пошук для відсортованого масиву з дробовими числами. Написана функція для двійкового пошуку повинна повертати кортеж, де першим елементом є кількість ітерацій, потрібних для знаходження елемента. Другим елементом має бути "верхня межа" — це найменший елемент, який є більшим або рівним заданому значенню.

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] >= x:
            upper_bound = arr[mid]
            high = mid - 1

    # Якщо upper_bound не знайдено в циклі, перевіряємо чи є більші елементи
    if upper_bound is None and low < len(arr):
        upper_bound = arr[low]

    return (iterations, upper_bound)


# Тестування функції
arr = [1.5, 2.3, 4.7, 6.1, 8.9, 10.2]
x = 4.5
result = binary_search(arr, x)
print(f"Кількість ітерацій: {result[0]}")
print(f"Верхня межа: {result[1]}")
