from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def create_history_keyboard(history):
    kb_builder = InlineKeyboardBuilder()

    for stroka in history:
        kb_builder.row(InlineKeyboardButton(
            text=str(stroka[4]),
            callback_data=str(stroka[0])
        ))

    return kb_builder.as_markup()