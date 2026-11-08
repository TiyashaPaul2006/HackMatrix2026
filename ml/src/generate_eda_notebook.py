import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

nb.cells = [
    nbf.v4.new_markdown_cell("""# AI-Powered Web Threat Detection & Digital Trust Intelligence
## Exploratory Data Analysis & Feature Investigation

This notebook documents the exploratory analysis of the `LegitPhish` dataset, verifying feature definitions, missing value patterns, domain distributions, and class balance.
"""),
    nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')"""),

    nbf.v4.new_markdown_cell("### 1. Load Cleaned Dataset"),
    nbf.v4.new_code_cell("""df = pd.read_csv('../processed/LegitPhish_Cleaned.csv')
print(f"Dataset Shape: {df.shape}")
print(f"Null Values:\\n{df.isnull().sum()[df.isnull().sum() > 0]}")
df.head()"""),

    nbf.v4.new_markdown_cell("### 2. Target Class Distribution"),
    nbf.v4.new_code_cell("""class_counts = df['ClassLabel'].value_counts()
print(f"Legitimate (0): {class_counts[0]:,} ({class_counts[0]/len(df):.2%})")
print(f"Phishing (1):   {class_counts[1]:,} ({class_counts[1]/len(df):.2%})")

plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='ClassLabel', palette=['#1f77b4', '#d62728'])
plt.title('Target Class Distribution (0=Legitimate, 1=Phishing)')
plt.xlabel('Class Label')
plt.ylabel('Count')
plt.show()"""),

    nbf.v4.new_markdown_cell("### 3. Feature Summary Statistics"),
    nbf.v4.new_code_cell("""features = [c for c in df.columns if c not in ['URL', 'ClassLabel']]
df[features].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']]"""),

    nbf.v4.new_markdown_cell("### 4. Correlation Analysis"),
    nbf.v4.new_code_cell("""plt.figure(figsize=(14, 10))
corr = df[features + ['ClassLabel']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Feature Correlation Matrix with Phishing Target')
plt.show()""")
]

out_path = os.path.join(os.path.dirname(__file__), '..', 'Notebooks', '01_dataset_analysis.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook generated successfully at {out_path}")

