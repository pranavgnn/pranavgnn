#!/usr/bin/env python3
import os
import re
from datetime import datetime
from github import Github

REPO_URLS = [
    "https://github.com/Finova-MIT/finova-website",
    "https://github.com/pranavgnn/lyrics-video-maker",
    "https://github.com/pranavgnn/mutualfunds-calc"
]

github_token = os.environ.get('GH_TOKEN')
g = Github(github_token)

def get_repo_details(repo_url):
    parts = repo_url.strip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    
    try:
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        details = {
            'name': repo.name,
            'full_name': repo.full_name,
            'description': repo.description,
            'stars': repo.stargazers_count,
            'watchers': repo.watchers_count,
            'forks': repo.forks_count,
            'url': repo_url,
            'homepage': repo.homepage,
            'language': repo.language,
            'last_updated': repo.updated_at.strftime('%Y-%m-%d')
        }
        return details
    except Exception as e:
        print(f"Error fetching details for {repo_url}: {e}")
        return None

def create_project_html():
    repos = []
    for url in REPO_URLS:
        repo_details = get_repo_details(url)
        if repo_details:
            repos.append(repo_details)
    
    html = '<div align="center">\n  <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">\n'
    
    for repo in repos:
        homepage_link = f" • <a href=\"{repo['homepage']}\">Live Demo</a>" if repo['homepage'] else ""
        
        html += f'''    <div style="border: 1px solid #30363d; border-radius: 6px; padding: 16px; text-align: left;">
      <h3>📂 <a href="{repo['url']}">{repo['name']}</a></h3>
      <p>{repo['description'] or 'No description available.'}</p>
      <p><strong>Tech:</strong> {repo['language'] or 'Not specified'}</p>
      <p>
        <span>⭐ {repo['stars']}</span> • 
        <span>👀 {repo['watchers']}</span> • 
        <span>🔄 {repo['forks']}</span>{homepage_link}
      </p>
      <small>Last updated: {repo['last_updated']}</small>
    </div>\n'''
    
    html += '  </div>\n</div>'
    
    # Add timestamp
    utc_time = datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    html += f'\n\n<div align="center"><small><i>Automatically updated on {utc_time} UTC</i></small></div>'
    
    return html

def update_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()

        start_pattern = r'## Projects\s+<div align="center">\s+<img src="commands/cat_projects\.svg" alt="Command: cat projects\.md">\s+</div>\s+'
        end_pattern = r'```txt[\s\S]*?```'

        pattern = start_pattern + end_pattern
        new_content = re.sub(pattern, f"## Projects\n\n<div align=\"center\">\n  <img src=\"commands/cat_projects.svg\" alt=\"Command: cat projects.md\">\n</div>\n\n{create_project_html()}", content)
        
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print("README.md has been updated successfully with the latest repository details.")
    except Exception as e:
        print(f"Error updating README.md: {e}")

if __name__ == "__main__":
    update_readme()