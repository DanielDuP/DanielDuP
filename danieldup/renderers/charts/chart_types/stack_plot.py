from typing import List, Union
from datetime import datetime
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import matplotlib.dates as mdates

from danieldup.renderers.render_utils import ColorSchemeInstance


def render_stack_plot(
    values: dict[str, List[Union[int, float]]],
    date_range: List[datetime],
    color_scheme: ColorSchemeInstance,
    filename: str,
):
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))

    # Prepare data for stack plot
    labels = list(values.keys())
    data = [values[label] for label in values]

    # Create color map
    cmap = plt.get_cmap("tab20")  # Using a colormap with more distinct colors
    colors = cmap(np.linspace(0, 1, len(values)))
    # Create stack plot
    ax.stackplot(
        date_range,  # List[datetime]
        data,
        labels=labels,
        colors=colors,
        edgecolor="none",
    )
    format_colors(fig, ax, color_scheme)
    format_axes(ax, date_range[0], date_range[-1])

    # Adjust layout
    plt.tight_layout()

    plt.savefig(filename)


def format_axes(ax: Axes, start_date, end_date):
    # Customize plot
    # ax.set_title('Language Composition Over Time', fontsize=16, pad=20)

    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())

    # Set axis limits to match data exactly
    ax.set_xlim(start_date, end_date)
    ax.set_ylim(0, 1)
    # Format y-axis
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y*100:.0f}%"))

    # Add legend
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)

    # Add grid
    ax.grid(axis="y", linestyle="--", alpha=0.7)


def format_colors(fig: Figure, ax: Axes, color_scheme: ColorSchemeInstance):
    # Customize colors
    background_color = color_scheme.background_f
    text_color = color_scheme.foreground_f
    line_color = color_scheme.foreground_f

    # Set background color
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Set text color for title, labels, and ticks
    ax.set_ylabel("Percentage of Repositories", fontsize=12, color=text_color)
    ax.tick_params(colors=text_color)

    # Set line colors
    ax.spines["bottom"].set_color(line_color)
    ax.spines["top"].set_color(line_color)
    ax.spines["left"].set_color(line_color)
    ax.spines["right"].set_color(line_color)

    # Customize legend
    legend = ax.legend()
    legend.get_frame().set_facecolor(background_color)
    for text in legend.get_texts():
        text.set_color(text_color)
