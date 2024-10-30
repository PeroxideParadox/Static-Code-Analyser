import os
from utils.github_helper import fetch_repositories, download_code_sample

def main():
    query = "language:python"
    max_repos = 50
    fetched_repos_log = "dataset/fetched_repos.log"
    os.makedirs("dataset/raw_code_samples", exist_ok=True)

    # Load already fetched repositories to avoid duplicates
    if os.path.exists(fetched_repos_log):
        with open(fetched_repos_log, "r") as log_file:
            fetched_repos = set(log_file.read().splitlines())
    else:
        fetched_repos = set()

    repo_list = fetch_repositories(query, max_repos)
    
    # Fetch only unique repositories
    for repo in repo_list:
        if repo['name'] in fetched_repos:
            continue  # Skip already fetched repos

        code_sample = download_code_sample(repo['contents_url'])
        if code_sample:
            path = os.path.join("dataset", "raw_code_samples", f"{repo['name']}.py")
            with open(path, "w") as f:
                f.write(code_sample)
            
            # Log fetched repository
            with open(fetched_repos_log, "a") as log_file:
                log_file.write(f"{repo['name']}\n")

if __name__ == "__main__":
    main()
