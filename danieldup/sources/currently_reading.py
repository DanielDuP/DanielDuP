import requests
from danieldup.schemas.Book import Book
import os


def get_currently_reading() -> Book:
    response = requests.get(_currently_reading_url(os.environ["OPEN_LIB_USERNAME"]))
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    return Book(**data.get("reading_log_entries")[0].get("work"))


def _currently_reading_url(username: str) -> str:
    return f"https://openlibrary.org/people/{username}/books/currently-reading.json"
