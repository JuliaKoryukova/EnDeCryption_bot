import sqlite3

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('crypto_history.db')
cursor = connection.cursor()

#Создаем таблицу History
cursor.execute('''
CREATE TABLE IF NOT EXISTS History (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
text_before TEXT NOT NULL,
text_after TEXT NOT NULL,
crypto_method TEXT NOT NULL,
crypto_key INTEGER
)
''')

#Выбираем всех пользователей
cursor.execute('SELECT * FROM History')
history = cursor.fetchall()

#Преобразуем результаты в список словарей
history_list = []
for user in history:
    user_dict = {
       'id': user[0],
       'username': user[1],
       'text_before': user[2],
       'text_after': user[3],
        'crypto_method': user[4],
        'crypto_key': user[5]
    }
    history_list.append(user_dict)

# #Сохраняем изменения и закрываем соединение
connection.commit()
cursor.close()
connection.close()