# -*- coding: utf-8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import sqlite3
import time
import bs4
from random import randint
#========== - Все нужные переменные - ==========#
global game #Проверка, находитесь-ли в мини-игре "Авокадо" 
global _NUMBER #Рандомные числы мини-игры "Авокадо"
global avokado_int #Кол-во найденных авокадо,лок-ая переменная,разная для каждого пользователя 
global id_player #Персональное ИД в Базе Данных игры 
global id_vk_player #ИД ВКонтакте 
global avokado_player #Кол-во авокадо на счету, лок-ая переменная,разная для каждого пользователя
global zoloto_player #Кол-во золота на счету, лок-ая переменная,разная для каждого пользователя 
global stats # Общая переменная,в которой вся информация для пользователя
global top_player_1 #Топ-игрок №1
global top_player_2 #Топ-игрок №2
global top_player_3 #Топ-игрок №3
global name_surname_top_1
global name_surname_top_2
global name_surname_top_3
global top_over
global results
global if_banned
global ban_menu
global if_admin
if_admin = 0
ban_menu = False
if_banned = 0
results = 0
top_over = 0
name_surname_top_1 = 0
name_surname_top_2 = 0
name_surname_top_3 = 0
top_player_1 = 0
top_player_2 = 0
top_player_3 = 0
stats = 0
id_player = 0
id_vk_player = 0
avokado_player = 0
zoloto_player = 0
game = False
_NUMBER = [str(randint(1,200)),str(randint(1,200))]
avokado_int = 0
#========== - Подключение базы данных - ==========#
with sqlite3.connect('database.db') as db:
    cursor = db.cursor()
