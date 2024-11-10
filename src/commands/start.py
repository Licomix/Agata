from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router(name=__name__)

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я Агата созданная для FrogseryLab! \n\nФыр-фыр-фыр")
