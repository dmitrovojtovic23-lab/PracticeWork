import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler


wine = load_wine()
data = pd.DataFrame(wine.data, columns=wine.feature_names)

print(data.head())
print(f"Розміри матриці ознак: {data.shape}")

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)

svd = TruncatedSVD(n_components=2, random_state=42)
svd_result = svd.fit_transform(scaled_data)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

fig, (svd_ax, pca_ax) = plt.subplots(1, 2, figsize=(12, 5))

for target in sorted(set(wine.target)):
    svd_mask = wine.target == target
    svd_ax.scatter(
        svd_result[svd_mask, 0],
        svd_result[svd_mask, 1],
        label=wine.target_names[target],
    )

svd_ax.set_xlabel("SVD Component 1")
svd_ax.set_ylabel("SVD Component 2")
svd_ax.set_title("SVD Projection")
svd_ax.legend()

for target in sorted(set(wine.target)):
    pca_mask = wine.target == target
    pca_ax.scatter(
        pca_result[pca_mask, 0],
        pca_result[pca_mask, 1],
        label=wine.target_names[target],
    )

pca_ax.set_xlabel("PCA Component 1")
pca_ax.set_ylabel("PCA Component 2")
pca_ax.set_title("PCA Projection")
pca_ax.legend()

print(f"Частка поясненої дисперсії для PCA: {pca.explained_variance_ratio_.sum():.4f}")

plt.tight_layout()
plt.savefig("dimensionality_reduction_comparison.png")
plt.show()