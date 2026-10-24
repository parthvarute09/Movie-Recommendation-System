import os, requests
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# ---------------- TMDB CONFIG ----------------
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "ead80456dc69d45f4b5ed88fd8b30571")
TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w500"

# ---------------- LOAD DATA ----------------
file_path = "dumped_obj"

data = pd.read_csv(os.path.join(file_path, "movie_data_for_app.csv"))
dataframe = pd.read_csv(os.path.join(file_path, "movie_dataframe_for_app.csv"))
sig = joblib.load(os.path.join(file_path, "sigmoid_kernel.pkl"))

# ---------------- FETCH POSTER ----------------
def fetch_poster(title):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "en-US"
        }

        res = requests.get(url, params=params, timeout=5)

        if res.status_code != 200:
            return None

        results = res.json().get("results", [])

        if results and results[0].get("poster_path"):
            return TMDB_IMG_BASE + results[0]["poster_path"]

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")

    return None

# ---------------- RECOMMENDATION ----------------
def give_recommendations(title):
    # Handle movie not found
    if title not in data['original_title'].values:
        return []

    idx = data[data['original_title'] == title].index[0]

    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    sig_scores = sig_scores[1:11]
    indices = [i[0] for i in sig_scores]

    # Safe column selection
    cols = ['original_title', 'vote_average', 'genres', 'overview']
    cols = [c for c in cols if c in dataframe.columns]

    recs = dataframe.iloc[indices][cols].to_dict('records')

    # Add posters
    for r in recs:
        r['poster'] = fetch_poster(r['original_title'])

    return recs

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    movies = sorted(data['original_title'].dropna().unique())
    recommendations = []
    selected = None

    if request.method == "POST":
        selected = request.form.get("movie")

        if selected:
            recommendations = give_recommendations(selected)

    return render_template(
        "index.html",
        movies=movies,
        recommendations=recommendations,
        selected=selected
    )

@app.route("/search")
def search():
    q = request.args.get("q", "").lower()
    movies = sorted(data['original_title'].dropna().unique())

    result = [m for m in movies if q in m.lower()][:20]
    return jsonify(result)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)