import requests

TMDB_IMG_BASE = "https://image.tmdb.org/t/p/w500"
DEFAULT_POSTER = "https://via.placeholder.com/500x750?text=No+Image"

# Simple cache to avoid repeated API calls
poster_cache = {}

def fetch_poster(title, api_key):
    if title in poster_cache:
        return poster_cache[title]

    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": api_key, "query": title}
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        results = data.get("results", [])

        if results and results[0].get("poster_path"):
            poster = TMDB_IMG_BASE + results[0]["poster_path"]
            poster_cache[title] = poster
            return poster

    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")

    poster_cache[title] = DEFAULT_POSTER
    return DEFAULT_POSTER