import numpy as np
import pandas as pd
import os
import pickle
from nltk.tokenize import word_tokenize

# ------ LOAD IN PREVIOUS FILES ------------
file_path_recipes = "my_dataframe.pkl"

if os.path.exists(file_path_recipes):
    recipe_df = pd.read_pickle('my_dataframe.pkl')
else:
    file_path = r"C:\Users\natha\Downloads\RAW_recipes.csv"
    #Read in the CSV
    recipe_df = pd.read_csv(file_path)
    recipe_df.to_pickle("my_dataframe.pkl")

file_path_model = "w2v_model.pkl"

if os.path.exists(file_path_model):
    w2v_model = pd.read_pickle(file_path_model)


file_path_encoder = "tag_encoder.pkl"

if os.path.exists(file_path_encoder):
    tag_encoder = pd.read_pickle(file_path_encoder)
# ------ DONE LOADING IN PREVIOUS FILES ------------


def load_data(csv_file):
    """Load the dataset containing recipe vectors."""
    return pd.read_csv(csv_file)

def encode_text(text):
    """Encode the text using Word2Vec."""
    words = word_tokenize(str(text).lower())
    
    # Retrieve vectors for words that exist in the Word2Vec model
    vectors = [w2v_model.wv[word] for word in words if word in w2v_model.wv]
    
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(w2v_model.vector_size)

def encode_tags(query):
    """Encode query into a binary tag vector using the tag encoder."""
    query_tags = [word for word in query.split() if word in tag_encoder.classes_]
    query_tag_vector = np.zeros(len(tag_encoder.classes_))
    for tag in query_tags:
        query_tag_vector[tag_encoder.classes_.tolist().index(tag)] = 1
    return query_tag_vector

def calculate_similarity(vec1, vec2, power=1):
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    dot_product = dot_product ** power #this allows us to adjust certain features of the dot product
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    return dot_product / (norm_vec1 * norm_vec2)

def search_recipes(df, query_name_vector, query_desc_vector, query_tag_vector, top_k=5):
    """Search for the top K matching recipes based on name and description vectors."""
    results = []
    
    tag_cols = tag_encoder.classes_[1:]
    recipe_tag_vectors = df[tag_cols].to_numpy()
    
    for idx, row in df.iterrows():
        # Extract name vector from the row
        recipe_name_vector = np.array([row[f'name_vec_{i}'] for i in range(100)])
        name_similarity = calculate_similarity(query_name_vector, recipe_name_vector)
        
        # Extract description vector from the row
        recipe_desc_vector = np.array([row[f'desc_vec_{i}'] for i in range(100)])
        desc_similarity = calculate_similarity(query_desc_vector, recipe_desc_vector, 2)#We want to square the dot product to exaggerate queries with good desc

        recipe_tag_vector = recipe_tag_vectors[idx]

        tag_similarity = calculate_similarity(query_tag_vector, recipe_tag_vector, 2) 

        # Combine similarities Through emprirical trials, I found personally that Tag Similarity will almost always get the protein correct, Description will do the same as well
        # but slightly worse, and name does the worst. 
        # combined_w2v_similarity = 0.6 * name_similarity + 0.15 * desc_similarity + 0.25 * (tag_similarity)
        combined_w2v_similarity = desc_similarity + 0.4 * tag_similarity + 0.1 * name_similarity
        
        # Collect results
        results.append((idx, combined_w2v_similarity))
    
    # Sort results by similarity in descending order and get the top_k
    # print("||||||||||||||||| USING FORUMLA : desc_similarity + 0.4 * tag_similarity + 0.4 * name_similarity |||||||||||||||||")
    results = sorted(results, key=lambda x: x[1], reverse=True)
    top_recipes_idx = [df.iloc[x[0]] for x in results[:top_k]]
    top_recipes = {}
    for i in top_recipes_idx:
        top_recipes[recipe_df.loc[i[0]]["name"]] = recipe_df.loc[i[0]]

    return top_recipes

def find_top_k_recipes(csv_file, query, top_k=5):
    """Find the top K matching recipes for a given query."""
    df = load_data(csv_file)
    
    # Encode query into Word2Vec vectors for name and description
    query_name_vector = encode_text(query)
    query_desc_vector = encode_text(query)
    query_tag_vector = encode_tags(query)[1:] # there is a empty space because of how the multi nominal sklearn obj works

    # Find top matching recipes
    return search_recipes(df, query_name_vector, query_desc_vector, query_tag_vector, top_k=top_k)

# Example usage
if __name__ == "__main__":
    # Adjust file path and query as needed
    top_recipes = find_top_k_recipes(
        'transformed_recipes.csv',
        'Recipes for chicken soup easy',
        top_k=10
    )
    print(top_recipes.keys())
    # pickle.load("tag_encoder.pkl")

