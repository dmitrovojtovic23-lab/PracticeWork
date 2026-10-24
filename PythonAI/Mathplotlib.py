import matplotlib.pyplot as plt
import numpy as np

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
plan = [120, 150, 170, 160, 200, 240]
fact = [110, 140, 165, 175, 190, 230]
plt.figure(figsize=(8, 5))
plt.plot(months, plan, marker="o", linewidth=2, label="План")
plt.plot(months, fact, marker="o", linewidth=2, label="Факт")
plt.title("План і факт")
plt.xlabel("Місяці")
plt.ylabel("Значення")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

values = np.random.normal(100, 15, 200)
plt.figure(figsize=(8, 5))
plt.hist(values, bins=20, color="#4c78a8", edgecolor="black")
plt.axvline(values.mean(), color="red", linestyle="--", linewidth=2, label="Середнє")
plt.title("Розподіл значень")
plt.xlabel("Значення")
plt.ylabel("Кількість")
plt.legend()
plt.tight_layout()
plt.show()

scores = {
    "Група A": [80, 90, 75, 88, 92, 78, 85],
    "Група B": [70, 82, 78, 68, 85, 80, 76],
    "Група C": [90, 95, 88, 84, 92, 89, 91],
}
plt.figure(figsize=(8, 5))
plt.boxplot(scores.values(), labels=scores.keys(), patch_artist=True)
plt.title("Результати іспитів")
plt.ylabel("Оцінки")
plt.tight_layout()
plt.show()

days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
temperature = [18, 21, 23, 22, 20, 19, 17]
humidity = [70, 65, 60, 62, 68, 74, 76]
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(days, temperature, color="tab:red", marker="o", linewidth=2, label="Температура")
ax1.set_xlabel("Дні")
ax1.set_ylabel("Температура, °C")
ax1.tick_params(axis="y", labelcolor="tab:red")
ax2 = ax1.twinx()
ax2.plot(days, humidity, color="tab:blue", marker="s", linewidth=2, label="Вологість")
ax2.set_ylabel("Вологість, %")
ax2.tick_params(axis="y", labelcolor="tab:blue")
fig.tight_layout()
plt.title("Температура і вологість")
plt.show()

hours = np.arange(24)
load = [20, 25, 22, 18, 17, 19, 28, 34, 42, 48, 52, 60, 58, 54, 50, 46, 44, 40, 38, 35, 30, 26, 22, 18]
plt.figure(figsize=(10, 5))
plt.plot(hours, load, color="tab:blue", linewidth=2)
plt.fill_between(hours, load, 0, color="tab:blue", alpha=0.2)
plt.title("Навантаження сервера")
plt.xlabel("Година")
plt.ylabel("Завантаження")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()

metrics = ["Конверсія", "Утримання", "Середній чек", "Кількість замовлень"]
values = [4.2, 62, 480, 140]
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, metric, value in zip(axes.flat, metrics, values):
    ax.bar([metric], [value], color="#4c78a8")
    ax.set_title(metric)
    ax.set_ylabel("Значення")
    ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
plt.show()
