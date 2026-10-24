# 🎬 Movie Recommendation System

A Machine Learning and Natural Language Processing (NLP) project that recommends movies similar to a user's selected movie. The system analyzes movie descriptions, calculates similarity scores, and returns the top 10 most similar movies.

Built using Python, Pandas, Scikit-learn, and the TMDB 5000 Movie Dataset, this project demonstrates data preprocessing, exploratory data analysis, recommendation algorithms, and web application development.

## 📌 Project Overview

Finding movies that match personal interests can be time-consuming. This project addresses that problem using a **content-based movie recommendation system**.

The model processes movie overviews using TF-IDF vectorization and calculates similarity using the Sigmoid Kernel. When a user selects a movie, the system ranks other movies by similarity and displays the top 10 recommendations.

The project also explores weighted-average ratings and popularity-based ranking to understand different recommendation approaches.

## ✨ Features

- 🎥 **Movie Recommendations:** Suggests the top 10 similar movies.
- 🧠 **Content-Based Filtering:** Uses movie descriptions to identify similar content.
- 📝 **TF-IDF Vectorization:** Converts textual movie overviews into numerical features.
- 📊 **Similarity Scoring:** Uses the Sigmoid Kernel to calculate similarity between movies.
- ⭐ **Movie Ratings:** Displays available ratings and related movie information.
- 🖼️ **Movie Posters:** The Flask application can fetch movie posters using the TMDB API.
- 🔎 **Movie Search:** Supports movie selection and search functionality.
- 🌐 **Web Interface:** Includes Streamlit and Flask application implementations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and preprocessing |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Exploratory data analysis |
| Scikit-learn | TF-IDF vectorization and similarity calculation |
| Joblib | Saving and loading model artifacts |
| Streamlit | Interactive recommendation interface |
| Flask | Web application and search endpoints |
| Requests | Fetching movie poster information |
| TMDB API | Movie poster and movie information lookup |
| Jupyter Notebook | Model development and experimentation |

## 📂 Dataset

This project uses the **TMDB 5000 Movie Dataset**, consisting of two CSV files.

1. `tmdb_5000_movies.csv`
   - Movie title and overview
   - Genres and keywords
   - Popularity
   - Vote average and vote count
   - Budget, revenue, and other movie metadata

2. `tmdb_5000_credits.csv`
   - Movie ID
   - Cast information
   - Crew information

Each CSV contains 4,803 records.

The datasets are merged using the movie ID to combine movie metadata and credits.

## ⚙️ How It Works

### 1. Data Collection and Preprocessing

- Load the movie and credits datasets using Pandas.
- Rename `movie_id` to `id` in the credits dataset.
- Merge the datasets using the common movie ID.
- Remove selected unnecessary columns.
- Explore movie ratings, popularity, and other features.

### 2. Recommendation Approaches

**Weighted-Average Recommendation**

Uses movie ratings and vote counts to calculate a weighted rating, reducing the influence of movies with very few votes.

Formula:

\[
WR=\frac{vR+mC}{v+m}
\]

Where:

- \(R\) = average rating of the movie
- \(v\) = number of votes for the movie
- \(C\) = mean rating across the dataset
- \(m\) = minimum vote threshold

**Popularity-Based Recommendation**

Ranks movies according to their popularity scores.

**Hybrid Ranking Exploration**

Combines normalized weighted ratings and popularity scores:

\[
Score=0.5W_s+0.5P_s
\]

Where \(W_s\) is the scaled weighted rating and \(P_s\) is the scaled popularity score.

**Content-Based Recommendation**

The application uses the content-based approach described below to generate similar-movie recommendations.

### 3. Text Vectorization Using TF-IDF

TF-IDF converts movie overviews into numerical feature vectors.

The notebook configures `TfidfVectorizer` with:

- English stop-word removal
- N-grams ranging from 1 to 3 words
- `min_df=3`

This allows the system to represent meaningful words and phrases from movie descriptions.

### 4. Similarity Calculation

The project applies Scikit-learn's `sigmoid_kernel` to the TF-IDF feature matrix to calculate pairwise similarity scores.

The system then:

1. Identifies the selected movie.
2. Retrieves its similarity scores.
3. Sorts movies in descending order of similarity.
4. Excludes the selected movie itself.
5. Returns the top 10 recommendations.

### 5. Web Application

