# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# Load the dataset (assuming it's already imported as per the challenge)
# books = pd.read_csv('BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
# users = pd.read_csv('BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
# ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")

# Filter users with at least 200 ratings
user_counts = ratings['User-ID'].value_counts()
ratings = ratings[ratings['User-ID'].isin(user_counts[user_counts >= 200].index)]

# Filter books with at least 100 ratings
book_counts = ratings['ISBN'].value_counts()
ratings = ratings[ratings['ISBN'].isin(book_counts[book_counts >= 100].index)]

# Create pivot table
book_ratings = ratings.pivot(index='ISBN', columns='User-ID', values='Book-Rating').fillna(0)

# Merge with book titles
book_ratings = book_ratings.merge(books[['ISBN', 'Book-Title']], left_index=True, right_on='ISBN')
book_ratings.set_index('ISBN', inplace=True)

# Convert to sparse matrix
book_matrix = csr_matrix(book_ratings.drop('Book-Title', axis=1).values)

# Initialize and fit the model
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(book_matrix)

def get_recommends(book_title):
    # Find the book in the dataset
    try:
        book_idx = book_ratings[book_ratings['Book-Title'] == book_title].index[0]
    except IndexError:
        return [book_title, []]  # Return empty recommendations if book not found
    
    # Get the index of the book in the matrix
    matrix_idx = book_ratings.index.get_loc(book_idx)
    
    # Find 6 nearest neighbors (including the book itself)
    distances, indices = knn.kneighbors(book_matrix[matrix_idx], n_neighbors=6)
    
    # Create recommendations list, excluding the first neighbor (the book itself)
    recommended_books = []
    for dist, idx in zip(distances[0][1:], indices[0][1:]):  # Skip first neighbor
        book_title_rec = book_ratings.iloc[idx]['Book-Title']
        recommended_books.append([book_title_rec, dist])
    
    return [book_title, recommended_books[:5]]  # Return only 5 recommendations

# Test the function
books = get_recommends("The Queen of the Damned (Vampire Chronicles (Paperback))")
print(books)