from danieldup.renderers.charts.chart_types.stack_plot import render_stack_plot
from danieldup.renderers.render_utils import (
    ColorScheme,
    get_date_range_of_repos,
    proportional_count_repos_by_quality_over_time,
)
from typing import List
from danieldup.schemas.Repo import Repo


def render_language_proportion(repos: List[Repo]):
    count = proportional_count_repos_by_quality_over_time(
        repos, lambda repo: repo.languages, 7
    )
    render_stack_plot(
        count,
        get_date_range_of_repos(repos),
        ColorScheme.DARK_MODE.value,
        "./media/repo_languages_dark_mode.png",
    )
    render_stack_plot(
        count,
        get_date_range_of_repos(repos),
        ColorScheme.LIGHT_MODE.value,
        "./media/repo_languages_light_mode.png",
    )
