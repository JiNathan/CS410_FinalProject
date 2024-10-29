import pandas as pd
from gensim.models import Word2Vec
from sklearn.preprocessing import StandardScaler
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import os

nltk.download('punkt')

file_path_model = "my_dataframe.pkl"


if os.path.exists(file_path_model):
    recipe_df = pd.read_pickle('my_dataframe.pkl')
else:
    file_path = r"C:\Users\natha\Downloads\RAW_recipes.csv"
    #Read in the CSV
    recipe_df = pd.read_csv(file_path)
    recipe_df.to_pickle("my_dataframe.pkl")



# ------ Notes about Dataframe -----
# Columns: ['name', 'id', 'minutes', 'contributor_id', 'submitted', 'tags', 'nutrition', 'n_steps', 'steps', 'description', 'ingredients', 'n_ingredients']
# Name: text information, we can use this to match to queries when asked I want to cook X, build vocab and word2vecmodel to compare to exist names
# ID: sorta useless
# Minutes: Numeric Data helpful as a search feature (very simple to implement)
# Contributor ID: Also kinda useless
# Tags: Very useful, consider a bit vector approach. We take query -> word2vec to determine what tags fit. Tags represented as bit vector, then dot with each recipe
# Example of tags: ['60-minutes-or-less', 'time-to-make', 'course', 'main-ingredient', 'cuisine', 'preparation', 'occasion', 'north-american', 'side-dishes', 'vegetables', 'mexican', 'easy', 'fall', 'holiday-event', 'vegetarian', 'winter', 'dietary', 'christmas', 'seasonal', 'squash']
# nutrition: Nutrition information (calories (#), total fat (PDV), sugar (PDV) , sodium (PDV) , protein (PDV) , saturated fat
# Number of steps in recipe: Numeric, easy for complexity rating
# description: Easy text information as well
# steps: most likely not necessary

# PLAN FOR FEATURES FOR RECOMMENDATION MODEL: Num of Steps, Bit Vector of Tags, Numeric Similairty of Description to Query, Numeric Similairty of Name to Query,
# User can then search recommendations based on time

#Vectorize Tags into a binary matrix
def vectorize_tags(df):
    all_tags = set(tag for tags in df['tags'] for tag in tags)
    tag_columns = {tag: i for i, tag in enumerate(all_tags)}
    
    # Create a binary matrix for tags
    tag_matrix = np.zeros((len(df), len(tag_columns)))
    for idx, tags in enumerate(df['tags']):
        for tag in tags:
            if tag in tag_columns:
                tag_matrix[idx, tag_columns[tag]] = 1

    # Convert to DataFrame
    tag_df = pd.DataFrame(tag_matrix, columns=tag_columns.keys())
    return tag_df

# Step 2: Train a Word2Vec model on name and description text
def train_word2vec_model(df, column):
    sentences = []
    for text in df[column]:
        words = [word for word in str(text).split() if word]
        sentences.append(words)
    model = Word2Vec(sentences=sentences, vector_size=100, min_count=1, window=5, sg=1)
    return model

# Step 3: Calculate similarity between query and each text field
def calculate_similarity(df, query, model, column):
    query_words = word_tokenize(query)
    query_vec = np.mean([model.wv[word] for word in query_words if word in model.wv], axis=0) if query_words else np.zeros(model.vector_size)
    
    similarities = []
    for text in df[column]:
        words = word_tokenize(str(text))
        text_vec = np.mean([model.wv[word] for word in words if word in model.wv], axis=0) if words else np.zeros(model.vector_size)
        similarity = np.dot(query_vec, text_vec) if text_vec is not None else 0
        similarities.append(similarity)
        
    return similarities

# Step 4: Combine all transformations into a new DataFrame
def transform_dataset(df, query):
    # Tag vectorization
    tag_df = vectorize_tags(df)
    
    # Numeric features
    numeric_features = df[['minutes', 'n_steps']]
    
    # Word2Vec model
    name_model = train_word2vec_model(df, 'name')
    desc_model = train_word2vec_model(df, 'description')
    
    # Similarity features
    name_similarity = calculate_similarity(df, query, name_model, 'name')
    description_similarity = calculate_similarity(df, query, desc_model, 'description')
    
    # Combine all features
    transformed_df = pd.concat([
        numeric_features.reset_index(drop=True),
        tag_df.reset_index(drop=True),
        pd.DataFrame({'name_similarity': name_similarity, 'description_similarity': description_similarity})
    ], axis=1)
    
    # Standardize the numeric features
    scaler = StandardScaler()
    transformed_df[['minutes', 'n_steps', 'name_similarity', 'description_similarity']] = scaler.fit_transform(
        transformed_df[['minutes', 'n_steps', 'name_similarity', 'description_similarity']]
    )
    
    return transformed_df

# Example usage
query = "I want to cook something quick and vegetarian"
transformed_df = transform_dataset(recipe_df, query)

print(transformed_df.head())