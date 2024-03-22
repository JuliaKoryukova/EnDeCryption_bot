import pathlib
import sqlite3
import sys

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from filters.filters import IsDigitCallbackData
from keyboards.historymarks_kb import create_history_keyboard
from keyboards.crypto_titles_kb import komanda_kb, encrypt_kb, decrypt_kb, create_key_keyboard
from keyboards.about_kb import create_about_keyboard
from lexicons.lexicons import LEXICON

from services.caesar import encrypt_caesar, decrypt_caesar
from services.with_key import encrypto_with_key, decrypto_with_key
from services.vigener import encrypto_vigener, decrypto_vigener
from services.crypto_service import get_random_number, get_random_words

router = Router()

class En_FSMFillForm(StatesGroup):
    fill_encrypt_text = State()  # Состояние ожидания ввода текста для зашифровывания
    fill_encrypt_key = State()  # Состояние ожидания ввода ключа
    fill_encrypt_key_text = State()

    fill_encrypt_text_wk = State()  # Состояние ожидания ввода текста для зашифровывания шифром с ключом
    fill_encrypt_key_wk = State()  # Состояние ожидания ввода ключа для шифра с ключом
    fill_encrypt_key_text_wk = State()

    fill_encrypt_text_vigener = State()  # Состояние ожидания ввода текста для зашифровывания шифром с ключом
    fill_encrypt_key_vigener = State()  # Состояние ожидания ввода ключа для шифра Виженера
    fill_encrypt_key_text_vigener = State()

class De_FSMFillForm(StatesGroup):
    fill_decrypt_text = State()  # Состояние ожидания ввода текста для зашифровывания
    fill_decrypt_key = State()  # Состояние ожидания ввода ключа
    fill_decrypt_key_text = State()

    fill_decrypt_text_wk = State()  # Состояние ожидания ввода текста для зашифровывания
    fill_decrypt_key_wk = State()  # Состояние ожидания ввода ключа
    fill_decrypt_key_text_wk = State()

    fill_decrypt_text_vigener = State()  # Состояние ожидания ввода текста для зашифровывания
    fill_decrypt_key_vigener = State()  # Состояние ожидания ввода ключа
    fill_decrypt_key_text_vigener = State()

class About_FSMFillForm(StatesGroup):
    fill_about = State()
    fill_about_caesar = State()
    fill_about_with_key = State()
    fill_about_vigener = State()
    fill_about_enigma = State()


# _____________ОБЫЧНЫЕ ХЭНДЛЕРЫ___________________________

#____________START______________
# Этот хэндлер будет срабатывать на команду '/start'
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=komanda_kb)

#____________HELP______________
# Этот хэндлер будет срабатывать на команду '/help'
# и отправлять пользователю сообщение с инструкцией
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


#____________ABOUT______________

# Этот хэндлер будет срабатывать на команду '/about'
# и отправлять пользователю описание шифров
@router.message(Command(commands='about'))
async def process_about_command(message: Message, state: FSMContext):
    await message.answer(LEXICON[message.text],
                         reply_markup=create_about_keyboard()
    )
    await state.set_state(About_FSMFillForm.fill_about)

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuerry c data 'about_caesar_button'
@router.callback_query(StateFilter(About_FSMFillForm.fill_about),
                       F.data == 'about_caesar_button')
async def process_about_caesar_button_press(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON['about_caesar'])

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuerry c data 'about_crypt_key_button'
@router.callback_query(StateFilter(About_FSMFillForm.fill_about),
                       F.data == 'about_crypt_key_button')
async def process_about_caesar_button_press(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON['about_crypt_key'])

# Этот хэндлер будет срабатывать на апдейт типа CallbackQuerry c data 'about_vigener_button'
@router.callback_query(StateFilter(About_FSMFillForm.fill_about),
                       F.data == 'about_vigener_button')
async def process_about_caesar_button_press(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON['about_vigener'])



# Этот хэндлер будет срабатывать на кнопку Зашифровать -
@router.message(F.text == LEXICON['Encrypt'])
async def process_encrypt_command(message: Message):
    await message.answer(LEXICON['Encrypt'], reply_markup=encrypt_kb)

