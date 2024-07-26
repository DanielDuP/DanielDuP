from pydantic import BaseModel, Field, computed_field
from typing import List


class Book(BaseModel):
    title: str
    author_names: List[str]
    first_publish_year: int
    cover_id: int

    @computed_field
    @property
    def cover_url(self) -> str:
        return f"https://covers.openlibrary.org/b/id/{str(self.cover_id)}-L.jpg"
