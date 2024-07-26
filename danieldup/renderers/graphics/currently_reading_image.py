from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from danieldup.schemas.Book import Book
from danieldup.renderers.render_utils import ColorSchemeInstance, wrap_text

font_file = "MonaspaceKrypton-Regular.otf"


def create_image(book: Book, color_scheme: ColorSchemeInstance, filename: str):
    background, foreground = color_scheme.background, color_scheme.foreground
    # Create a new image with white background
    img = Image.new("RGB", (800, 600), color=background)
    d = ImageDraw.Draw(img)

    # Load fonts
    title_font = ImageFont.truetype(font_file, 36)
    author_font = ImageFont.truetype(font_file, 24)
    info_font = ImageFont.truetype(font_file, 18)

    # Download and paste book cover
    cover_response = requests.get(book.cover_url)
    cover_img = Image.open(BytesIO(cover_response.content))
    cover_img = cover_img.resize((300, 450))  # Resize cover to fit
    img.paste(cover_img, (50, 75))

    # Add text
    d.text(
        (400, 50),
        "Currently Reading",
        font=title_font,
        fill=foreground,
    )

    # Wrap and draw title
    title_lines = wrap_text(book.title, author_font, 350)
    title_height = sum(author_font.getbbox(line)[3] for line in title_lines)
    title_y = 100
    for line in title_lines:
        d.text((400, title_y), line, font=author_font, fill=foreground)
        title_y += author_font.getbbox(line)[3]

    # Wrap and draw authors
    authors_text = f"by {', '.join(book.author_names)}"
    author_lines = wrap_text(authors_text, info_font, 350)
    author_y = title_y + 20
    for line in author_lines:
        d.text((400, author_y), line, font=info_font, fill=foreground)
        author_y += info_font.getbbox(line)[3]

    # Add publication year
    d.text(
        (400, author_y + 20),
        f"First published: {book.first_publish_year}",
        font=info_font,
        fill=foreground,
    )

    # Save the image
    img.save(filename)
    print(f"Image saved as {filename}")
