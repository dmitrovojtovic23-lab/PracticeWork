from collections import Counter


def print_table(title, rows, columns):
    widths = [len(str(column)) for column in columns]
    for row in rows:
        widths = [max(widths[i], len(str(row[i]))) for i in range(len(columns))]
    header = " | ".join(str(columns[i]).ljust(widths[i]) for i in range(len(columns)))
    separator = "-+-".join("-" * widths[i] for i in range(len(columns)))
    print(title)
    print(header)
    print(separator)
    for row in rows:
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(columns))))
    print()


temperatures = [2, 5, 4, 6, 7, 3, 1]
average_temp = sum(temperatures) / len(temperatures)
min_temp = min(temperatures)
max_temp = max(temperatures)
range_temp = max_temp - min_temp
print_table(
    "Завдання 1",
    [
        ["Середнє значення", average_temp],
        ["Мінімальне значення", min_temp],
        ["Максимальне значення", max_temp],
        ["Різниця max - min", range_temp],
    ],
    ["Показник", "Значення"],
)

expenses = [1200, 1500, 800, 600, 1000, 400, 900]
total_expenses = sum(expenses)
average_expenses = total_expenses / len(expenses)
min_expenses = min(expenses)
max_expenses = max(expenses)
count_over_1000 = sum(1 for value in expenses if value > 1000)
print_table(
    "Завдання 2",
    [
        ["Загальна сума витрат", total_expenses],
        ["Середнє значення", average_expenses],
        ["Мінімальна витрата", min_expenses],
        ["Максимальна витрата", max_expenses],
        ["Кількість днів > 1000", count_over_1000],
    ],
    ["Показник", "Значення"],
)

votes = ["apple", "banana", "apple", "orange", "banana", "apple", "apple", "apple", "orange"]
fruit_counts = Counter(votes)
leader = max(fruit_counts, key=fruit_counts.get)
print_table(
    "Завдання 3",
    [[fruit, count] for fruit, count in sorted(fruit_counts.items())],
    ["Фрукт", "Кількість"],
)
print("Лідер:", leader)
print_table(
    "Топ-3",
    [[fruit, count] for fruit, count in fruit_counts.most_common(3)],
    ["Фрукт", "Кількість"],
)

math = [80, 92, 75, 60, 88]
physics = [70, 65, 90, 85, 78]
english = [95, 100, 85, 90, 87]
subjects = {
    "math": math,
    "physics": physics,
    "english": english,
}
subject_results = {}
for subject, marks in subjects.items():
    subject_results[subject] = {
        "середній бал": sum(marks) / len(marks),
        "мінімальний бал": min(marks),
        "максимальний бал": max(marks),
    }

best_subject = max(subject_results, key=lambda subject: subject_results[subject]["середній бал"])
print_table(
    "Завдання 4",
    [
        [subject, subject_results[subject]["середній бал"], subject_results[subject]["мінімальний бал"], subject_results[subject]["максимальний бал"]]
        for subject in subject_results
    ],
    ["Предмет", "Середній бал", "Мінімальний бал", "Максимальний бал"],
)
print("Предмет з найвищим середнім результатом:", best_subject)
