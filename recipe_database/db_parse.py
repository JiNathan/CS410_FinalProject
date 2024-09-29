import json

class Recipe:
    def __init__(self, recipe_dict):
        self.id = recipe_dict.get('id')
        self.name = recipe_dict.get('name')
        self.source = recipe_dict.get('source')
        self.preptime = recipe_dict.get('preptime')
        self.waittime = recipe_dict.get('waittime')
        self.cooktime = recipe_dict.get('cooktime')
        self.servings = recipe_dict.get('servings')
        self.comments = recipe_dict.get('comments')
        self.calories = recipe_dict.get('calories')
        self.fat = recipe_dict.get('fat')
        self.satfat = recipe_dict.get('satfat')
        self.carbs = recipe_dict.get('carbs')
        self.fiber = recipe_dict.get('fiber')
        self.sugar = recipe_dict.get('sugar')
        self.protein = recipe_dict.get('protein')
        self.instructions = recipe_dict.get('instructions')
        self.ingredients = recipe_dict.get('ingredients')
        self.tags = recipe_dict.get('tags')

    def __str__(self):
        return (f"Recipe: {self.name}. Tags: {self.tags}")
    
#read in dp recipes json file
with open('db-recipes.json', 'r') as file:
    data = json.load(file)

#Get recipes in list
recipe_tokens = list(data.values())
recipe_list = []
for recipe in recipe_tokens:
    temprecipe = Recipe(recipe)
    recipe_list.append(temprecipe)
    
#Display Brief overview of Recipes
for r in recipe_list:
    print(r)