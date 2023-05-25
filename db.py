from mysql.connector import *
import hashlib
import datetime

def get_user(login, password):
    try:
        with connect(
                host="localhost",
                user="root",
                password="1111",
                database="study_app",
        ) as connection:
            select_movies_query = "SELECT * FROM users"
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    if row[0] == int(login) and row[1] == hashlib.sha256(password.encode()).hexdigest():
                        return row
                return "not found"
    except Error as e:
        return e


def get_username_by_id(id):
    try:
        with connect(
                host="localhost",
                user="root",
                password="1111",
                database="study_app",
        ) as connection:
            select_movies_query = "SELECT id, name, surname, patronymic FROM users where id = %s"
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query, (id,))
                result = cursor.fetchall()
                return result[0]
    except Error as e:
        return e


def get_chats(id):
    try:
        with connect(
                host="localhost",
                user="root",
                password="1111",
                database="study_app",
        ) as connection:
            select_movies_query = "SELECT * FROM chat where user1id = %s or user2Id = %s"
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query, (id, id))
                result = cursor.fetchall()
                return result
    except Error as e:
        return e


def get_messages(chatId):
    try:
        with connect(
                host="localhost",
                user="root",
                password="1111",
                database="study_app",
        ) as connection:
            select_movies_query = "SELECT * FROM messages where chatId = %s"
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query, (chatId,))
                result = cursor.fetchall()
                return result
    except Error as e:
        return e


def add_messages(chatId, mes, userId):
    try:
        with connect(
                host="localhost",
                user="root",
                password="1111",
                database="study_app",
        ) as connection:
            select_movies_query = "INSERT INTO messages (chatId, message, userId, datetime) VALUES (%s, %s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query, (chatId, mes, userId, str(datetime.datetime.now())))
                connection.commit()
    except Error as e:
        return e













# def add_token(token, userId):
#     try:
#         with connect(
#                 host="localhost",
#                 user="root",
#                 password="1111",
#                 database="study_app",
#         ) as connection:
#             select_movies_query = "INSERT INTO tokens (token, userId) VALUES (%s, %s)"
#             with connection.cursor() as cursor:
#                 cursor.execute(select_movies_query, (token, userId))
#                 connection.commit()
#     except Error as e:
#         return e
#
# def get_user_by_token(token):
#     try:
#         with connect(
#                 host="localhost",
#                 user="root",
#                 password="1111",
#                 database="study_app",
#         ) as connection:
#             select_movies_query = "SELECT users.* FROM users join tokens on users.id = tokens.user_id where token = %s"
#             with connection.cursor() as cursor:
#                 cursor.execute(select_movies_query, (token,))
#                 result = cursor.fetchall()
#                 if result: return result[0]
#                 return None
#     except Error as e:
#         return e

# add_messages(1, "Здравствуйте, у меня вопрос по лабораторной работе.", 1)
# add_messages(1, "Здравствуй, конечно спрашивай.", 2)

# print(get_messages(1))