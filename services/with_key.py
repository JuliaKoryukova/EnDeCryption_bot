#Шифр Шифрование с ключом
import re
import string

from services.crypto_service import has_latin

def remove_punctuation(input_string):
    translator = str.maketrans('', '', string.punctuation + ' ')
    result = input_string.translate(translator)
    return result

def encrypto_with_key(text, key, reverse=False):
    encrypted_text = ''
    text = remove_punctuation(text)
    if has_latin(text):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
    else:
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    key_str = str(key)
    key = [int(k) for k in key_str] if not reverse else [-int(k) for k in key_str]
    decrypted = ''
    key_index = 0

    for i in range(len(text)):
        number = key[key_index % len(key)]
        key_index += 1
        letter = text[i]
        position = alphabet.find(letter)
        decrypted += alphabet[(position + number) % len(alphabet)]

    return decrypted

def decrypto_with_key(text, key, reverse=True):
    encrypted_text = ''
    text = remove_punctuation(text)
    if has_latin(text):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
    else:
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    key_str = str(key)
    key = [int(k) for k in key_str] if not reverse else [-int(k) for k in key_str]
    decrypted = ''
    key_index = 0

    for i in range(len(text)):
        number = key[key_index % len(key)]
        key_index += 1
        letter = text[i]
        position = alphabet.find(letter)
        decrypted += alphabet[(position + number) % len(alphabet)]

    return decrypted