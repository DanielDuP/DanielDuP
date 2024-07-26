from danieldup.renderers.charts.chart_types.stack_plot import render_stack_plot
from danieldup.renderers.render_utils import (
    ColorScheme,
    get_date_range_of_repos,
    proportional_count_repos_by_quality_over_time,
)
from typing import List, Dict
from danieldup.schemas.Repo import Repo

PROPORTION_OF_BACKEND_TO_FRONTEND = 0.4


def render_area_proportion(repos: List[Repo]):
    raw_count = proportional_count_repos_by_quality_over_time(
        repos, lambda repo: repo.areas
    )
    final_count = reallocate_counts(raw_count)
    render_stack_plot(
        final_count,
        get_date_range_of_repos(repos),
        ColorScheme.DARK_MODE.value,
        "./media/repo_areas_dark_mode.png",
    )
    render_stack_plot(
        final_count,
        get_date_range_of_repos(repos),
        ColorScheme.LIGHT_MODE.value,
        "./media/repo_areas_light_mode.png",
    )


def reallocate_counts(count: Dict[str, List[float]]) -> Dict[str, List[float]]:
    if not count.get("Full Stack"):
        return count
    for i, day in enumerate(count["Full Stack"]):
        count["Backend"][i] += day * PROPORTION_OF_BACKEND_TO_FRONTEND
        count["Frontend"][i] += day - day * PROPORTION_OF_BACKEND_TO_FRONTEND
    del count["Full Stack"]
    return count