# Этот хэндлер будет срабатывать на кнопку Расшифровать -
@router.message(F.text == LEXICON['Decrypt'])
async def process_decrypt_command(message: Message):
    await message.answer(LEXICON['Decrypt'], reply_markup=decrypt_kb)



# ___________________________ШИФР ЦЕЗАРЯ Зашифровать___________________________________

# Этот хэндлер будет срабатывать на кнопку Шифр Цезаря Зашифровать
@router.message(F.text == LEXICON['en_caesar'])
async def caesar_process_encrypto_button(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваш текст')
    await state.set_state(En_FSMFillForm.fill_encrypt_text)

# Этот хэндлер будет срабатывать, если введен корректный текст
@router.message(StateFilter(En_FSMFillForm.fill_encrypt_text))
async def caesar_process_text_sent(message: Message, state: FSMContext):
    LEXICON['text_to_encrypt'] = message.text
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Выберите тип ключа',
        reply_markup=create_key_keyboard()
    )
    await state.set_state(En_FSMFillForm.fill_encrypt_key)

# Этот хэндлер будет срабатывать на кнопку Заданный ключ
@router.callback_query(StateFilter(En_FSMFillForm.fill_encrypt_key),
                       F.data.in_(['key_know']))
async def caesar_process_encrypto_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Пожалуйста, введите ваш ключ')
    await state.set_state(En_FSMFillForm.fill_encrypt_key_text)

#Этот хэндлер выводит Зашифрованный текст на Заданный пользователем ключ
@router.message(StateFilter(En_FSMFillForm.fill_encrypt_key_text))
async def caesar_process_key_know_sent(message: Message):
    if message.text.isdigit():
        encrypt_caesar_text = caesar_save_encrypt_to_history(message.from_user.id, LEXICON['text_to_encrypt'], message.text)
        await message.answer(text='Исходный текст:\n' + LEXICON['text_to_encrypt'] +'\n\n' + 'Ключ: ' +  message.text + '\n\n' + 'Зашифрованный текст:\n' + encrypt_caesar_text,
                             reply_markup=komanda_kb)
    else:
        await message.answer(
            text='Ключ должен быть целым числом\n\n'
                 'Попробуйте еще раз')

# Этот хэндлер будет срабатывать на кнопку Произвольный ключ и выводить Зашифрованный текст
@router.callback_query(StateFilter(En_FSMFillForm.fill_encrypt_key),
                       F.data.in_(['random_key']))
async def caesar_process_encrypto_button(callback: CallbackQuery):
    await callback.message.delete()
    random_key = get_random_number()
    encrypt_caesar_text = caesar_save_encrypt_to_history(callback.from_user.id, LEXICON['text_to_encrypt'], random_key)
    await callback.message.answer(text='Исходный текст:\n' + LEXICON['text_to_encrypt'] +'\n\n' + 'Ключ: ' + str(random_key) + '\n\n' + 'Зашифрованный текст:\n' + encrypt_caesar_text,
                                  reply_markup=komanda_kb)

#Сохранение в базу данных
def caesar_save_encrypt_to_history(user_id, input_text, key):
    caesar_text_after = encrypt_caesar(input_text, key)
    script_dir = pathlib.Path(sys.argv[0]).parent
    db_file = script_dir / 'crypto_history.db'
    connection = sqlite3.connect(db_file)
    #connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    # cursor.execute(
    #     f'INSERT INTO History(username, text_before, text_after, crypto_method, crypto_key) '
    #     f'VALUES(\'{user_id}\', \'{input_text}\', \'{caesar_text_after}\', \'Шифр Цезаря (Encrypt)\', \'{key}\')'
    # )
    cursor.execute("""CREATE TABLE IF NOT EXISTS History(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    text_before TEXT NOT NULL,
    text_after TEXT NOT NULL,
    crypto_method TEXT NOT NULL,
    crypto_key INTEGER);""")

    connection.commit()
    cursor.close()
    connection.close()
    return caesar_text_after



# ___________________________ШИФР ЦЕЗАРЯ Расшифровать___________________________________

