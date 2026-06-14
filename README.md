# 🎬 Movie Recommender — Setup Guide

## Project Structure

```
movie_recommender/
├── app.py                  ← Flask backend
├── requirements.txt
├── dumped_obj/             ← YOUR existing ML files go here
│   ├── movie_data_for_app.csv
│   ├── movie_dataframe_for_app.csv
│   └── sigmoid_kernel.pkl
├── templates/
│   └── index.html          ← Frontend HTML
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## Step 1 — Copy your ML files

Move your dumped_obj folder into the project root:

```
movie_recommender/
└── dumped_obj/
    ├── movie_data_for_app.csv
    ├── movie_dataframe_for_app.csv
    └── sigmoid_kernel.pkl
```

---

## Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3 — Run the app

```bash
python app.py
```

Open your browser at: http://127.0.0.1:5000

---

## How it connects (the flow)

```
User types movie name
       ↓
Frontend autocomplete  →  GET /search?q=...  →  returns matching titles
       ↓
User clicks Recommend
       ↓
JS fetch()             →  POST /recommend    →  { "title": "Inception" }
                                   ↓
                          app.py: give_recommendations()
                                   ↓
                          sigmoid kernel similarity lookup
                                   ↓
                          fetch_poster() for each result (TMDB API)
                                   ↓
                          returns JSON: { recommendations: [...] }
       ↓
main.js renders movie cards with poster, rating, genre, overview
```

---

## API Endpoints

| Method | Route         | Description                          |
|--------|---------------|--------------------------------------|
| GET    | `/`           | Serve the main page                  |
| POST   | `/recommend`  | Get 10 movie recommendations (JSON)  |
| GET    | `/search?q=`  | Autocomplete movie titles (JSON)     |

### POST /recommend

Request body:
```json
{ "title": "Inception" }
```

Response:
```json
{
  "title": "Inception",
  "recommendations": [
    {
      "original_title": "Interstellar",
      "vote_average": 8.1,
      "genres": "[{\"name\": \"Sci-Fi\"}, ...]",
      "overview": "A team of explorers...",
      "poster": "https://image.tmdb.org/t/p/w342/..."
    }
  ]
}
```

---

## Optional: Change TMDB API key

Replace the key in app.py line 10, or set an environment variable:

```bash
export TMDB_API_KEY=your_key_here
python app.py
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `FileNotFoundError: dumped_obj/...` | Make sure your dumped_obj folder is inside the movie_recommender folder |
| `Movie not found` error | The title must exactly match a value in `movie_data_for_app.csv` — use the autocomplete |
| Posters not loading | Check your TMDB API key; posters are optional and cards still work without them |
| Port already in use | `python app.py` uses port 5000 by default; change with `app.run(port=8080)` |