#========== - Печать выигрышных чисел в консоль - ==========#    
print(f"Числа: {_NUMBER}")
#========== - Основной класс бота - ==========#
class VkBot:
    def __init__(self, user_id):  
        self._USER_ID = user_id
        self._USER_LINK = "https://vk.com/id"+str(user_id)
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._ANSWERS = ['ДА', 'НЕТ']
        #========== - Все команды бота - ==========#
        self._COMMANDS = ["ПРИВЕТ", "ВРЕМЯ", "ПОКА", "АВОКАДО", "ТОП", "АДМИН","КОМАНДЫ", 'ЗАКОНЧИТЬ', 'МЕНЮ', 'ЗАРЕГИСТРИРОВАТЬСЯ','+', 'ЗАБЛОКИРОВАТЬ']
        #==========================================#
    #========== - Получение имени пользователя - ==========#    

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        name_surname = ' '.join((user_name.split()[0], user_name.split()[1]))
        return name_surname
    #======================================================#
    #========== - Получение времени - ==========#
    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]
    #===========================================#
    #========== - Получение пользователя - ==========#
    def get_user(self, user_id):        
        cmd = "SELECT * FROM players WHERE user_id = %d" % user_id        
        cursor.execute(cmd)
        return cursor.fetchone()

    def top_on_avocado(self):
        global top_player_1
        global top_player_2
        global top_player_3
        global name_surname_top_1
        global name_surname_top_2
        global name_surname_top_3
        global top_over
        cmd = 'SELECT id, user_id, avokado_int FROM players ORDER BY avokado_int DESC'
        cursor.execute(cmd)
        records = cursor.fetchall()
        top_player_1 = str(records[0])
        top_player_2 = str(records[1])
        top_player_3 = str(records[2])
        top_player_1 = top_player_1[1:-1]
        top_player_2 = top_player_2[1:-1]
        top_player_3 = top_player_3[1:-1]
        top_player_1 = top_player_1.split(',')
        top_player_2 = top_player_2.split(',')
        top_player_3 = top_player_3.split(',')
        name_surname_top_1 = self._get_user_name_from_vk_id(int(top_player_1[1]))
        name_surname_top_2 = self._get_user_name_from_vk_id(int(top_player_2[1]))
        name_surname_top_3 = self._get_user_name_from_vk_id(int(top_player_3[1]))
        top_over = f'1. {name_surname_top_1} - {top_player_1[2]} авокадо\n2. {name_surname_top_2} - {top_player_2[2]} авокадо\n3. {name_surname_top_3} - {top_player_3[2]} авокадо'
    

    def stats_on_player(self,user_id):
        global id_player
        global id_vk_player
        global avokado_player
        global zoloto_player
        global stats
        global if_admin

        sqlite_select_query = 'SELECT * from players WHERE user_id = %d' % user_id
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for row in records:
            id_player = f"Твой уникальный ID: {row[0]}"
            id_vk_player = f"Твой ID ВКонтакте: {row[1]}"
            avokado_player = f"Количество авокадо на твоем счету: {row[2]}"
            zoloto_player = f"Количество золота на твоем счету: {row[3]}"
            if_admin = f"Админ статус: {row[4]}"
            stats = '\n'.join((id_player, id_vk_player,avokado_player,zoloto_player, if_admin))


    #================================================#
    def if_player(self):
        global result
        global results
        cmd = "SELECT * FROM players WHERE id"   
        cursor.execute(cmd)
        result = cursor.fetchall()
        for row in result:
            results = row
        return results


    def if_ban(self,user_id):
        global if_banned
        sqlite_select_query = 'SELECT * from players WHERE user_id = %d' % user_id
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            if_banned = row[5]
        return if_banned
    
    def if_admin(self,user_id):     
        global if_admin
        sqlite_select_query = 'SELECT * from players WHERE user_id = %d' % user_id
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            if_admin = row[4]
        return if_admin

    def get_avocado(self, user_id):
        cmd = 'SELECT avokado_int FROM players WHERE user_id = %d' % user_id
        cursor.execute(cmd)
        return cursor.fetchone()
        
    def get_prize(self, user_id):        
        cmd = "SELECT * FROM prize WHERE user_id = %d" % user_id        
        cursor.execute(cmd)
        return cursor.fetchone()
    
    #========== - Очищение от не нужных тегов - ==========#  
    @staticmethod
    def _clean_all_tag_from_str(string_line):
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        
        return result
    #====================================================#
    #========== - Все проверки бота - ==========#
    def new_message(self, message):
        #========== - Все нужные переменные - ==========#
        global game
        global _NUMBER
        global avokado_int
        global id_player
        global id_vk_player
        global avokado_player
        global zoloto_player
        global stats
        global top_player_1
        global top_player_2
        global top_player_3
        global ban_menu
        #===============================================#
        #========== - Скрытая проверка,есть ли пользователель в бд, если нет - добавляет  - ==========#
        if not self.get_user(self._USER_ID):
            query = "INSERT INTO players (user_id) VALUES (%d)" % self._USER_ID
            cursor.execute(query)
            db.commit()
        #==============================================#

         #   return print(str(cursor.fetchone()))
        #========== - Основные проверки - ==========#
        if message.upper() in self._COMMANDS and self.if_ban(self._USER_ID) == 1:
            return 'Вы заблокированны!'
        '''if message.upper() == self._COMMANDS[0]:
            return 'Привет' '''
        if message.upper() == self._COMMANDS[0]:
            self.if_player()
            return results
        elif message.upper() == self._COMMANDS[6]:
            return "Все команды бота:\n1. Время - покажет московское время\n2. Авокадо - начать игру 'Авокадо'\n3. Топ - показывает топ пользователя по количеству найденных авокадо(на данный момент обновляется в ручную)\n4. Админ - функция для администраторов,на данный момент показывает только статистику"        
        elif message.upper() == self._COMMANDS[3]:
            return "Хочешь отгадать авокадо?"
        elif message.upper() == self._ANSWERS[0]:
            game = True
            return "Здорово!🥑 Вводи номер авокадо 🥑 от 1 до 200, если угадаешь, я тебе напишу об этом! (всего два числа). Если хочешь перестать играть - вводи: Закончить"
        elif message.upper() == _NUMBER[0] or message.upper() == _NUMBER[1]:
            print(f'ВНИМАНИЕ: {self._USERNAME}, {self._USER_LINK}: Нашел авокадо!')
            _NUMBER = [str(randint(1,200)),str(randint(1,200))]
            avokado_int = self.get_avocado(self._USER_ID)[0] + 1
            cmd = "UPDATE players SET avokado_int = %d WHERE user_id = %d" % (avokado_int, self._USER_ID)
            cursor.execute(cmd)
            db.commit()
            print(f'Новые числа: {_NUMBER}')
            return("Ура! Ты отгадал авокадо, поздравляю!🥑")
        elif message.upper() == self._COMMANDS[7] or message.upper() == self._ANSWERS[1]:
            game = False
            return "Жаль, можешь воспользоваться другими функциями бота: 'Команды'"   
        elif message.upper() == self._COMMANDS[8]:
            self.stats_on_player(self._USER_ID)
            return stats
        elif message.upper() == self._COMMANDS[4]:
            self.top_on_avocado()
            return top_over
        elif message.upper() == self._COMMANDS[5]:
            if self.if_admin(self._USER_ID) >= 1:
                return f"Количество найденных авокадо за ссесию: {avokado_int}\n\nФункции:\n1. Заблокировать"
            else:
                return "Нет доступа!"
        elif message.upper() == self._COMMANDS[2]:
            return "Пока-пока!"
        elif message.upper() != _NUMBER[0] and game == True or message.upper() != _NUMBER[1] and game == True:
            print(_NUMBER)
            return "Не отгадал!"            
        elif message.upper() == self._COMMANDS[10]:
            if not self.get_prize(self._USER_ID):
                query = "INSERT INTO prize (user_id) VALUES (%d)" % self._USER_ID
                cursor.execute(query)
                db.commit()
            return "Круто! Ты учавствуешь в конкурсе"
        elif message.upper() == self._COMMANDS[11]:
            ban_menu = True
            return "Вы вошли в бан-меню, введите персональный id пользователя"
        elif self.if_admin(self._USER_ID) >= 1 and ban_menu == True:
            ban_menu = False
            return 'Игрок забанен'
        else:
            return f"{self._USERNAME}, я тебя не понимаю :("
        #===============================================#
#=============================================#    
    
    
    
    
    
    
    
    
    
    