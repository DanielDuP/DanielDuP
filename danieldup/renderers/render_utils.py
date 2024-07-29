from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any, Union, List, Dict, Optional, Tuple
from typing_extensions import DefaultDict
from danieldup.schemas.Repo import Repo
from datetime import datetime, timedelta
from collections import defaultdict

COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (13, 17, 23)


def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    i = 0
    while i < len(words):
        line = ""
        while i < len(words) and font.getbbox(line + words[i])[2] <= max_width:
            line = line + words[i] + " "
            i += 1
        if not line:
            line = words[i]
            i += 1
        lines.append(line.strip())
    return lines


@dataclass
class ColorSchemeInstance:
    background: Tuple[int, int, int]
    foreground: Tuple[int, int, int]

    @property
    def background_f(self) -> Tuple[float, float, float, float]:
        return tuple(float(c) / 255.0 for c in self.background)

    @property
    def foreground_f(self) -> Tuple[float, float, float, float]:
        return tuple(c / 255 for c in self.foreground)


class ColorScheme(Enum):
    LIGHT_MODE = ColorSchemeInstance(COLOR_WHITE, COLOR_GREY)
    DARK_MODE = ColorSchemeInstance(COLOR_GREY, COLOR_WHITE)


def get_date_range_of_repos(repos: list[Repo]) -> list[datetime]:
    sorted_repos = sorted(repos, key=lambda x: x.first_commit)
    start_date = sorted_repos[0].first_commit
    end_date = datetime.now()
    date_range = [
        start_date + timedelta(days=x)
        for x in range((end_date - start_date.replace(tzinfo=None)).days + 1)
    ]
    return date_range


def count_repos_by_quality_over_time(
    repos: List[Repo],
    extractor: Callable[[Repo], Union[Any, List[Any]]],
    top_n: Optional[int] = None,
) -> dict[str, List[int]]:
    date_range = get_date_range_of_repos(repos)
    quality_counts = defaultdict(lambda: [0] * len(date_range))
    for repo in repos:
        repo_start_index = (repo.first_commit - date_range[0]).days
        qualities = set(extractor(repo))
        for quality in qualities:
            for i in range(repo_start_index, len(date_range)):
                quality_counts[quality][i] += 1
    sorted_qualities = sorted(
        quality_counts.items(), key=lambda x: x[-1][-1], reverse=True
    )
    top_qualities = {quality: counts for (quality, counts) in sorted_qualities[0:top_n]}
    if top_n and len(sorted_qualities) > top_n:
        other = dict(sorted_qualities[top_n:])
        top_qualities["Other"] = [sum(counts) for counts in zip(*other.values())]
    return top_qualities


def proportional_count_repos_by_quality_over_time(
    repos: List[Repo],
    extractor: Callable[[Repo], Union[Any, List[Any]]],
    top_n: Optional[int] = None,
) -> dict[str, List[float]]:
    date_range = get_date_range_of_repos(repos)
    absolute_counts = count_repos_by_quality_over_time(repos, extractor, top_n)
    totals = [sum(counts) for counts in zip(*absolute_counts.values())]
    percentages = {
        lang: [
            absolute_counts[lang][i] / totals[i] if totals[i] != 0 else 0
            for i, _ in enumerate(date_range)
        ]
        for lang in absolute_counts.keys()
    }
    return percentages


def proportional_count_repos_in_category_over_time(
    repos: List[Repo],
    extractor: Callable[[Repo], Union[Any, List[Any]]],
    categories: Dict[str, List[str]],
    default: str,
) -> dict[str, List[float]]:
    date_range = get_date_range_of_repos(repos)
    percentage_counts = proportional_count_repos_by_quality_over_time(repos, extractor)
    del percentage_counts["total"]
    quality_counts: DefaultDict[str, List[float]] = defaultdict(
        lambda: [0] * len(date_range)
    )
    for category in categories:
        for member in categories[category]:
            if percentage_counts[member]:
                quality_counts[category] += percentage_counts[member]
    return quality_counts
