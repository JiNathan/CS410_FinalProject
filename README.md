# Recipe Recommender System
UIUC CS 410 (Text Information Systems) Final Project

## Getting Started

### Dependencies

* Node.js v20.17
* npm v10.8
* Python v3.11
* pip v24.3

### Installing

* Clone this GitHub repository
```
git clone https://github.com/JiNathan/CS410_FinalProject
```
* Navigate to the client directory
```
cd ./CS410_FinalProject/client/recipe-generator
```
* Install React dependencies on your local machine
```
npm install
```
* Navigate to the server directory
```
cd ../recipe_database
```
* Install server dependencies on your local machine
```
pip install numpy pandas scikit-learn nltk gensim flask flask-cors python-dotenv
```
* Download 'RAW_recipes.csv' from https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv
* Add your file path to the csv you just downloaded to a .env file
```
echo "file_path = [YOUR_FILE_PATH]\RAW_recipes.csv" >> .env
```
* Preprocess the data and train that model. Note: this may take between 5-10 minutes to execute
```
python db_trainingpreprocess.py
```

### Executing client (React app)

* Navigate to the client directory
```
cd client/recipe-generator
```
* Run on your local machine
```
npm run dev
```
* Open a web browser and navigate to http://localhost:3000

### Executing server

* Navigate to the server directory
```
cd recipe_database
```
* Run flask app in debug mode on your local machine
```
python app.py
```
* OR modify the example usage section at the bottom of recipe_recommender.py and run directly
```
python recipe_recommender.py
```


## About

This project aims to develop a recipe recommender system that leverages text information techniques to provide users with recipes based on their specifications. By analyzing various recipes’ ingredients, instructions, and previous user preferences, we can employ Natural Language Processing techniques (NLP) alongside the Word2Vec model to identify relevant recipes for the user. The system will focus on matching ingredients to recipes based on the similarity of the specific ingredient to the recipe as well as the similarity of related ingredients to the recipe. We will also associate words related to specific dietary restrictions with different recipes in order to provide the user with more relevant and useful recipes.