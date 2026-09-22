import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

df = pd.read_csv("zomato.csv")

#EXPLORE DATA STAGE
df.head()

df.columns

df.shape

df.info()

df.describe()

df.isnull().sum()

df['rate'].value_counts()

df['rate'].unique()

#FEATURE ENGINEERING STAGE
df_clean = df.copy()

df_clean['rate'] = df_clean['rate'].replace("NEW", np.nan)

df_clean['rate'] = df_clean['rate'].replace("-", np.nan)

df_clean['rate'] = df_clean['rate'].str.replace("/5", "")

df_clean['rate'].unique()

df_clean.isnull().sum()

df_clean['rate'] = df_clean['rate'].astype(float)

df_clean.info()

df_clean['rate'] 

df_clean.rename(columns={'rate': 'rate(over 5)'}, inplace=True)

df_clean.columns

df_clean.groupby('listed_in(type)')['rate(over 5)'].median()

#-------------------------------------------------------------------------------
df_clean.head()

df['phone'].unique()

df['phone'].value_counts()

df['phone'].str.isnumeric().sum()

df_clean[['phone_first', 'phone_secondary']] = df_clean['phone'].str.split(r'\r?\n', n=1, expand=True)

df_clean[['phone', 'phone_first', 'phone_secondary']].head(10)

df_clean.info()

chars_to_remove = ["+", " "]
cols_to_clean = ["phone_first", "phone","phone_secondary"]

for item in chars_to_remove:
    for cols in cols_to_clean:
        df_clean[cols] = df_clean[cols].str.replace(item, "")
        
df_clean["phone"].unique()

df_clean["phone_first"].unique()

df_clean["phone_secondary"].unique()

df_clean = df_clean.drop(columns="phone")

#-------------------------------------------------------------------------------

df_clean.tail()

df_clean.info()

df_clean['approx_cost(for two people)'].unique()

df_clean['approx_cost(for two people)'].value_counts()

df_clean.isnull().sum()

df_clean['approx_cost(for two people)'] = df_clean['approx_cost(for two people)'].str.replace(",", "")

df_clean['approx_cost(for two people)'] = df_clean['approx_cost(for two people)'].astype(float)
 
df_clean.describe()

#-------------------------------------------------------------------------------

df_clean.tail()

df_clean.isnull().sum()

df_clean["listed_in(type)"].value_counts()

df_clean['rate(over 5)'] = df_clean.groupby('listed_in(type)')['rate(over 5)'].transform(lambda x: x.fillna(x.median()))

df_clean.info()

(df_clean['menu_item'] == '[]').sum()

(df_clean['menu_item'] == '[]').sum() / len(df_clean) * 100

df_clean = df_clean.drop(columns="dish_liked")

df_clean = df_clean.drop(columns="menu_item")

drop_na_col = ['location', 'cuisines']

df_clean = df_clean.dropna(subset=drop_na_col)

df_clean['rest_type'].fillna(df_clean['rest_type'].mode()[0]).value_counts()

df_clean['rest_type'] = df_clean['rest_type'].fillna(df_clean['rest_type'].mode()[0])

df_clean.info()

df_clean.groupby('listed_in(type)')['approx_cost(for two people)'].median()

df_clean['approx_cost(for two people)']  = df_clean.groupby('listed_in(type)')['approx_cost(for two people)'].transform(lambda x: x.fillna(x.median()))

df_clean.info()

df_clean.isnull().sum()
#-----------------------------------------------------------------------------------------------------------

df_clean.columns

df_clean = pd.get_dummies(df_clean, columns=['online_order', 'book_table'], drop_first=True)

df_clean['location'].unique()

df_clean['rest_type'].unique()

df_clean['cuisines'].unique()

df_clean['listed_in(type)'].unique()

df_clean['listed_in(city)'].unique()

df_clean = pd.get_dummies(df_clean, columns=['listed_in(type)'], drop_first=True)

df_clean.info()

#----------------------------------------------------------------------------------------------------------

df_clean.corr(numeric_only=True)

plt.figure(figsize=(16, 12))
sns.heatmap(df_clean.corr(numeric_only=True), annot=True, cmap='coolwarm', center=0)
plt.title('Korelasyon Matrisi')
plt.tight_layout()
plt.show()

sns.boxplot(x='book_table_Yes', y='approx_cost(for two people)', data=df_clean)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(df_clean['rate(over 5)'], kde=True, ax=axes[0])
axes[0].set_title('Rate Dağılımı')

sns.histplot(df_clean['votes'], kde=True, ax=axes[1])
axes[1].set_title('Votes Dağılımı')

sns.histplot(df_clean['approx_cost(for two people)'], kde=True, ax=axes[2])
axes[2].set_title('Approx Cost Dağılımı')

plt.tight_layout()
plt.show()


fig, axes = plt.subplots(1, 3, figsize=(20, 6))

sns.scatterplot(data=df_clean, x='votes', y='rate(over 5)', alpha=0.3, ax=axes[0])
axes[0].set_title('Votes vs Rate')

sns.scatterplot(data=df_clean, x='approx_cost(for two people)', y='rate(over 5)', alpha=0.3, ax=axes[1])
axes[1].set_title('Approx Cost vs Rate')

sns.boxplot(data=df_clean, x='book_table_Yes', y='rate(over 5)', ax=axes[2])
axes[2].set_title('Book Table vs Rate')

plt.tight_layout()
plt.show()

#----------------------------------------------------------------------------------------------------------------------