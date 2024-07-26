from danieldup.renderers.render_utils import ColorScheme
from danieldup.sources.currently_reading import get_currently_reading
from danieldup.renderers.graphics.currently_reading_image import create_image


def render():
    currently_reading = get_currently_reading()
    create_image(
        currently_reading,
        ColorScheme.LIGHT_MODE.value,
        "./media/currently_reading_light_mode.png",
    )
    create_image(
        currently_reading,
        ColorScheme.DARK_MODE.value,
        "./media/currently_reading_dark_mode.png",
    )
