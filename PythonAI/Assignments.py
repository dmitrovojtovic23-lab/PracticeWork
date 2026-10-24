import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def task_1():
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    rng = np.random.default_rng(42)
    users = rng.integers(120, 260, size=30)
    sessions = users + rng.integers(40, 120, size=30)
    revenue = (sessions * rng.uniform(1.2, 2.8, size=30) + users * rng.uniform(0.5, 1.9, size=30)).round(2)
    data = pd.DataFrame({
        "date": dates,
        "users": users,
        "sessions": sessions,
        "revenue": revenue,
    })
    print("Task 1")
    print(data.head(10).to_string(index=False))
    corr = data[["users", "sessions", "revenue"]].corr()
    print("\nCorrelation matrix")
    print(corr.round(4).to_string())
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].scatter(data["users"], data["sessions"], alpha=0.7)
    axes[0, 0].set_title("users - sessions")
    axes[0, 0].set_xlabel("users")
    axes[0, 0].set_ylabel("sessions")
    axes[0, 1].scatter(data["users"], data["revenue"], alpha=0.7)
    axes[0, 1].set_title("users - revenue")
    axes[0, 1].set_xlabel("users")
    axes[0, 1].set_ylabel("revenue")
    axes[1, 0].scatter(data["sessions"], data["revenue"], alpha=0.7)
    axes[1, 0].set_title("sessions - revenue")
    axes[1, 0].set_xlabel("sessions")
    axes[1, 0].set_ylabel("revenue")
    axes[1, 1].plot(data["date"], data["revenue"], marker="o", linewidth=2)
    axes[1, 1].set_title("revenue by date")
    axes[1, 1].set_xlabel("date")
    axes[1, 1].set_ylabel("revenue")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig("task1.png")
    plt.close(fig)


def task_2():
    rng = np.random.default_rng(5)
    n = 100
    group_a = np.repeat("A", n)
    group_b = np.repeat("B", n)
    group = np.concatenate([group_a, group_b])
    converted = np.concatenate([
        rng.binomial(1, 0.12, size=n),
        rng.binomial(1, 0.16, size=n),
    ])
    data = pd.DataFrame({"group": group, "converted": converted})
    summary = data.groupby("group")["converted"].agg(["mean", "count"])
    summary = summary.rename(columns={"mean": "conversion_rate", "count": "observations"})
    conversion_a = summary.loc["A", "conversion_rate"]
    conversion_b = summary.loc["B", "conversion_rate"]
    difference = conversion_b - conversion_a
    relative_change = difference / conversion_a if conversion_a else 0.0
    z = 1.96
    ci_a = np.array([conversion_a - z * np.sqrt(conversion_a * (1 - conversion_a) / n), conversion_a + z * np.sqrt(conversion_a * (1 - conversion_a) / n)])
    ci_b = np.array([conversion_b - z * np.sqrt(conversion_b * (1 - conversion_b) / n), conversion_b + z * np.sqrt(conversion_b * (1 - conversion_b) / n)])
    print("\nTask 2")
    print(summary.round(4).to_string())
    print(f"Absolute difference: {difference:.4f}")
    print(f"Relative change: {relative_change:.2%}")
    print(f"95% CI A: {ci_a.round(4).tolist()}")
    print(f"95% CI B: {ci_b.round(4).tolist()}")
    fig, ax = plt.subplots(figsize=(8, 6))
    groups = ["A", "B"]
    rates = [conversion_a, conversion_b]
    errors = [
        z * np.sqrt(conversion_a * (1 - conversion_a) / n),
        z * np.sqrt(conversion_b * (1 - conversion_b) / n),
    ]
    ax.bar(groups, rates, yerr=errors, capsize=6, color=["steelblue", "darkorange"])
    ax.set_title("Conversion by group")
    ax.set_ylabel("conversion rate")
    ax.set_ylim(0, max(rates) + 0.1)
    for i, value in enumerate(rates):
        ax.text(i, value + 0.01, f"{value:.2%}", ha="center", va="bottom")
    plt.savefig("task2.png")
    plt.close(fig)


def task_3():
    rng = np.random.default_rng(13)
    population = rng.lognormal(mean=0.0, sigma=1.5, size=5_000_000)
    sample_size = 1000
    samples = 500
    sample_means = np.empty(samples)
    for i in range(samples):
        sample = rng.choice(population, size=sample_size, replace=False)
        sample_means[i] = sample.mean()
    mean_value = sample_means.mean()
    std_value = sample_means.std(ddof=1)
    x = np.linspace(sample_means.min(), sample_means.max(), 200)
    normal_pdf = (1 / (std_value * np.sqrt(2 * np.pi))) * np.exp(-((x - mean_value) ** 2) / (2 * std_value ** 2))
    print("\nTask 3")
    print(f"Population mean: {population.mean():.4f}")
    print(f"Population std: {population.std(ddof=1):.4f}")
    print(f"Mean of sample means: {mean_value:.4f}")
    print(f"Std of sample means: {std_value:.4f}")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(sample_means, bins=40, density=True, alpha=0.7, color="seagreen")
    ax.plot(x, normal_pdf, color="darkred", linewidth=2)
    ax.set_title("Distribution of sample means")
    ax.set_xlabel("sample mean")
    ax.set_ylabel("density")
    plt.savefig("task3.png")
    plt.close(fig)


def task_4():
    dates = pd.date_range("2024-01-01", periods=90, freq="D")
    t = np.arange(90)
    seasonal = 18 * np.sin(2 * np.pi * t / 30)
    trend = 120 + 0.8 * t
    noise = np.random.default_rng(21).normal(0, 25, size=90)
    sales = trend + seasonal + noise
    data = pd.DataFrame({"date": dates, "sales": sales.round(2)})
    data["rolling_mean_7"] = data["sales"].rolling(window=7, min_periods=1).mean()
    data["rolling_std_7"] = data["sales"].rolling(window=7, min_periods=1).std()
    print("\nTask 4")
    print(data.head(10).to_string(index=False))
    fig, axes = plt.subplots(2, 1, figsize=(12, 9))
    axes[0].plot(data["date"], data["sales"], label="sales", linewidth=1.5)
    axes[0].plot(data["date"], data["rolling_mean_7"], label="rolling mean 7", linewidth=2, color="darkorange")
    axes[0].set_title("Sales and rolling mean")
    axes[0].set_ylabel("sales")
    axes[0].legend()
    axes[1].plot(data["date"], data["rolling_std_7"], color="forestgreen", linewidth=2)
    axes[1].set_title("Rolling std 7")
    axes[1].set_ylabel("std")
    axes[1].set_xlabel("date")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig("task4.png")
    plt.close(fig)


def main():
    task_1()
    task_2()
    task_3()
    task_4()


main()
