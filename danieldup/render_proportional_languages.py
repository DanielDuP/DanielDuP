from danieldup.sources.repos import get_repos
from danieldup.renderers.charts.repo_language_proportion import (
    render_language_proportion,
)
from danieldup.renderers.charts.repo_area_proportion import render_area_proportion


def render():
    repos = get_repos()
    render_language_proportion(repos)
    render_area_proportion(repos)
