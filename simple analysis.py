# -*- coding: utf-8 -*-
"""analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Tr89H_IsGqxJ6AhNrbr0-v6KLVoW6aRE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

df = pd.read_csv("data.csv")
df.shape

df.head()

df.info()

df.describe(include='all')

"""### Distribution of KOI Disposition

"""

if "koi_disposition" in df.columns:
    plt.figure()
    sns.countplot(x="koi_disposition", data=df)
    plt.title("Count of KOI Disposition Categories")
    plt.xlabel("KOI Disposition")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

"""### Trend Over Time: Vet Year Distribution

"""

if "vet_year" in df.columns:
    plt.figure()
    sns.countplot(x="vet_year", data=df)
    plt.title("Distribution of Vet Years")
    plt.xlabel("Year of Vetting")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=45)
    plt.show()

"""### Relationship Between Engineered Features and KOI Disposition

"""

if "total_pos_diff" in df.columns and "koi_disposition" in df.columns:
    plt.figure()
    sns.boxplot(x="koi_disposition", y="total_pos_diff", data=df)
    plt.title("Total Positional Discrepancy by KOI Disposition")
    plt.xlabel("KOI Disposition")
    plt.ylabel("Total Positional Discrepancy")
    plt.xticks(rotation=45)
    plt.show()

"""### Distribution of Engineered Features

"""

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
if "pos_diff_mdec" in df.columns:
    sns.histplot(df["pos_diff_mdec"], bins=30, kde=True, ax=axes[0])
    axes[0].set_title("Distribution of Positional Difference in Declination")
    axes[0].set_xlabel("Absolute Difference in Declination")
if "total_pos_diff" in df.columns:
    sns.histplot(df["total_pos_diff"], bins=30, kde=True, ax=axes[1])
    axes[1].set_title("Distribution of Total Positional Discrepancy")
    axes[1].set_xlabel("Total Positional Difference (mdec + msky)")
plt.tight_layout()
plt.show()

"""### Dimensionality Reduction with PCA
### --------------------------

### Select numerical columns from the dataset
"""

num_data = df.select_dtypes(include=[np.number])
print("\nNumerical columns used for PCA:")
print(num_data.columns.tolist())

num_data_clean = num_data.dropna()

"""### Standardize the numerical features"""

scaler = StandardScaler()
scaled_data = scaler.fit_transform(num_data_clean)

"""### Apply PCA to reduce the data to 2 components for visualization"""

pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)
print("Explained variance by principal components:", pca.explained_variance_ratio_)

"""Create a DataFrame for the PCA results"""

pca_df = pd.DataFrame(data=pca_result, columns=["PC1", "PC2"])

pca_df["koi_disposition"] = df.loc[num_data_clean.index, "koi_disposition"].values

"""pca result"""

plt.figure()
sns.scatterplot(x="PC1", y="PC2", hue="koi_disposition", data=pca_df, palette="viridis", alpha=0.7)
plt.title("PCA of Numerical Features (Colored by KOI Disposition)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title="KOI Disposition", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

"""Correlaton analysis"""

plt.figure()
corr_matrix = num_data.corr()
sns.heatmap(corr_matrix, annot=True, cmap="viridis", linewidths=0.5)
plt.title("Correlation Matrix of Numerical Features")
plt.show()

