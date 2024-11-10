from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command

from utils.managers.db_manager import SQLiteDatabaseManager

router = Router(name=__name__)

@router.message(Command('top'))
async def top_cmd(message: Message):
    reply_message = await get_top_users()

    await message.answer(reply_message)

@router.message(F.text)
async def top_liczymy(message: Message):
    if message.from_user.is_bot:
        return
    elif message.chat.type == "private":
        return
    elif message.text.startswith('/'):
        return
    await update_message_count(message.from_user.id, message.from_user.username)

async def update_message_count(user_id: int, username: str):
    message_count_x = 0

    async with SQLiteDatabaseManager() as cursor:
        await cursor.execute("""SELECT message_count FROM user_messages WHERE user_id = ?""", [user_id])
        message_count_x = await cursor.fetchone()

    if message_count_x:
        message_count_x = message_count_x[0]
    else:
        message_count_x = 0

    message_count_x += 1

    async with SQLiteDatabaseManager() as cursor:
        await cursor.execute('''INSERT OR REPLACE INTO user_messages (user_id, username, message_count) VALUES (?, ?, ?)''', (user_id, username, message_count_x))

async def get_top_users():
    async with SQLiteDatabaseManager() as cursor:
        await cursor.execute("""SELECT username, message_count FROM user_messages ORDER BY message_count DESC LIMIT 10""")
        top_users_list = await cursor.fetchall()

    reply_message = "Топ 10 пользователей по количеству сообщений:\n\n"
    for index, user in enumerate(top_users_list, start=1):
        username, message_count = user
        reply_message += f"{index}. {username} - {message_count} сообщений\n"

    return(reply_message)
