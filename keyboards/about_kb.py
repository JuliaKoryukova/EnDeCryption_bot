from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicons.lexicons import LEXICON


# Функция, генерирующая клавиатуру для about
def create_about_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    #Инициализируем билдер. Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    #Наполняем клавиатуру кнопками
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['about_caesar_button'],
            callback_data='about_caesar_button'
        ),
        InlineKeyboardButton(
            text=LEXICON['about_crypt_key_button'],
            callback_data='about_crypt_key_button'
        ),
        InlineKeyboardButton(
            text=LEXICON['about_vigener_button'],
            callback_data='about_vigener_button'
        ),
        width=2
    )
    return kb_builder.as_markup()