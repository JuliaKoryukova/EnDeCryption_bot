import re
import random
import string

#Проверка на пунктуацию
def remove_punctuation(input_string):
    translator = str.maketrans('', '', string.punctuation + ' ')
    result = input_string.translate(translator)
    result = result.lower()
    return result

#Определение алфавита
def has_latin(text):
    return bool(re.search('[a-zA-Z]', text))


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Функция возвращающая случайное слово
def get_random_words(text) -> str:
    if has_latin(text):
        random_words = random.choice(words_en)
    else:
        random_words = random.choice(words_ru)
    return random_words

words_en = ["apple", "banana", "cherry", "dog", "elephant", "flower", "guitar", "happy", "island", "jazz"]

words_ru = ["яблоко", "банан", "вишня", "собака", "слон", "цветок", "гитара", "счастливый", "остров", "джаз"]
