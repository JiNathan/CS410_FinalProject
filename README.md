# CS410_FinalProject

The Recipe Recommendation Engine
The recommendation engine aims to assist users in finding recipes tailored to their queries by analyzing and comparing textual attributes like names, descriptions, and tags. It uses a dataset of recipes and implements techniques for text encoding, feature extraction, and similarity computation to return the most relevant matches.

Key Topics in Text-Information Systems
1. Text Vectorization with Word2Vec
A cornerstone of the system is the transformation of textual data into numerical representations using Word2Vec. This word-embedding technique maps words in a high-dimensional vector space where semantic relationships between words are preserved, which is used similairly to how it was applied throughout CS 410 like in HW 1. For instance, words like "chicken" and "turkey" may have similar vector representations due to their contextual similarity in recipes, which allows us to provide relevant documents back to the user.

In this project, the Word2Vec model was trained using tokenized recipe names and descriptions. Each word's vector was averaged to create a fixed-length representation for each recipe. This representation enabled efficient computation of similarities between user queries and recipes. This was particularly critical so that the query and the recipe will be able to compare semantic meanings, which provided a very accurate system that would provide relevant feedback to the user.

2. Feature Engineering and Data Transformation
The engine combines several features to represent a recipe:

Normalized Numeric Features: Recipe metadata like preparation time (minutes) and steps (n_steps) were scaled using StandardScaler. Normalization ensures these features have equal weight in similarity computations, which was a very importance concept throughout the class in preprocessing data to ensure for stable mathematical computations.
One-Hot Encoding of Tags: Tags like "vegetarian," "easy," and "gluten-free" were one-hot encoded using MultiLabelBinarizer. This created a binary vector where each dimension indicates the presence of a specific tag. This was meant to model the bit-vector discussions had in class, describing how words can be matched to documents, but instead we preform tagging and tag-extraction of the queries.

3. Similarity Computation and Ranking
To find relevant recipes, the engine computes the cosine similarity between query vectors and recipe vectors. Cosine similarity is an effective measure for comparing high-dimensional vectors by focusing on their directional alignment rather than magnitude, as the magnitude of these vectors do not contain as much information as their directional alignment due to the nature of W2V.

The system uses a weighted combination of three similarity scores:

Name Similarity: Measures the relevance of the recipe's name to the query.
Description Similarity: Gives higher importance to detailed matches in recipe descriptions.
Tag Similarity: Emphasizes categorical matches like diet preferences or meal types.

The weights (e.g., 0.6 for description similarity) were fine-tuned empirically, primarily using the same intuition as the feedback systems we used in class, where we logged the number of relevant documents compared to the contribution of the three similarities. This intuition was directly from the rocchio feedback algorithm where alpha, beta, and gamma were adjusted to move queries closer to relevant docs, but instead of changing the query in this case, we instead alter the ranking function in a similair manner.

Another key factor of this ranking is that the dot product for Description and Tag simialirty were squared, which is a very similair intuition to concepts introduced into this class
involving rank boosting and ranking algorithms, and the mathematical foundatin of this method can be found throughout the class include topics like MSE, etc. Squaring these two were
critical for the preformance as it decrease non-relevant dot products and increases larger dot products, which allowed for bigger differences between non-relevant and relevant documents. Although in general this would boost the preformance of any recommendation system, we believe it was particularly important here as semantically, many of the recipes are similair as they are all within the same domain of words. For example, if we were doing websearch for the key "Steak", it would easily classify "Gold", "Computer", "Text" much further away from "Beef". However, the domain we search for instead only contains recipes, meaning "Steak" would be compared against "Pork", "Tofu", "Lamb", all of which may have very close similarities as "Beef". This observation was why squaring was implementing in this similarity function.