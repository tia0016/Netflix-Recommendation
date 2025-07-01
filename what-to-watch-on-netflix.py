import streamlit as st
import sys
sys.path.append('src')
from recommender import load_data, build_similarity_matrix, recommend_from_titles

# Page config
st.set_page_config(page_title="What to Watch on Netflix", layout="centered")

# Custom Netflix-like styling
st.markdown("""
    <style>
        body {
            background-color: #141414;
            color: white;
        }
        .stApp {
            background-color: #141414;
        }
        .title-style {
            font-size: 48px;
            font-weight: bold;
            color: #e50914;
            text-align: center;
            padding: 10px 0;
        }
        .subtitle {
            text-align: center;
            color: #ffffffaa;
            font-size: 18px;
            padding-bottom: 30px;
        }
        .recommend-box {
            background-color: #222;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        .netflix-button {
            background-color: #e50914;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title-style">What to Watch on Netflix 🍿</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Type your favorite Netflix shows or movies and we’ll recommend similar ones you’ll love!</div>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_everything():
    df = load_data('netflix_titles.csv')
    similarity = build_similarity_matrix(df)
    return df, similarity

df, similarity = load_everything()

# Input box
user_input = st.markdown(
    '<p style="color:#bbbbbb; font-size:16px; ">🎬 Enter 1–3 Netflix titles (comma separated):</p>',
    unsafe_allow_html=True
)
user_input = st.text_input("", placeholder="e.g. Stranger Things, The Crown")


if st.button("🎯 Recommend"):
    titles = [title.strip() for title in user_input.split(',') if title.strip()]
    
    if not titles:
        st.warning("⚠️ Please enter at least one title.")
    else:
        result = recommend_from_titles(df, similarity, titles)
        if isinstance(result, dict):
            st.markdown(f"""
    <div class="recommend-box">
        <h3 style='color:#e50914;'>Top Match:</h3>
        <p style='color:#ffffff; font-size:18px;'><b>{result['Top Match']}</b></p>
        <h4 style='color:#e50914;'>Other Suggestions:</h4>
        <ul style='color:#ffffff; font-size:16px;'>
            <li>{result['Other Options'][0]}</li>
            <li>{result['Other Options'][1]}</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
        else:
            st.error(result)

