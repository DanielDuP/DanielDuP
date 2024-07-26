import requests
import os
from danieldup.schemas.Repo import github_headers, Repo
from typing import List


def get_repos() -> List[Repo]:
    url = f"{os.environ.get('GITHUB_API_URL')}/user/repos"
    params = {"per_page": 100, "page": 1}
    response = requests.get(url, headers=github_headers(), params=params)
    response.raise_for_status()
    return [Repo(**repo) for repo in response.json()]