# Этот хэндлер будет срабатывать на кнопку Шифр Цезаря Расшифровать
@router.message(F.text == LEXICON['de_caesar'])
async def caesar_process_decrypto_button(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите зашифрованный текст')
    await state.set_state(De_FSMFillForm.fill_decrypt_text)

# Этот хэндлер будет срабатывать, если введен корректный текст и ждать ввода ключа
@router.message(StateFilter(De_FSMFillForm.fill_decrypt_text))
async def caesar_process_text_sent(message: Message, state: FSMContext):
    LEXICON['text_to_decrypt'] = message.text
    await message.answer(text='Пожалуйста, введите ключ')
    await state.set_state(De_FSMFillForm.fill_decrypt_key)

# Этот хэндлер выводит Зашифрованный текст на Заданный пользователем ключ
@router.message(StateFilter(De_FSMFillForm.fill_decrypt_key))
async def caesar_process_decrypt_key_sent(message: Message):
    if message.text.isdigit():
        decrypt_caesar_text = caesar_save_decrypt_to_history(message.from_user.id, LEXICON['text_to_decrypt'], message.text)
        await message.answer(text='Зашифрованный текст:\n' + LEXICON['text_to_decrypt'] +'\n\n' + 'Ключ: ' +  message.text + '\n\n' + 'Расшифрованный текст:\n' + decrypt_caesar_text,
                             reply_markup=komanda_kb)
    else:
        await message.answer(
            text='Ключ должен быть целым числом\n\n'
                 'Попробуйте еще раз')

#Сохранение в базу данных
def caesar_save_decrypt_to_history(user_id, input_text, key):
    caesar_text_after = decrypt_caesar(input_text, key)
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO History(username, text_before, text_after, crypto_method, crypto_key) '
        f'VALUES(\'{user_id}\', \'{input_text}\', \'{caesar_text_after}\', \'Шифр Цезаря(Decrypt))\', \'{key}\')'
    )
    connection.commit()
    cursor.close()
    connection.close()
    return caesar_text_after


# ___________________________ШИФР С КЛЮЧОМ Зашифровать___________________________________

# Этот хэндлер будет срабатывать на кнопку Шифр с ключом Зашифровать
@router.message(F.text == LEXICON['en_crypt_key'])
async def with_key_process_encrypto_button(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваш текст')
    await state.set_state(En_FSMFillForm.fill_encrypt_text_wk)

# Этот хэндлер будет срабатывать, если введен корректный текст и ждать ввода ключа
@router.message(StateFilter(En_FSMFillForm.fill_encrypt_text_wk))
async def with_key_process_text_sent(message: Message, state: FSMContext):
    LEXICON['text_to_encrypt'] = message.text
    await message.answer(text='Пожалуйста, введите ключ')
    await state.set_state(En_FSMFillForm.fill_encrypt_key_wk)

# Этот хэндлер выводит Зашифрованный текст на Заданный пользователем ключ
@router.message(StateFilter(En_FSMFillForm.fill_encrypt_key_wk))
async def with_key_process_encrypt_key_sent(message: Message):
    if message.text.isdigit():
        encrypt_crypto_with_key_text = with_key_save_encrypt_to_history(message.from_user.id, LEXICON['text_to_encrypt'], message.text)
        await message.answer(text='Зашифрованный текст:\n' + LEXICON['text_to_encrypt'] +'\n\n' + 'Ключ: ' +  message.text + '\n\n' + 'Расшифрованный текст:\n' + encrypt_crypto_with_key_text,
                             reply_markup=komanda_kb)
    else:
        await message.answer(
            text='Ключ должен быть целым числом\n\n'
                 'Попробуйте еще раз')

#Сохранение в базу данных
def with_key_save_encrypt_to_history(user_id, input_text, key):
    with_key_text_after = encrypto_with_key(input_text, key)
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO History(username, text_before, text_after, crypto_method, crypto_key) '
        f'VALUES(\'{user_id}\', \'{input_text}\', \'{with_key_text_after}\', \'Шифр С Ключом(Encrypt))\', \'{key}\')'
    )
    connection.commit()
    cursor.close()
    connection.close()
    return with_key_text_after


# ___________________________ШИФР С КЛЮЧОМ Расшифровать___________________________________

