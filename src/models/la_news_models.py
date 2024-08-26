"""Model python file for class News"""
from dataclasses import dataclass
import re

@dataclass
class News:
    """Dataclass News"""
    title: str
    date: str
    description: str
    phrase_count: int
    money: bool
    image: str

    def __init__(self, title, date, search_phrase, description, image) -> None:
        self.title = title
        self.date = date
        self.description = description
        title_count = self.count_occurrences(self.title, search_phrase)
        description_count = self.count_occurrences(self.description, search_phrase)
        self.phrase_count = title_count + description_count
        self.image = image
        self.money= self.contains_currency_format(title)


    def count_occurrences(self, text: str, phrase: str) -> int:
        """count of search phrases in a string"""
        return text.count(phrase) if text else 0

    def contains_currency_format(self, text: str) -> bool:
        """
        Returns True if the string contains any of the specified currency formats.
        Possible formats:
        - $11.1
        - $111,111.11
        - 11 dollars
        - 11 USD
        """
        pattern = re.compile(r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+\s*dollars|\d+\s*USD')
        return bool(pattern.search(text))
