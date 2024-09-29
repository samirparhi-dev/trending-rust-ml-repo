import requests
import pandas as pd
import numpy as np

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

# Replace this with your personal access token
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"

# Function to search GitHub repositories based on a query
def search_github_repositories(query, language="Rust"):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    params = {
        'q': query + f' language:{language}',
        'per_page': 100
    }

    response = requests.get(f"{GITHUB_API_URL}/search/repositories", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repositories: {response.status_code}")
        return None

# Function to get language details of a repository
def get_repo_languages(repo_full_name):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(f"{GITHUB_API_URL}/repos/{repo_full_name}/languages", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching languages for {repo_full_name}: {response.status_code}")
        return None

# Function to filter repositories where Rust code is more than 90%
def filter_rust_dominant_repos(repositories):
    rust_dominant_repos = []

    for repo in repositories['items']:
        repo_name = repo['full_name']
        languages = get_repo_languages(repo_name)

        if languages and 'Rust' in languages:
            total_bytes = sum(languages.values())
            rust_bytes = languages['Rust']
            rust_percentage = (rust_bytes / total_bytes) * 100

            if rust_percentage > 90:
                rust_dominant_repos.append({
                    'name': repo_name,
                    'url': repo['html_url'],
                    'rust_percentage': rust_percentage
                })

    return rust_dominant_repos

# Main function to search and filter repositories
def find_ml_rust_repositories():
    query = 'machine learning'
    repositories = search_github_repositories(query)

    if repositories:
        rust_dominant_repos = filter_rust_dominant_repos(repositories)
        return rust_dominant_repos
    else:
        return []

# Get the repositories and convert to DataFrame
rust_repos = find_ml_rust_repositories()

if rust_repos:
    df = pd.DataFrame(rust_repos)
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv("ml_rust_repositories.csv", index=False)
    print("CSV file created: ml_rust_repositories.csv")
else:
    print("No repositories found with more than 90% Rust code.")
