import os
import requests
from dotenv import load_dotenv
import json
from collections import defaultdict

# Load API key from .env
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'

HEADERS = {
    'Authorization': f'Bearer {TMDB_API_KEY}',
    'Content-Type': 'application/json;charset=utf-8'
}

# List of superhero-related keywords/franchises
SUPERHERO_KEYWORDS = [
    'superhero', 'marvel', 'dc', 'avengers', 'x-men', 'spider-man', 'batman', 'superman',
    'wonder woman', 'iron man', 'captain america', 'thor', 'hulk', 'flash', 'arrow',
    'guardians of the galaxy', 'black panther', 'deadpool', 'daredevil', 'luke cage',
    'jessica jones', 'punisher', 'ant-man', 'shazam', 'aquaman', 'suicide squad',
    'justice league', 'teen titans', 'legion', 'the boys', 'invincible', 'watchmen',
    'kick-ass', 'fantastic four', 'doctor strange', 'wolverine', 'catwoman', 'venom',
    'blade', 'ghost rider', 'green lantern', 'supergirl', 'batwoman', 'black widow',
    'eternals', 'moon knight', 'ms. marvel', 'hawkeye', 'peacemaker', 'star girl',
    'doom patrol', 'runaways', 'cloak & dagger', 'the tick', 'umbrella academy',
    'jupiter\'s legacy', 'the gifted', 'powers', 'misfits', 'heroes', 'chronicle'
]

# TMDb genre IDs for relevant genres (as of 2024)
RELEVANT_GENRE_IDS = set([
    28,   # Action
    12,   # Adventure
    14,   # Fantasy
    878,  # Science Fiction
])

def fetch_tmdb(query, media_type, max_pages=2):
    """
    Fetches TV shows or movies from TMDb matching the query.
    """
    results = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/search/{media_type}?query={query}&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            results.extend(data.get('results', []))
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break
    return results

def is_superhero_result(result):
    """
    Returns True if the result is likely a superhero show/movie based on keywords and genres.
    """
    title = result.get('title') or result.get('name') or ''
    overview = result.get('overview', '')
    genres = set(result.get('genre_ids', []))
    text = f"{title} {overview}".lower()
    # Must match at least one keyword
    keyword_match = any(kw in text for kw in SUPERHERO_KEYWORDS)
    # Should have at least one relevant genre
    genre_match = bool(genres & RELEVANT_GENRE_IDS)
    return keyword_match and genre_match

def fetch_superhero_shows_movies(keywords=SUPERHERO_KEYWORDS, max_pages=2, cache_path='data/raw/superhero_tmdb.json'):
    """
    Fetches both TV shows and movies from TMDb matching superhero-related keywords.
    Caches results to a local JSON file.
    """
    all_results = defaultdict(dict)
    for media_type in ['tv', 'movie']:
        for keyword in keywords:
            results = fetch_tmdb(keyword, media_type, max_pages=max_pages)
            for result in results:
                tmdb_id = (result.get('id'), media_type)
                # Avoid duplicates by TMDb ID and media type
                if tmdb_id not in all_results:
                    if is_superhero_result(result):
                        all_results[tmdb_id] = result
    # Convert to list
    filtered_results = list(all_results.values())
    # Cache to file
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_results, f, ensure_ascii=False, indent=2)
    print(f"Fetched and cached {len(filtered_results)} results to {cache_path}")
    return filtered_results

if __name__ == "__main__":
    fetch_superhero_shows_movies()