# Этот хэндлер будет срабатывать на кнопку Шифр с ключом Расшифровать
@router.message(F.text == LEXICON['de_crypt_key'])
async def with_key_process_decrypto_button(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваш текст')
    await state.set_state(De_FSMFillForm.fill_decrypt_text_wk)

# Этот хэндлер будет срабатывать, если введен корректный текст и ждать ввода ключа
@router.message(StateFilter(De_FSMFillForm.fill_decrypt_text_wk))
async def with_key_process_text_sent(message: Message, state: FSMContext):
    LEXICON['text_to_decrypt'] = message.text
    await message.answer(text='Пожалуйста, введите ключ')
    await state.set_state(De_FSMFillForm.fill_decrypt_key_wk)

# Этот хэндлер выводит Расшифрованный текст на Заданный пользователем ключ
@router.message(StateFilter(De_FSMFillForm.fill_decrypt_key_wk))
async def with_key_process_decrypt_key_sent(message: Message):
    if message.text.isdigit():
        decrypt_crypto_with_key_text = with_key_save_decrypt_to_history(message.from_user.id, LEXICON['text_to_decrypt'], message.text)
        await message.answer(text='Зашифрованный текст:\n' + LEXICON['text_to_decrypt'] +'\n\n' + 'Ключ: ' +  message.text + '\n\n' + 'Расшифрованный текст:\n' + decrypt_crypto_with_key_text,
                             reply_markup=komanda_kb)
    else:
        await message.answer(
            text='Ключ должен быть целым числом\n\n'
                 'Попробуйте еще раз')

#Сохранение в базу данных
def with_key_save_decrypt_to_history(user_id, input_text, key):
    with_key_text_after = decrypto_with_key(input_text, key)
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO History(username, text_before, text_after, crypto_method, crypto_key) '
        f'VALUES(\'{user_id}\', \'{input_text}\', \'{with_key_text_after}\', \'Шифр С Ключом(Decrypt))\', \'{key}\')'
    )
    connection.commit()
    cursor.close()
    connection.close()
    return with_key_text_after


# ___________________________ШИФР ВИЖЕНЕРА Зашифровать___________________________________

# Этот хэндлер будет срабатывать на кнопку Шифр Виженера
@router.message(F.text == LEXICON['en_vigener'])
async def vigener_process_encrypto_button(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите ваш текст')
    await state.set_state(En_FSMFillForm.fill_encrypt_text_vigener)

# Этот хэндлер будет срабатывать, если введен корректный текст
@router.message(StateFilter(En_FSMFillForm.fill_encrypt_text_vigener))
async def vigener_process_text_sent(message: Message, state: FSMContext):
    LEXICON['text_to_encrypt'] = message.text
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Выберите тип ключа',
        reply_markup=create_key_keyboard()
    )
    await state.set_state(En_FSMFillForm.fill_encrypt_key_vigener)

# Этот хэндлер будет срабатывать на кнопку Заданный ключ
@router.callback_query(StateFilter(En_FSMFillForm.fill_encrypt_key_vigener),
                       F.data.in_(['key_know']))
async def vigener_process_encrypto_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Пожалуйста, введите ваш ключ')
    await state.set_state(En_FSMFillForm.fill_encrypt_key_text_vigener)

#Этот хэндлер выводит Зашифрованный текст на Заданный пользователем ключ
@router.message(StateFilter(En_FSMFillForm.fill_encrypt_key_text_vigener))
async def vigener_process_key_know_sent(message: Message):
    if message.text.isalpha():
        encrypt_vigener_text = vigener_save_encrypt_to_history(message.from_user.id, LEXICON['text_to_encrypt'], message.text)
        await message.answer(text='Исходный текст:\n' + LEXICON['text_to_encrypt'] +'\n\n' + 'Ключ: ' +  message.text + '\n\n' + 'Зашифрованный текст:\n' + encrypt_vigener_text,
                             reply_markup=komanda_kb)
    else:
        await message.answer(
            text='Ключ должен быть буквенным\n\n'
                 'Попробуйте еще раз')

# Этот хэндлер будет срабатывать на кнопку Произвольный ключ и выводить Зашифрованный текст
@router.callback_query(StateFilter(En_FSMFillForm.fill_encrypt_key_vigener),
                       F.data.in_(['random_key']))
async def vigener_process_encrypto_button(callback: CallbackQuery):
    await callback.message.delete()
    random_key = get_random_words(LEXICON['text_to_encrypt'])
    #await callback.message.answer(text='Произвольный ключ: ' + str(random_key))
    encrypt_vigener_text = vigener_save_encrypt_to_history(callback.from_user.id, LEXICON['text_to_encrypt'], random_key)
    await callback.message.answer(text='Исходный текст:\n' + LEXICON['text_to_encrypt'] +'\n\n' + 'Ключ: ' + str(random_key) + '\n\n' + 'Зашифрованный текст:\n' + encrypt_vigener_text,
                                  reply_markup=komanda_kb)

