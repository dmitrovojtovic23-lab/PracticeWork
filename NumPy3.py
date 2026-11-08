import numpy as np

print("Завдання 1")
size = int(input("Введіть кількість елементів масиву: "))
low = int(input("Введіть нижню межу: "))
high = int(input("Введіть верхню межу: "))
if low > high:
    low, high = high, low
arr1 = np.random.randint(low, high + 1, size)
print("Масив:", arr1)
threshold = int(input("Введіть порогове значення: "))
print("Кількість елементів, що перевищують порогове значення:", np.count_nonzero(arr1 > threshold))
print("Максимальне значення:", arr1.max())
print("Індекс максимального значення:", np.argmax(arr1))
print("Масив після сортування:", np.sort(arr1))
print()

print("Завдання 2")
size = int(input("Введіть розмір квадратної матриці: "))
low = int(input("Введіть нижню межу: "))
high = int(input("Введіть верхню межу: "))
if low > high:
    low, high = high, low
arr2 = np.random.randint(low, high + 1, (size, size))
print("Матриця:")
print(arr2)
print("Головна діагональ:", np.diag(arr2))
print("Сума елементів головної діагоналі:", np.trace(arr2))
arr2_mod = arr2.copy()
arr2_mod[np.triu_indices(size, k=1)] = 0
print("Матриця після обнулення елементів вище головної діагоналі:")
print(arr2_mod)
print()

print("Завдання 3")
start = int(input("Введіть початок діапазону: "))
end = int(input("Введіть кінець діапазону: "))
if start <= end:
    seq3 = np.arange(start, end + 1)
else:
    seq3 = np.arange(start, end - 1, -1)
if len(seq3) != 25:
    seq3 = np.linspace(start, end, 25, dtype=int)
mat3 = seq3.reshape(5, 5)
print("Матриця:")
print(mat3)
print("Сума елементів у кожному рядку:", mat3.sum(axis=1))
print("Сума елементів у кожному стовпці:", mat3.sum(axis=0))
print("Максимальне значення в матриці:", mat3.max())
print()

print("Завдання 4")
low = int(input("Введіть нижню межу діапазону: "))
high = int(input("Введіть верхню межу діапазону: "))
if low > high:
    low, high = high, low
arr4 = np.random.randint(low, high + 1, 15)
print("Масив:", arr4)
negative = arr4[arr4 < 0]
print("Від’ємні елементи:", negative)
arr4_mod = arr4.copy()
arr4_mod[arr4_mod < 0] = 0
print("Масив із заміненими від’ємними елементами:", arr4_mod)
print("Кількість нульових елементів:", np.count_nonzero(arr4_mod == 0))
print()

print("Завдання 5")
length = int(input("Введіть довжину масивів: "))
arr5_1 = np.random.randint(0, 11, length)
arr5_2 = np.random.randint(10, 21, length)
print("Перший масив:", arr5_1)
print("Другий масив:", arr5_2)
arr5_total = np.concatenate((arr5_1, arr5_2))
print("Об’єднаний масив:", arr5_total)
print("Поелементне додавання:", arr5_1 + arr5_2)
print()

print("Завдання 6")
rows = int(input("Введіть кількість рядків вихідної матриці: "))
cols = int(input("Введіть кількість стовпців вихідної матриці: "))
arr6 = np.arange(1, rows * cols + 1).reshape(rows, cols)
print("Вихідна матриця:")
print(arr6)
while True:
    new_rows = int(input("Введіть кількість рядків нової матриці: "))
    new_cols = int(input("Введіть кількість стовпців нової матриці: "))
    if new_rows * new_cols == arr6.size:
        break
    print("Неможливо змінити форму матриці. Сума нових розмірів має дорівнювати кількості елементів:", arr6.size)
arr6_new = arr6.reshape(new_rows, new_cols)
print("Нова матриця:")
print(arr6_new)
print("Мінімальні значення в кожному рядку:", arr6_new.min(axis=1))
print("Максимальні значення в кожному рядку:", arr6_new.max(axis=1))
print("Загальна сума всіх елементів:", arr6_new.sum())
