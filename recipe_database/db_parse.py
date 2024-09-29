import pandas as pd
import sqlite3

file_path = r"C:\Users\natha\Downloads\RAW_recipes.csv"
# Step 1: Read in the data
recipe_df = pd.read_csv(file_path)

# Step 2: Connect to SQLite and create the database
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Step 3: Create a table schema based on the CSV columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    name TEXT,
    id INTEGER PRIMARY KEY,
    minutes INTEGER,
    contributor_id INTEGER,
    submitted DATE,
    tags TEXT,
    nutrition TEXT,
    n_steps INTEGER,
    steps TEXT,
    description TEXT,
    ingredients TEXT,
    n_ingredients INTEGER
)
''')

# Step 4: Insert the data into the SQLite table
recipe_df.to_sql('recipes', conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()