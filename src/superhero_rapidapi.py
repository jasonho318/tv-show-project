import os
import requests
import json
from typing import List, Dict

RAPIDAPI_KEY = "06ec84f68bmsh9054e4d76b848f7p1add96jsna4eeb88e1ebf"
RAPIDAPI_HOST = 'movies-ratings2.p.rapidapi.com'
BASE_URL = 'https://movies-ratings2.p.rapidapi.com'

HEADERS = {
    'X-RapidAPI-Key': RAPIDAPI_KEY,
    'X-RapidAPI-Host': RAPIDAPI_HOST
}

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
    "jupiter's legacy", 'the gifted', 'powers', 'misfits', 'heroes', 'chronicle'
]

def fetch_superhero_titles(keywords: List[str], max_results_per_keyword: int = 100) -> List[Dict]:
    all_results = {}
    for keyword in keywords:
        params = {"query": keyword, "limit": max_results_per_keyword}
        response = requests.get(f"{BASE_URL}/search", headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('results', []):
                unique_key = (item.get('title', '').lower(), item.get('year', ''))
                if unique_key not in all_results:
                    all_results[unique_key] = item
        else:
            print(f"Error fetching '{keyword}': {response.status_code} - {response.text}")
    return list(all_results.values())

def filter_superhero_results(results: List[Dict]) -> List[Dict]:
    filtered = []
    for item in results:
        title = item.get('title', '').lower()
        description = item.get('description', '').lower()
        media_type = item.get('type', '').lower()
        if any(kw in title or kw in description for kw in SUPERHERO_KEYWORDS):
            if media_type in ['movie', 'tv', 'series', 'miniseries']:
                filtered.append(item)
    return filtered

def save_results(results: List[Dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(results)} results to {path}")

def main():
    print("Fetching superhero movies and TV shows from RapidAPI...")
    raw_results = fetch_superhero_titles(SUPERHERO_KEYWORDS)
    print(f"Fetched {len(raw_results)} raw results.")
    filtered_results = filter_superhero_results(raw_results)
    print(f"Filtered down to {len(filtered_results)} relevant superhero movies and TV shows.")
    save_results(filtered_results, 'data/raw/superhero_rapidapi.json')

if __name__ == "__main__":
    main()