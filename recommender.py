import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and clean dataset
def load_data(path='data/netflix_titles.csv'):
    df = pd.read_csv(path)

    # Fill missing values
    df['director'] = df['director'].fillna('')
    df['cast'] = df['cast'].fillna('')
    df['listed_in'] = df['listed_in'].fillna('')
    df['description'] = df['description'].fillna('')

    # Create combined 'tags' column
    df['tags'] = (
        df['title'] + ' ' + df['director'] + ' ' + df['cast'] + ' ' +
        df['listed_in'] + ' ' + df['description']
    ).str.lower()

    return df

# Build similarity matrix
def build_similarity_matrix(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['tags'])
    similarity = cosine_similarity(tfidf_matrix)
    return similarity

# Recommend based on input titles
def recommend_from_titles(df, similarity, fav_titles):
    indices = []
    for title in fav_titles:
        try:
            idx = df[df['title'].str.lower() == title.lower()].index[0]
            indices.append(idx)
        except:
            print(f"❌ Title not found: {title}")

    if not indices:
        return "No valid titles provided."

    # Average similarity
    avg_similarity = sum([similarity[i] for i in indices]) / len(indices)

    # Sort and exclude input titles
    sim_scores = list(enumerate(avg_similarity))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] not in indices]

    top_match = df.iloc[sim_scores[0][0]]['title']
    alt1 = df.iloc[sim_scores[1][0]]['title']
    alt2 = df.iloc[sim_scores[2][0]]['title']

    return {
        'Top Match': top_match,
        'Other Options': [alt1, alt2]
    }
