from flask import Flask, request, jsonify
from flask_cors import CORS
import recipe_recommender
import ast

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' key in request"}), 400
    
    query = data['query']
    
    top_recipes = recipe_recommender.find_top_k_recipes(
        'transformed_recipes.csv',
        query,
        top_k=5
    )

    recipes = []
    nutrition_labels = ["calories", "total fat", "sugar", "sodium", "protein", "saturated fat", "carbohydrates"]
    nutrition_dv = ["", "78", "50", "2300", "50", "20", "275"]
    nutrition_units = ["", "g", "g", "mg", "g", "g", "g"]
    for val in top_recipes.values():
        recipe = f"{val['name'].title()}\n"
        if len(val['description']) > 0:
            recipe += f"{val['description']}\n"
        recipe += f"Total Time: {val['minutes']} min\n"
        
        recipe += "\nIngredients:\n"
        for i in range(val['n_ingredients']):
            recipe += f"{i+1}. {ast.literal_eval(val['ingredients'])[i].capitalize()}\n"

        recipe += "\nDirections:\n"
        for s in range(val['n_steps']):
            recipe += f"{s+1}. {ast.literal_eval(val['steps'])[s].capitalize()}\n"
        
        recipe += "\nNutrition:\n"
        for n, label in enumerate(nutrition_labels):
            pdv = ast.literal_eval(val['nutrition'])[n]
            recipe += f"{label.title()}: {int(pdv*float(nutrition_dv[n])/100) if len(nutrition_dv[n]) > 0 else int(pdv)}{nutrition_units[n]}{' ('+str(int(pdv+0.5))+'%)' if len(nutrition_dv[n]) > 0 else ''}\n"

        recipes.append(recipe.replace(" ,", ","))

    response = "\n\n".join(recipes)
    
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