The project includes two application implementations:

- **Streamlit:** Provides a movie dropdown and a button to display recommended movie titles.
- **Flask:** Provides a web interface, a search endpoint, movie details, and TMDB poster lookup.

## 📁 Project Structure

```text

Movie-Recommendation-System/
│
├── Movie_Recommendation.ipynb
├── Recc_system_tmdb.ipynb
├── app.py
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── Static/
│   ├── main.js
│   └── style.css
│
├── Utils/
│   ├── recommender
│   └── tmdb
│
├── templates/
│   └── index.html
│
└── dumped_obj/
    ├── movie_data_for_app.csv
    ├── movie_dataframe_for_app.csv
    ├── tfidf_vectorizer.pkl
    └── sigmoid_kernel.pkl

```

**Note:** The `dumped_obj/` files are generated by the notebooks and are required by the application code. The Flask version also expects the `templates/index.html` file. Ensure these files exist before running the corresponding application.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or another compatible Python version
- Git
- pip
- Jupyter Notebook (optional, for model development)

### Step 1: Clone the Repository

```bash
git clone https://github.com/parthvarute09/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

Create a `requirements.txt` file containing:

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
joblib
streamlit
flask
requests
python-dotenv
jupyter
```

Install the packages:

```bash
python -m pip install -r requirements.txt
```

### Step 4: Prepare the Model Files

Open `Recc_system_tmdb.ipynb` or `Movie_Recommendation.ipynb` in Jupyter Notebook.

Run the notebook cells to:

1. Load and preprocess the datasets.
2. Build the TF-IDF feature matrix.
3. Calculate similarity scores.
4. Save the processed movie CSV files.
5. Save the model artifacts using Joblib.

Place the generated files in the `dumped_obj/` directory.

**Important:** Update the notebook's output paths to a relative project path instead of the original machine-specific Windows paths.

### Step 5: Configure the TMDB API Key

The Flask application uses the TMDB API to fetch movie posters. If you want this feature, obtain your own API key from [The Movie Database](https://www.themoviedb.org/).

Create a `.env` file in the project root:

```text
TMDB_API_KEY=your_tmdb_api_key_here
```

Load the environment variable in `app.py` using `python-dotenv` or configure it in your terminal. Do not commit `.env` or expose your API key in public repositories.

## ▶️ Running the Application

### Option 1: Streamlit Application

Ensure the model files exist and update the hardcoded `file_path` in `Movie_app.py` to point to your project's `dumped_obj/` directory.

Run:

```bash
streamlit run Movie_app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

Select a movie and click **Get recommendations**.

### Option 2: Flask Application

Ensure `dumped_obj/` and `templates/index.html` are available, then configure the TMDB API key if poster fetching is required.

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The Flask application also exposes a `/search?q=` endpoint for movie-title search suggestions.

## 📊 Example

**Selected movie:** The Avengers

**Expected output:** A list of up to 10 movies ranked by their calculated similarity to the selected movie.

The exact recommendations depend on the processed dataset and the similarity scores generated by the model.

## 🔮 Future Improvements

- Add genre, cast, director, and keyword information to the content-based feature representation.
- Improve movie search with autocomplete and fuzzy matching.
- Display movie posters, ratings, release dates, and descriptions in a polished interface.
- Add user ratings and personalized recommendation history.
- Experiment with cosine similarity and other recommendation algorithms.
- Evaluate recommendation quality using appropriate ranking metrics.
- Deploy the application to a cloud platform.
- Add automated tests and reproducible model-building scripts.

## 🎓 Learning Outcomes

This project provides practical experience with:

- Data cleaning and exploratory data analysis
- Feature engineering and NLP preprocessing
- TF-IDF text vectorization
- Similarity-based recommendation algorithms
- Saving and loading machine learning artifacts
- Building interactive applications with Streamlit and Flask
- Integrating third-party APIs

## 👨‍💻 Author

**Parth Varute**

GitHub: [@parthvarute09](https://github.com/parthvarute09)

Project Repository: [Movie Recommendation System](https://github.com/parthvarute09/Movie-Recommendation-System)

## 📄 Dataset and Attribution

Dataset: [TMDB 5000 Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

Movie poster and metadata integration: [The Movie Database (TMDB)](https://www.themoviedb.org/)


---

⭐ If you find this project useful, consider starring the repository!
