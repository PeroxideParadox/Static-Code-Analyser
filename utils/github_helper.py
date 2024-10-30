import requests
from config import TOKEN  

def fetch_repositories(query, max_repos):
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {TOKEN}"}
    params = {"q": query, "sort": "stars", "per_page": min(max_repos, 100)}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("items", [])

def download_code_sample(contents_url):
    contents_url = contents_url.replace("{+path}", "")
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(contents_url, headers=headers)
    return response.text if response.ok else None
