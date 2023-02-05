import sqlite3
import time
import math


class FDataBase: # будет принимать db
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self): # функция вывода данных menu
        sql = 'SELECT * FROM mainmenu' # запрос на вывод все данных из таблицы
        try: # если БД существует
            self.__cur.execute(sql) # считываем данные
            res = self.__cur.fetchall() # все данные сохраняем в переменную res
            if res: # если res не пустой
                return res
        except IOError: # если произошла ошибка и try не отработал
            print("Ошибка чтения из БД")
        return [] # если ничего не вернет создадим пустой список

    def add_post(self, title, text, url): # функция добавления данных в БД
        try:
            self.__cur.execute('SELECT COUNT() as "count" FROM posts WHERE url LIKE ?', (url,))
            res = self.__cur.fetchone()
            if res['count']> 0:
                print('Услуга с таким url уже существует')
                return False
            tm =math.floor(time.time()) # создаем время вернет кол-во секунд
            self.__cur.execute('INSERT INTO posts VALUES(NULL,?,?,?,?)',
                               (title, text,url, tm)) # вызываем cur и добавляем данные
            self.__db.commit() # сохраняем данные в БД
        except sqlite3.Error as e:
            print("Ошибка добавления услуги в БД" + str(e))
            return False

        return True # если все корректно отрабатывает в try возвращаем True

    def get_posts_anonce(self): # вывод данных услуг из БД
        try:
            self.__cur.execute('SELECT id, title, text, url FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res: # если try отработает то вернем данные
                return res
        except sqlite3.Error as e:
            print("Ошибка получения услуги в БД" + str(e))
            return []

    def get_post(self, alias):
        try:
            self.__cur.execute(f'SELECT title, text FROM posts WHERE url="{alias}" LIMIT 1')
            res = self.__cur.fetchone()
            if res: # если try отработает то вернем данные
                return res
        except sqlite3.Error as e:
            print("Ошибка получения услуги в БД" + str(e))
            return []

        return False, False