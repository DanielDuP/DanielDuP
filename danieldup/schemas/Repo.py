from pydantic import BaseModel, Field, computed_field
from functools import cached_property
from typing import List, Optional
from datetime import datetime
import requests
from os import environ


def github_headers():
    return {
        "Authorization": f"token {environ.get('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


# get the repos themselves into a list
class Repo(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    language: Optional[str] = None
    created_at: datetime
    pushed_at: datetime
    updated_at: datetime

    @computed_field
    @cached_property
    def languages(self) -> List[str]:
        url = f"{environ.get('GITHUB_API_URL')}/repos/{self.full_name}/languages"
        response = requests.get(url, headers=github_headers())
        response.raise_for_status()
        # I mean, are they really programming languages, per se?
        filter_list = ["HTML"]
        return [
            map_language(lang)
            for lang in list(response.json().keys())
            if lang not in filter_list
        ]

    @computed_field
    @cached_property
    def areas(self) -> List[str]:
        return [map_segments(language) for language in self.languages]

    @computed_field
    @cached_property
    def first_commit(self) -> datetime:
        url = f"{environ.get('GITHUB_API_URL')}/repos/{self.full_name}/commits"
        params = {"per_page": 1, "page": 1}
        response = requests.get(url, headers=github_headers(), params=params)
        response.raise_for_status()
        commits = response.json()
        if commits:
            return datetime.fromisoformat(
                commits[0]["commit"]["author"]["date"].rstrip("Z")
            ).replace(tzinfo=None)
        return self.created_at.replace(tzinfo=None)


def map_language(lang: str) -> str:
    language_map = {
        "vue": "TypeScript",
        "react": "TypeScript",
        # Add more mappings here as needed
    }
    return language_map.get(lang.lower(), lang)


def map_segments(lang: str) -> str:
    default = "Backend"
    language_map = {
        "vue": "Frontend",
        "scss": "Frontend",
        "typescript": "Full Stack",
        "html": "Frontend",
        "css": "Frontend",
        "javascript": "Full Stack",
        "c": "System Level",
        "zig": "System Level",
        "rust": "System Level",
        "cmake": "System Level",
        "makefile": "System Level",
        "latex": "DevOps/ML/Other",
        "tex": "DevOps/ML/Other",
        "rich text format": "DevOps/ML/Other",
        "jupyter notebook": "DevOps/ML/Other",
        "procfile": "DevOps/ML/Other",
        "dockerfile": "DevOps/ML/Other",
        "shell": "DevOps/ML/Other",
        # Add more mappings here as needed
    }
    return language_map.get(lang.lower(), default)
