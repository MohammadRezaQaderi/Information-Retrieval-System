# Information-Retrieval-System
The Information retrieval Project :) 

# About the project
This project is my information retrieval course project which is a search engine for retrieving news documents based on users' queries. <br>
The project in implmented using [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/) and [gensim](https://github.com/RaRe-Technologies/gensim) libraries. 

# Preprocessing

For all query answering approaches, we need a positional posting list which is extracted in [](). <br>
Also for word embedding purposes, a word to vector model is constructed in []().

# Categorization

In order to answer queries fast enough, we need to categorize documents and queries. <br>
In []() a supervised categorizing approach is implemented using the KNN algorithm. <br>
In []() an unsupervised approach is implemented using the K-means algorithm.

# Query answering

Multiple query answering approaches are implemented:
+ Simple common word counting approach in []().
+ An approach based on inner product and tf-idf in []() which uses champion lists in order to speed up.
+ A word embedding-based approach with inner product criteria in []().
+ A fast version of the word embedding approach in []() which uses clusters in order to speed up.
+ A category aware approach in []() that user enters the category along with the query itself.
