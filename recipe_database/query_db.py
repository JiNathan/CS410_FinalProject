import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Query for recipes that take between 30 and 35 minutes
cursor.execute('''
SELECT name, minutes, ingredients, steps 
FROM recipes 
WHERE minutes BETWEEN 30 AND 35
''')

# Fetch all matching recipes
recipes = cursor.fetchall()

# Print the results
if recipes:
    print("Recipes that take between 30 and 35 minutes:\n")
    for recipe in recipes:
        name, minutes, ingredients, steps = recipe
        print(f"Recipe Name: {name}")
        print(f"Time: {minutes} minutes")
        print(f"Ingredients: {ingredients}")
        print(f"Steps: {steps}\n")
else:
    print("No recipes found that match the criteria.")

# Close the connection
conn.close()