#Сохранение в базу данных
def vigener_save_encrypt_to_history(user_id, input_text, key):
    vigener_text_after = encrypto_vigener(input_text, key)
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO History(username, text_before, text_after, crypto_method, crypto_key) '
        f'VALUES(\'{user_id}\', \'{input_text}\', \'{vigener_text_after}\', \'Шифр Виженера(Encrypt))\', \'{key}\')'
    )
    connection.commit()
    cursor.close()
    connection.close()
    return vigener_text_after


# ___________________________ШИФР ВИЖЕНЕРА Расшифровать___________________________________

# Этот хэндлер будет срабатывать на кнопку Шифр Виженера Расшифровать
@router.message(F.text == LEXICON['de_vigener'])
async def vigener_process_decrypto_button(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите зашифрованный текст')
    await state.set_state(De_FSMFillForm.fill_decrypt_text_vigener)

# Этот хэндлер будет срабатывать, если введен корректный текст и ждать ввода ключа
@router.message(StateFilter(De_FSMFillForm.fill_decrypt_text_vigener))
async def vigener_process_text_sent(message: Message, state: FSMContext):
    LEXICON['text_to_decrypt'] = message.text
    await message.answer(text='Пожалуйста, введите ключ')
    await state.set_state(De_FSMFillForm.fill_decrypt_key_vigener)

# Этот хэндлер выводит Зашифрованный текст на Заданный пользователем ключ
@router.message(StateFilter(De_FSMFillForm.fill_decrypt_key_vigener))
async def vigener_process_decrypt_key_sent(message: Message):
    if message.text.isalpha():
        decrypt_vigener_text = vigener_save_decrypt_to_history(message.from_user.id, LEXICON['text_to_decrypt'], message.text)
        await message.answer(text='Зашифрованный текст:\n' + LEXICON['text_to_decrypt'] +'\n\n' + 'Ключ: ' +  message.text + '\n\n' + 'Расшифрованный текст:\n' + decrypt_vigener_text,
                             reply_markup=komanda_kb)
    else:
        await message.answer(
            text='Ключ должен быть буквенным\n\n'
                 'Попробуйте еще раз')

#Сохранение в базу данных
def vigener_save_decrypt_to_history(user_id, input_text, key):
    vigener_text_after = decrypto_vigener(input_text, key)
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO History(username, text_before, text_after, crypto_method, crypto_key) '
        f'VALUES(\'{user_id}\', \'{input_text}\', \'{vigener_text_after}\', \'Шифр Виженера(Decrypt))\', \'{key}\')'
    )
    connection.commit()
    cursor.close()
    connection.close()
    return vigener_text_after



# ___________________________HISTORY___________________________________

# Этот хэндлер будет срабатывать на команду '/history'
# и показывать пользователю сохраненные тексты, если они есть,
# или сообщение о том, что сохраненных текстов нет
@router.message(Command(commands='history'))
async def process_history_command(message: Message):
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * FROM History WHERE username = {message.from_user.id} ORDER BY id DESC LIMIT 5'
    )
    history = cursor.fetchall()

    if not history:
        await message.answer(text=LEXICON['no_history'])
        return

    keyboard_markup = create_history_keyboard(history)
    await message.answer(
        text='Список последних 5 шифров из истории',
        reply_markup=keyboard_markup
        )

    connection.commit()
    cursor.close()
    connection.close()


@router.callback_query(IsDigitCallbackData())
async def process_history_press(callback: CallbackQuery):
    history_id = int(callback.data)
    connection = sqlite3.connect('crypto_history.db')
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * FROM History WHERE id = {history_id}'
    )
    history = cursor.fetchall()

    if history:
        for stroka in history:
            await callback.message.answer(
                text=f'{stroka[4]}\nИсходный текст: {stroka[2]}\nРезультат: {stroka[3]}\nКлюч: {stroka[5]}'
            )
    else:
        await callback.message.answer(text=LEXICON['no_history'])

    await callback.answer()
    cursor.close()
    connection.close()