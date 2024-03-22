#Зашифровка шифром Цезаря

from services.crypto_service import has_latin

def encrypt_caesar(text: str, key):
    encrypted_text = ''

    if has_latin(text):
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 !%^&*-+=|~;:"<>?,.#'
    else:
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890 !%^&*-+=|~;:"<>?,.#'

    for char in text:
        if char in alphabet:

            #Сдвиг по алфавиту
            key_char = alphabet[(alphabet.index(char) + int(key)) % len(alphabet)]
            encrypted_text += key_char

        else:
            encrypted_text += char

    return encrypted_text

#Расшифровка шифром Цезаря
def decrypt_caesar(text, key):
    decrypted_text = ''
    if has_latin(text) == True:
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 !%^&*-+=|~;:"<>?,.#'
    else:
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890 !%^&*-+=|~;:"<>?,.#'

    for char in text:
        if char in alphabet:

            # Сдвиг по алфавиту
            key_char = alphabet[(alphabet.index(char) - int(key)) % len(alphabet)]
            decrypted_text += key_char

        else:
            decrypted_text += char
    return decrypted_text