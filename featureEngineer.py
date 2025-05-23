# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1APGF7AYf1Qk9kQ18wgWXt1P0ywYqgX6s
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

df = pd.read_csv('cleankepler.csv')

df.head()

df.info()

df.describe(include='all')

df.shape

if 'koi_vet_date' in df.columns:
    df['koi_vet_date'] = pd.to_datetime(df['koi_vet_date'], errors='coerce')
    print("Converted koi_vet_date to datetime.")

categorical_cols = ['koi_disposition', 'koi_vet_stat', 'koi_pdisposition', 'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co']

for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype('category')
        # Optionally, create dummy/indicator variables.
        dummies = pd.get_dummies(df[col], prefix=col)
        df = pd.concat([df, dummies], axis=1)
        print(f"Encoded {col} as a categorical variable.")

"""### Positional Difference in Declination: absolute difference between 'koi_dicco_mdec' and 'koi_dikco_mdec'"""

if 'koi_dicco_mdec' in df.columns and 'koi_dikco_mdec' in df.columns:
    df['pos_diff_mdec'] = np.abs(df['koi_dicco_mdec'] - df['koi_dikco_mdec'])
    print("Created feature 'pos_diff_mdec'.")

"""### Positional Difference in Sky Magnitude: difference between 'koi_dicco_msky' and 'koi_dikco_msky'

"""

if 'koi_dicco_msky' in df.columns and 'koi_dikco_msky' in df.columns:
    df['pos_diff_msky'] = np.abs(df['koi_dicco_msky'] - df['koi_dikco_msky'])
    print("Created feature 'pos_diff_msky'.")

"""### Average error in Declination measurements: average of the two error columns for declination, if available

"""

if 'koi_dicco_mdec_err' in df.columns and 'koi_dikco_mdec_err' in df.columns:
    df['avg_err_mdec'] = df[['koi_dicco_mdec_err', 'koi_dikco_mdec_err']].mean(axis=1)
    print("Created feature 'avg_err_mdec'.")

"""### Average error in Declination measurements: average of the two error columns for declination, if available

"""

if 'pos_diff_mdec' in df.columns and 'pos_diff_msky' in df.columns:
    df['total_pos_diff'] = df['pos_diff_mdec'] + df['pos_diff_msky']
    print("Created feature 'total_pos_diff'.")

"""### time-related features from koi_vet_date, like the vet year."""

if 'koi_vet_date' in df.columns:
    df['vet_year'] = df['koi_vet_date'].dt.year
    print("Created feature 'vet_year' from koi_vet_date.")



"""### Overview of engineered features"""

print(df[['pos_diff_mdec', 'pos_diff_msky', 'avg_err_mdec', 'total_pos_diff']].head())

"""### Summary statistics for new features"""

df[['pos_diff_mdec', 'pos_diff_msky', 'avg_err_mdec', 'total_pos_diff']].describe()

"""Correlation Analysis

Select numerical columns for correlation analysis. We include our new features
"""

num_cols = df.select_dtypes(include=[np.number])
corr_matrix = num_cols.corr()

plt.figure()
sns.heatmap(corr_matrix, annot=True, cmap='viridis', linewidths=0.5)
plt.title('Correlation Matrix Including Engineered Features')
plt.show()



"""Distribution of positional difference in declination"""

if 'pos_diff_mdec' in df.columns:
    plt.figure()
    sns.histplot(df['pos_diff_mdec'], bins=30, kde=True)
    plt.title('Distribution of Positional Difference in Declination')
    plt.xlabel('Absolute Difference in Declination')
    plt.ylabel('Frequency')
    plt.show()

""" Distribution of total positional discrepancy"""

if 'total_pos_diff' in df.columns:
    plt.figure()
    sns.histplot(df['total_pos_diff'], bins=30, kde=True)
    plt.title('Distribution of Total Positional Discrepancy')
    plt.xlabel('Total Positional Difference (mdec + msky)')
    plt.ylabel('Frequency')
    plt.show()

"""

```
# This is formatted as code
```

"""

if 'koi_disposition' in df.columns and 'total_pos_diff' in df.columns:
    plt.figure()
    sns.boxplot(x='koi_disposition', y='total_pos_diff', data=df)
    plt.title('Total Positional Discrepancy by KOI Disposition')
    plt.xlabel('KOI Disposition')
    plt.ylabel('Total Positional Discrepancy')
    plt.xticks(rotation=45)
    plt.show()

print("Feature engineering and initial analysis complete.")

from google.colab import files
df.to_csv('data.csv', index=False, encoding='utf-8')
files.download('data.csv')

