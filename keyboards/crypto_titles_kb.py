from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicons.lexicons import LEXICON


#клавиатура выбора команды шифрования/дешифрования
#создаем кнопки
button_1 = KeyboardButton(text=LEXICON['Encrypt'])
button_2 = KeyboardButton(text=LEXICON['Decrypt'])

komanda_kb = ReplyKeyboardMarkup(
    keyboard=[[button_1],
              [button_2]],
    one_time_keyboard=True,
    resize_keyboard=True
)

#клавиатура выбора Шифра для Зашифровывания
#создаем кнопки
button_1 = KeyboardButton(text=LEXICON['en_caesar'])
button_2 = KeyboardButton(text=LEXICON['en_crypt_key'])
button_3 = KeyboardButton(text=LEXICON['en_vigener'])

encrypt_kb = ReplyKeyboardMarkup(
    keyboard=[[button_1],
              [button_2],
              [button_3]],
    one_time_keyboard=False,
    resize_keyboard=True
)

#клавиатура выбора Шифра для Расшифровывания
#создаем кнопки
button_1 = KeyboardButton(text=LEXICON['de_caesar'])
button_2 = KeyboardButton(text=LEXICON['de_crypt_key'])
button_3 = KeyboardButton(text=LEXICON['de_vigener'])

decrypt_kb = ReplyKeyboardMarkup(
    keyboard=[[button_1],
              [button_2],
              [button_3]],
    one_time_keyboard=False,
    resize_keyboard=True
)


# Функция, генерирующая клавиатуру для выбора вида ключа
def create_key_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    #Инициализируем билдер. Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    #Наполняем клавиатуру кнопками
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['key_know'],
            callback_data='key_know'
        ),
        InlineKeyboardButton(
            text=LEXICON['random_key'],
            callback_data='random_key'
        ),
        width=2
    )
    return kb_builder.as_markup()