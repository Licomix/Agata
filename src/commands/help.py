import random

import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.filters.fyr import FyrrFilter

router = Router(name=__name__)

fyr_phrases = [
    'Фыр-фыр-фыр',
    'Фря',
    'Фыррррр',
    'Фррр... Фррр... ',
]

@router.message(Command('help'))
async def top_cmd(message: Message):
    reply = """Вот список доступных вам команд команд:\n
        <i>/start</i> - Приветственное сообщение: фыр-фыр-фыр!\n
        <i>/help</i> - Получить справку о доступных командах!\n
        <i>/top</i> - Отобразит таблицу лидеров по количеству сообщений!\n
        <i>Фыррр</i> - Просто фыррр..."""
    await message.reply(reply)

@router.message(FyrrFilter())
async def fyrrr(message: Message):
    if message.from_user.is_bot:
        return

    image_url = await get_random_fox_image()
    return_phrase = random.choice(fyr_phrases)

    await message.reply_photo(caption=return_phrase, photo=image_url)

async def get_random_fox_image():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://randomfox.ca/floof/') as resp:
            data = await resp.json()
            image_url = data['image']
    return image_url
