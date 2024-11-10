from difflib import SequenceMatcher

from aiogram.filters.base import Filter
from aiogram.types import Message

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class FyrrFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        target_phrase = "фыррр"
        similarity_threshold = 0.6

        if similar(message.text.lower(), target_phrase.lower()) > similarity_threshold:
            return True
        else:
            return False
