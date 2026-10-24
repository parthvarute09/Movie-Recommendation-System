from concurrent.futures import ThreadPoolExecutor
from utils.tmdb import fetch_poster

def give_recommendations(title, data, dataframe, sig, api_key):
    if title not in data['original_title'].values:
        return []

    idx = data[data['original_title'] == title].index[0]
    sig_scores = sorted(list(enumerate(sig[idx])), key=lambda x: x[1], reverse=True)[1:11]
    indices = [i[0] for i in sig_scores]

    cols = ['original_title', 'vote_average', 'genres', 'overview']
    cols = [c for c in cols if c in dataframe.columns]
    recs = dataframe.iloc[indices][cols].to_dict('records')

    # Fetch posters in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        posters = list(executor.map(lambda x: fetch_poster(x['original_title'], api_key), recs))

    for i in range(len(recs)):
        recs[i]['poster'] = posters[i]

    return recs