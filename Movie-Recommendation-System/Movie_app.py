import pandas as pd
import joblib
import streamlit as st
import os

# ---------------- LOAD DATA ----------------
def load_data(file_path):
    try:
        data = pd.read_csv(os.path.join(file_path, "movie_data_for_app.csv"))
        dataframe = pd.read_csv(os.path.join(file_path, "movie_dataframe_for_app.csv"))
        return data, dataframe
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# ---------------- LOAD MODELS ----------------
def load_models(file_path):
    try:
        sig = joblib.load(os.path.join(file_path, "sigmoid_kernel.pkl"))
        tfv = joblib.load(os.path.join(file_path, "tfidf_vectorizer.pkl"))
        return sig, tfv
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

# ---------------- RECOMMENDATION FUNCTION ----------------
def give_recommendations(title, sig, data, dataframe):
    try:
        # Get index of the movie
        idx = data[data['original_title'] == title].index[0]

        # Get similarity scores
        sig_scores = list(enumerate(sig[idx]))

        # Sort movies based on similarity score
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Get top 10 similar movies (excluding itself)
        sig_scores = sig_scores[1:11]

        # Get movie indices
        movie_indices = [i[0] for i in sig_scores]

        # Return movie titles
        return dataframe['original_title'].iloc[movie_indices].tolist()

    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

# ---------------- PATH ----------------
file_path = r"D:\Movie Recommended\dumped_obj"

data, dataframe = load_data(file_path)
sig, tfv = load_models(file_path)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Simple Movie Recommender", layout="centered")

st.title("🎬 Simple Movie Recommender")
st.write("Find movies similar to your favorite one")

if data is not None:
    movie_list = sorted(data['original_title'].dropna().unique())
    selected_movie = st.selectbox("Select a movie:", movie_list)

    if st.button("Get recommendations"):
        if selected_movie:
            recommendations = give_recommendations(selected_movie, sig, data, dataframe)

            st.subheader("Movies similar to: " + selected_movie)
            for index, movie in enumerate(recommendations):
                st.write(f"{index + 1}. {movie}")

st.markdown("----")