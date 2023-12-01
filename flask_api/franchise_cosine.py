import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.io as pio
import seaborn as sns
import missingno as mno

from sklearn.feature_extraction.text import TfidfVectorizer

# Dataset perlu diperbarui
franchise = pd.read_csv('https://drive.google.com/uc?export=download&id=1Vl0KXqTxcygmlnM5ZDqy8olOWhenCQ_R', low_memory=False)
franchise.info()
franchise.head()

franchise.duplicated().sum()

# Describe the features
feature = ['franchise_name', 'description', 'franchise_category', 'franchise_type', 'costs']

franchise[feature].describe()

counts_franchise_name = franchise['franchise_name'].value_counts()
count_percentage = franchise['franchise_name'].value_counts(1)*100
counts_dffranchise_name = pd.DataFrame({'Franchise':counts_franchise_name.index,'Counts':counts_franchise_name.values,'Percent%':np.round(count_percentage.values,2)})
top_10_franchise_name = counts_dffranchise_name.head(10)
top_10_franchise_name

pd_type = pd.DataFrame()
pd_type["Count"] = franchise["franchise_category"].value_counts()
pd_type["Count%"] = franchise["franchise_category"].value_counts()/franchise.shape[0]*100
pd_type

counts = franchise['franchise_type'].value_counts()
count_percentage = franchise['franchise_type'].value_counts(1)*100
counts_df = pd.DataFrame({'Franchise Type':counts.index,'Counts':counts.values,'Percent%':np.round(count_percentage.values,2)})
counts_df

franchise['description']=franchise['description'].astype('category')
franchise['labels']=franchise['description'].cat.codes
franchise.head()

counts_effect = franchise['description'].value_counts()
count_percentage = franchise['description'].value_counts(1)*100
counts_effect_df = pd.DataFrame({'Description':counts_effect.index,'Counts':counts_effect.values,'Percent%':np.round(count_percentage.values,2)})
counts_effect_df.head(10)

# Remove duplicated rows (14 in total)
franchise.drop_duplicates(inplace=True)

# Re-checking the existence of duplicated rows
franchise.duplicated().sum()

# Fill NaN values with an empty string before splitting
franchise['franchise_category'].fillna('', inplace=True)

# Separate all skintype into one list, considering comma + space as separators
franchise_category = franchise['franchise_category'].str.split(', ').tolist()

# Flatten the list
flat_franchise_category = [item for sublist in franchise_category for item in sublist]

# Convert to a set to make unique
set_franchise_category = set(flat_franchise_category)

# Back to list
unique_franchise_category = list(set_franchise_category)

# Create columns by each unique skintype
franchise = franchise.reindex(franchise.columns.tolist() + unique_franchise_category, axis=1, fill_value=0)

# For each value inside column, update the dummy
for index, row in franchise.iterrows():
    for val in row.franchise_category.split(', '):
        if val != 'NA' and val in unique_franchise_category:
            franchise.loc[index, val] = 1

franchise.head(5)

franchise.to_csv("export_walbiz.csv")

# Modeling with Content Based Filtering
# Initializing TfidfVectorizer
tf = TfidfVectorizer()

# Perform IDF calculation on 'notable_efects' data
tf.fit(franchise['franchise_category'])

# Mapping array from integer index feature to name feature
tf.get_feature_names_out()

# Doing fit then transformed to matrix form
tfidf_matrix = tf.fit_transform(franchise['franchise_category'])

# Viewing matrix size TF IDF
shape = tfidf_matrix.shape
shape

# Convert TF-IDF vector in matrix form with todense() function
tfidf_matrix.todense()

# Making dataframe to see TF-IDF matrix

pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tf.get_feature_names_out(),
    index=franchise.franchise_name
).sample(shape[1], axis=1).sample(10, axis=0)

# Calculating Cosine Similarity on the TF-IDF matrix
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

cosine_sim_df = pd.DataFrame(cosine_sim, index=franchise['franchise_name'], columns=franchise['franchise_name'])

cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

def franchise_recommendations(nama, similarity_data=cosine_sim_df, items=franchise[['franchise_name', 'franchise_category','franchise_type', 'costs']], k=5):

    # Retrieve data by using argpartition to partition indirectly along a given axis
    # Dataframe converted to be numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama].to_numpy().argpartition(
        range(-1, -k, -1))

    # Retrieve data with the greatest similarity from the existing index
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Drop a name so that the name of the product we are looking for doesnt' appear in the list of recommendations
    closest = closest.drop(nama, errors='ignore')

    return pd.DataFrame(closest).merge(items).head(k)

franchise[franchise.franchise_name.eq('Bakso Kemon')].head()

franchise_recommendations("Bakso Kemon")