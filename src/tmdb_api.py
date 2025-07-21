import os
import requests
from dotenv import load_dotenv
import json

# Load API key from .env
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = 'https://api.themoviedb.org/3'

HEADERS = {
    'Authorization': f'Bearer {TMDB_API_KEY}',
    'Content-Type': 'application/json;charset=utf-8'
}

def fetch_superhero_shows_movies(query='superhero', media_type='tv', max_pages=2, cache_path='data/raw/superhero_tmdb.json'):
    """
    Fetches TV shows or movies from TMDb matching the query (e.g., 'superhero').
    Caches results to a local JSON file.
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
    # Cache to file
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Fetched and cached {len(results)} results to {cache_path}")
    return results

if __name__ == "__main__":
    fetch_superhero_shows_movies()