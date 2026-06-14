import os
import requests
import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── TMDB CONFIG ──────────────────────────────────────────────────────────────
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "ead80456dc69d45f4b5ed88fd8b30571")
TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w342"

# ── LOAD DATA & MODEL ────────────────────────────────────────────────────────
FILE_PATH = "dumped_obj"

data      = pd.read_csv(os.path.join(FILE_PATH, "movie_data_for_app.csv"))
dataframe = pd.read_csv(os.path.join(FILE_PATH, "movie_dataframe_for_app.csv"))
sig       = joblib.load(os.path.join(FILE_PATH, "sigmoid_kernel.pkl"))

# Pre-build sorted movie list once
MOVIE_LIST = sorted(data["original_title"].dropna().unique().tolist())


# ── HELPERS ──────────────────────────────────────────────────────────────────
def fetch_poster(title: str) -> str | None:
    """Return TMDB poster URL for a title, or None on failure."""
    try:
        res = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": TMDB_API_KEY, "query": title, "language": "en-US"},
            timeout=5,
        )
        results = res.json().get("results", [])
        if results and results[0].get("poster_path"):
            return TMDB_IMG_BASE + results[0]["poster_path"]
    except requests.RequestException:
        pass
    return None


def give_recommendations(title: str) -> list[dict]:
    """Return up to 10 similar movies with metadata and poster."""
    if title not in data["original_title"].values:
        return []

    idx = data[data["original_title"] == title].index[0]
    scores = sorted(enumerate(sig[idx]), key=lambda x: x[1], reverse=True)[1:11]
    indices = [i[0] for i in scores]

    cols = [c for c in ["original_title", "vote_average", "genres", "overview"]
            if c in dataframe.columns]
    recs = dataframe.iloc[indices][cols].to_dict("records")

    for r in recs:
        r["poster"] = fetch_poster(r["original_title"])

    return recs


# ── ROUTES ───────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", movies=MOVIE_LIST)


@app.route("/recommend", methods=["POST"])
def recommend():
    """JSON endpoint called by the frontend."""
    body = request.get_json(silent=True) or {}
    title = body.get("title", "").strip()

    if not title:
        return jsonify({"error": "No title provided"}), 400

    recs = give_recommendations(title)
    if not recs:
        return jsonify({"error": f'"{title}" not found in dataset'}), 404

    return jsonify({"title": title, "recommendations": recs})


@app.route("/search")
def search():
    """Autocomplete endpoint."""
    q = request.args.get("q", "").lower()
    matches = [m for m in MOVIE_LIST if q in m.lower()][:20]
    return jsonify(matches)


# ── RUN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
