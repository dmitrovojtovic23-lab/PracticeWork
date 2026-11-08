import pandas as pd
from pathlib import Path


def task_1():
    books = pd.DataFrame(
        {
            "Назва": ["Python для дітей", "Глибокі знання", "Мистецтво коду", "Чистий Python"],
            "Автор": ["Аліна Коваль", "Олексій Сидоренко", "Марина Лисенко", "Іван Петров"],
            "Рік видання": [2018, 2015, 2020, 2014],
            "Ціна": [320, 280, 410, 260],
        }
    )
    print("Завдання 1")
    print(books)
    print("Середня ціна:", books["Ціна"].mean())
    print("Книги, видані після 2015 року:")
    print(books[books["Рік видання"] > 2015])
    print("Відсортовано за ціною в порядку зростання:")
    print(books.sort_values("Ціна").reset_index(drop=True))
    print()


def task_2():
    orders = pd.DataFrame(
        {
            "Номер замовлення": [1001, 1002, 1003, 1004, 1005, 1006],
            "Клієнт": ["Іван", "Марина", "Іван", "Олег", "Марина", "Анна"],
            "Дата": ["2024-01-05", "2024-01-07", "2024-01-10", "2024-01-12", "2024-01-15", "2024-01-18"],
            "Сума": [1200, 850, 1500, 640, 930, 2100],
        }
    )
    path = Path(__file__).with_name("orders.csv")
    orders.to_csv(path, index=False)
    orders_df = pd.read_csv(path)
    print("Завдання 2")
    print("Перші 5 рядків:")
    print(orders_df.head())
    print("Кількість замовлень на клієнта:")
    print(orders_df["Клієнт"].value_counts())
    print("Максимальна сума замовлення:", orders_df["Сума"].max())
    print("Мінімальна сума замовлення:", orders_df["Сума"].min())
    print("Загальна сума замовлень:", orders_df["Сума"].sum())
    print()


def task_3():
    products = pd.DataFrame(
        {
            "Продукт": ["Яблука", "Гречка", "Йогурт", "Курятина", "Сир", "Овес"],
            "Категорія": ["Фрукти", "Крупи", "Молочні", "М'ясо", "Молочні", "Крупи"],
            "Калорійність": [52, 340, 88, 195, 250, 366],
            "Білки": [0.3, 12.0, 8.0, 31.0, 22.0, 11.0],
        }
    )
    print("Завдання 3")
    print(products)
    print("Продукти з калорійністю більше 300:")
    print(products[products["Калорійність"] > 300])
    print("Середня кількість білків за категоріями:")
    print(products.groupby("Категорія", as_index=False)["Білки"].mean())
    print("Відсортовано за калорійністю за спаданням:")
    print(products.sort_values("Калорійність", ascending=False).reset_index(drop=True))
    print()


def task_4():
    employees = pd.DataFrame(
        {
            "Ім'я": ["Олена", "Максим", "Ірина", "Олександр", "Катерина", "Дмитро"],
            "Проект": ["A", "B", "A", "C", "B", "A"],
            "Години": [120, 75, 100, 80, 90, 140],
        }
    )
    print("Завдання 4")
    print(employees)
    print("Загальна кількість годин за проектами:")
    print(employees.groupby("Проект", as_index=False)["Години"].sum())
    print("Загальна кількість годин на співробітника:")
    print(employees.groupby("Ім'я", as_index=False)["Години"].sum())
    top_employee = employees.groupby("Ім'я")["Години"].sum().idxmax()
    print("Співробітник з найбільшою кількістю годин:")
    print(pd.DataFrame({"Ім'я": [top_employee], "Години": [employees.groupby("Ім'я")["Години"].sum().max()]}))
    print()


def task_5():
    sales = pd.DataFrame(
        {
            "Фільм": ["Інтерстеллар", "Інтерстеллар", "Країна", "Країна", "Дюна", "Дюна"],
            "Місто": ["Київ", "Львів", "Київ", "Одеса", "Львів", "Київ"],
            "Продані квитки": [230, 180, 160, 140, 210, 250],
        }
    )
    print("Завдання 5")
    print(sales)
    print("Загальна кількість проданих квитків за фільмом:")
    print(sales.groupby("Фільм", as_index=False)["Продані квитки"].sum())
    print("Загальна кількість проданих квитків за містом:")
    print(sales.groupby("Місто", as_index=False)["Продані квитки"].sum())
    best_movie = sales.groupby("Фільм")["Продані квитки"].sum().idxmax()
    print("Фільм із найбільшою кількістю продажів:")
    print(pd.DataFrame({"Фільм": [best_movie], "Продані квитки": [sales.groupby("Фільм")["Продані квитки"].sum().max()]}))
    print()


def task_6():
    customers = pd.DataFrame(
        {
            "ID": [1, 2, 3, 4],
            "Ім'я": ["Андрій", "Людмила", "Олег", "Марія"],
            "Місто": ["Київ", "Львів", "Одеса", "Київ"],
        }
    )
    orders = pd.DataFrame(
        {
            "ID клієнта": [1, 2, 1, 3, 4, 2],
            "Замовлення": ["Книга", "Ноутбук", "Рюкзак", "Навушники", "Монітор", "Планшет"],
            "Вартість": [250, 1200, 320, 450, 780, 650],
        }
    )
    merged = customers.merge(orders, left_on="ID", right_on="ID клієнта", how="inner")
    print("Завдання 6")
    print(merged)
    print("Загальна вартість замовлень за кожним клієнтом:")
    print(merged.groupby(["ID", "Ім'я", "Місто"], as_index=False)["Вартість"].sum())
    print()


task_1()
task_2()
task_3()
task_4()
task_5()
task_6()

