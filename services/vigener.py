from services.crypto_service import has_latin

def encrypto_vigener(text, key, reverse=False):
    if has_latin(text):
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 !%^&*-+=|~;:"<>?,.#'
    else:
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890 !%^&*-+=|~;:"<>?,.#'
    key_str = key.lower()
    key = [alphabet.find(k) for k in key_str] if not reverse else [-alphabet.find(k) - 1 for k in key_str]
    encrypted_text = ''
    key_index = 0

    for i in range(len(text)):
        number = key[key_index % len(key)]
        key_index += 1
        letter = text[i]
        position = alphabet.find(letter)
        encrypted_text += alphabet[(position + number) % len(alphabet)]

    return encrypted_text


def decrypto_vigener(text, key, reverse=True):

    if has_latin(text):
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 !%^&*-+=|~;:"<>?,.#'
    else:
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890 !%^&*-+=|~;:"<>?,.#'
    key_str = key.lower()
    key = [alphabet.find(k) + 1 for k in key_str] if not reverse else [-alphabet.find(k) for k in key_str]
    decrypted_text = ''
    key_index = 0

    for i in range(len(text)):
        number = key[key_index % len(key)]
        key_index += 1
        letter = text[i]
        position = alphabet.find(letter)
        decrypted_text += alphabet[(position + number) % len(alphabet)]

    return decrypted_text