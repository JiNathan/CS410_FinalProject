import pandas as pd
from gensim.models import Word2Vec
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import os
nltk.download('punkt')
import pickle

# Step 1: Normalize numeric columns (minutes, n_steps)
def normalize_numeric_columns(df, columns):
    scaler = StandardScaler()
    normalized = scaler.fit_transform(df[columns])
    return pd.DataFrame(normalized, columns=columns)

# Step 2: Convert name and description to numeric representations using Word2Vec
def word2vec_column_representation(df, column):
    # Train Word2Vec model
    sentences = [word_tokenize(str(text)) for text in df[column].fillna("")]
    model = Word2Vec(sentences=sentences, vector_size=100, min_count=1, window=5, sg=1)
    with open("w2v_model.pkl", "wb") as f:
        pickle.dump(model, f)
    # Represent each row by averaging Word2Vec vectors
    def average_vector(text):
        words = word_tokenize(str(text))
        vectors = [model.wv[word] for word in words if word in model.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)
    
    return np.array([average_vector(text) for text in df[column]])

# Step 3: One-hot encode tags
def one_hot_encode_tags(df, column):
    mlb = MultiLabelBinarizer()
    tag_matrix = mlb.fit_transform(df[column])
    tag_df = pd.DataFrame(tag_matrix, columns=mlb.classes_)
    return tag_df, mlb

# Step 4: Combine all features into a new DataFrame
def create_feature_dataframe(df):
    id_df = df[['id']].reset_index(drop=True)
    # Normalize numeric columns
    numeric_columns = ['minutes', 'n_steps']
    numeric_df = normalize_numeric_columns(df, numeric_columns)
    
    # Convert name and description to numeric vectors
    name_vectors = word2vec_column_representation(df, 'name')
    desc_vectors = word2vec_column_representation(df, 'description')
    name_df = pd.DataFrame(name_vectors, columns=[f'name_vec_{i}' for i in range(name_vectors.shape[1])])
    desc_df = pd.DataFrame(desc_vectors, columns=[f'desc_vec_{i}' for i in range(desc_vectors.shape[1])])
    
    # One-hot encode tags
    tags_df, tag_encoder = one_hot_encode_tags(df, 'tags')
    
    # Combine all transformed data into a single DataFrame
    combined_df = pd.concat([id_df, numeric_df, name_df, desc_df, tags_df], axis=1)
    return combined_df, tag_encoder

# Example usage
# Ensure 'tags' is a list of lists before one-hot encoding

file_path_model = "my_dataframe.pkl"

if os.path.exists(file_path_model):
    recipe_df = pd.read_pickle('my_dataframe.pkl')
else:
    file_path = r"C:\Users\natha\Downloads\RAW_recipes.csv"
    #Read in the CSV
    recipe_df = pd.read_csv(file_path)
    recipe_df.to_pickle("my_dataframe.pkl")


recipe_df['tags'] = recipe_df['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)

transformed_df, tag_encoder = create_feature_dataframe(recipe_df)

# Save the transformed DataFrame and tag encoder for future use
transformed_df.to_csv("transformed_recipes.csv")
with open("tag_encoder.pkl", "wb") as f:
    pickle.dump(tag_encoder, f)

print(transformed_df.head())
