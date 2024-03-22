from aiogram import Router
from aiogram.types import Message
from lexicons.lexicons import LEXICON

router = Router()

#Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON['other_answer'])