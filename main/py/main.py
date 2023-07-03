import random
from datetime import datetime
import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from translate import Translator
from config import *
import check_is_admin
from langdetect import detect
from langdetect import detect_langs
from gtts import gTTS
import os
import shutil
from currency_converter import CurrencyConverter

currency = CurrencyConverter()
translator = Translator(to_lang="Russian")

bot = telebot.TeleBot("6184823844:AAE7JvBRB4shgFkLd2353I9ihWf4Ggtkr74")

@bot.message_handler(commands=['vip_info'])
def vip_info(message):
    bot.send_message(message.chat.id, f'<b>vip_info</b>\n{possibilities}', parse_mode='html')

@bot.message_handler(commands=['buy_vip'])
def buy_vip(message):
    bot.send_message(message.chat.id, '<b>Автоматическая продажа еще в ращработке. Для покупки vip статуса напишите @Oberrrr</b>\nСтоимость - <u>99р</u>\nВозморжности вип - /vip_info', parse_mode='html')


@bot.message_handler(commands=['get_vip'])
def get_vip(message):
    if user_is_admin and int(message.chat.id) == 947827934:
        bot.send_message(message.chat.id, 'Введите id человека, которому хотите выдать вип:')
        bot.register_next_step_handler(message, get_vip_step2)
    else:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!')
def get_vip_step2(message):
    global new_vip_people
    new_vip_people = message.text
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, get_vip_step3)

def get_vip_step3(message):
    if message.text == 'qwerty123321':
        id = new_vip_people
        with open('../sql/vip.txt', 'a', encoding='utf-8')as file1:
            file1.write(f'{id}\n')
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, 'Успешно.')


@bot.message_handler(commands=['convert_currency'])
def convert(message):
    bot.send_message(message.chat.id, '<b>Введите сумму</b>\nДля отмены введите cancel', parse_mode='html')
    bot.register_next_step_handler(message, convert_step2)

def convert_step2(message):
    global amount
    try:
        if message.text.strip() == 'cancel':
            bot.send_message(message.chat.id, ' Действие отменено.')
            return
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, '<b>Вы ввели отрицательное число или 0, введите сумму заново.</b>\nДля отмены введите cancel', parse_mode='html')
            bot.register_next_step_handler(message, convert_step2)
            return

    except ValueError:
        bot.send_message(message.chat.id, '<b>Неверный формат, введите сумму заново.</b>\nДля отмены введите cancel', parse_mode='html')
        bot.register_next_step_handler(message, convert_step2)
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
    btn3 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
    btn4 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
    btn5 = types.InlineKeyboardButton('Другое значение', callback_data='else_curr')
    markup.add(btn1,btn2, btn3,btn4,btn5)
    bot.send_message(message.chat.id,
                     '<b>Обращаем ваше внимание!</b>\n<u>конвертация любых валют в RUB временно не доступна.</u>\nПриносим свои извинения.',
                     parse_mode='html')
    bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)

def convert_step3(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Повторить', callback_data='repeat_convert')
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Повторить', callback_data='repeat_convert')
        markup.add(btn)
        bot.send_message(message.chat.id, f'{amount}{values[0]} = {round(res, 3)}{values[1]}', reply_markup=markup)

    except:
        bot.send_message(message.chat.id, '<b>Неверный формат, введите сумму заново.</b>\nДля отмены введите cancel\nЕсли ошибка повторится используйте /feedback', parse_mode='html')
        bot.register_next_step_handler(message,convert_step2)
        return

@bot.message_handler(commands=['Send_Message'])
def Send_Message(message):
    if not user_is_admin or not message.chat.id in admins_list:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!')
        return
    bot.send_message(message.chat.id, 'Введите id адресанта')

    bot.register_next_step_handler(message, Send_Message_step1)

@bot.message_handler(commands=['send_all'])
def send_all(message):
    if not user_is_admin or not message.chat.id in admins_list:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!')
        return
    bot.send_message(message.chat.id, 'Введите сообщение:')
    bot.register_next_step_handler(message, send_all_step2)

def send_all_step2(message, success = 0, not_success = 0, success_list=[]):
    with open('../sql/users.txt', 'r', encoding='utf-8')as file:
        users_list = file.readlines()
        for i in users_list:
            try:
                bot.send_message(int(i), message.text)
                success += 1
                success_list.append(i)
            except:
                not_success += 1
        if not_success > 0:
            bot.send_message(message.chat.id, f'<b>Рассылка завершена</b>.\nУспешно - {success}\nНеуспешно - {not_success}\n<u>id с неудачной рассылкой удалены из списка</u>', parse_mode='html')
    with open('../sql/users.txt', 'w', encoding='utf-8')as file4:
        for j in success_list:
            file4.write(str(j))

def Send_Message_step1(message):
    global user_adress
    user_adress = message.text
    bot.send_message(message.chat.id, 'Введите сообщение')
    bot.register_next_step_handler(message, Send_Message_step2)
def Send_Message_step2(message):
    global user_adress
    message_to_user = message.text
    try:
        bot.send_message(user_adress, message_to_user)
    except:
        pass
    bot.send_message(message.chat.id, 'Сообщение отправлено')

@bot.message_handler(commands=['text_to_audio'])
def TextToAudio(message):
    check_id(message.chat.id)
    bot.send_message(message.chat.id, 'Введите текст для преобразования:')
    bot.register_next_step_handler(message, TextToAudio_text_input)

@bot.message_handler(commands=['reports'])
def check_reports(message):
    # if not user_is_admin or not message.chat.id in admins_list:
    #     bot.send_message(message.chat.id, 'У вас недостаточно прав!')
    #     return
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Feedback', callback_data='feedback_type')
    btn2 = types.InlineKeyboardButton('Обращение text_to_audio', callback_data='text_to_audio_type')
    markup.row(btn1,btn2)
    with open('../sql/feedback.txt', 'r', encoding='utf-8')as file:
        x = file.readlines()
        new_reports_feedback = len(x)
    with open('../sql/new_reports.txt', 'r', encoding='utf-8')as file2:
        y = file2.readlines()
        new_reports_audio = len(y)
    bot.send_message(message.chat.id,f'Новых обращений feedback - {new_reports_feedback}\nНовых обращений text to audio - {new_reports_audio}',parse_mode='html')
    bot.send_message(message.chat.id, '<b>Выберите категорию:</b>',reply_markup=markup, parse_mode='html')


def report_check_feedback(message, user_know=False, user_first=0):
    global user_id_feedback
    try:
        with open('../sql/feedback.txt', 'r', encoding='utf-8') as reports:
            reports_list = reports.readlines()
            for j in reports_list:
                user_first += 1
                x = j.replace('\n', '')
                user = (x[12:x.find(")") + 1])
                print(user[1:4])
                if user[1:4] == 'vip':
                    user = (x[17:x.find(")") + 1])
                    user_know = True
                    break
            if user_know == False:
                i = reports_list[0]
            else:
                i = reports_list[user_first-1]
            i = i.replace('\n', '')
            user_id_feedback = (i[i.find("(")+4:i.find(')')])
            if user_know == False:
                user = (i[12:i.find(")")+1])


            bot.send_message(message.chat.id, f'Сообщение от: {user}')
            bot.send_message(message.chat.id, f'Текст: {i[i.find("text")+5:]}')
            bot.send_message(message.chat.id, f'Ответьте пользователю:')
            bot.register_next_step_handler(message, report_check_feedback_step2)




        with open('../sql/feedback.txt', 'w', encoding='utf-8') as reports2:
            reports_list1 = []
            for i in reports_list:
                i = i.replace('\n', '')
                reports_list1.append(i)
            if user_know == True:
                reports_list1.pop(user_first-1)
            else:
                reports_list1.pop(0)
            for i in reports_list1:
                reports2.write(f'{i}\n')
    except:
        bot.send_message(message.chat.id, 'Репортов нет.')

def report_check_feedback_step2(message):
    try:
        bot.send_message(user_id_feedback, f'<b>Ответ администратора на ваше обращение:</b> {message.text}\nПодробнее - discord - Ober11#7777      tg - @Oberrrr', parse_mode='html')
    except:
        pass
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data='report_yes1')
    btn2 = types.InlineKeyboardButton('Нет', callback_data='report_no1')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'Репорт просмотрен, открыть следующий?', reply_markup=markup)


def report_check_audio(message):
    try:
        with open('../sql/new_reports.txt', 'r', encoding='utf-8')as reports:
            reports_list = reports.readlines()
            i = reports_list[0]
            i = i.replace('\n', '')
            file_txt = open(f'{i}/report.txt', encoding='utf-8')
            file_mp3 = open(f'{i}/report.mp3', 'rb')
            bot.send_audio(message.chat.id, file_mp3)
            bot.send_document(message.chat.id, file_txt)
            from_user_report = i[10:]
            from_user_report = from_user_report[::-1]
            from_user_report = from_user_report[(from_user_report.find('/')+1):]
            from_user_report = from_user_report[::-1]
            bot.send_message(from_user_report,'Ваш репорт был доставлен разработчикам, мы уже думаем над решением проблемы. С уважением, администрация.')
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Да', callback_data='report_yes')
            btn2 = types.InlineKeyboardButton('Нет', callback_data='report_no')
            markup.row(btn1, btn2)
            bot.send_message(message.chat.id, 'Репорт просмотрен, открыть следующий?', reply_markup=markup)
            file_txt.close()
            file_mp3.close()
            shutil.rmtree(i)

        with open('../sql/new_reports.txt', 'w', encoding='utf-8')as reports2:
            reports_list1 = []
            for i in reports_list:
                i = i.replace('\n', '')
                reports_list1.append(i)
            reports_list1.pop(0)
            for i in reports_list1:
                reports2.write(f'{i}\n')

    except:
        bot.send_message(message.chat.id, 'Репортов нет.')

def TextToAudio_text_input(message):
    global audio
    global language
    global text_for_report
    text_for_report = message.text

    try:
        audio = f"../audio_out/audio_for_{message.chat.id}.mp3"
        if detect(message.text) == 'mk' or detect(message.text) == 'bg':
            language = 'ru'
        else:
            language = detect(message.text)
    except:
        bot.send_message(message.chat.id, 'Язык не поддерживается, или не распознан, повторите попытку!\nЕсли ошибка повторится используйте /feedback')
        return
    try:
        sp = gTTS(text=message.text, lang=language, slow=False)
        sp.save(audio)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Распознование не верно', callback_data='Recognition_not_correct')
        markup.row(btn1)
        file = open(audio, 'rb')
        bot.send_audio(message.chat.id, file, title='Ваше сообщение')
        bot.send_message(message.chat.id, f'Язык сообщения: {language}\nЕсли язык распознан не правильно нажмите на кнопку ниже:', reply_markup=markup)
        file.close()
    except:
        bot.send_message(message.chat.id, 'Язык не поддерживается, или не распознан, повторите попытку!\nЕсли ошибка повторится используйте /feedback')
        return


def bug_report(error, chat_id, path):
    with open(f'../{path}/report.txt', 'w', encoding='utf-8') as file1:
        file1.write(f'Текст: {text_for_report}\nЯзык: {language}\nid: {chat_id}')
    with open('../sql/new_reports.txt', 'a', encoding='utf-8')as file2:
        file2.write(f'../{path}\n')
    try:
        shutil.move(f'{audio}', f'../{path}')
        os.rename(f'../errors/{chat_id}/error{error}/audio_for_{chat_id}.mp3',f'../errors/{chat_id}/error{error}/report.mp3')
    except:
        pass

@bot.message_handler(commands=['leave'])
def leave(message):
    check_id(message.chat.id)
    global account
    global user_is_admin
    global information
    account = None
    user_is_admin = None
    information = (check_is_admin.check_info_adm(user_is_admin, message.chat.id, admins_list))
    bot.send_message(message.chat.id, 'Выход успешен!')



@bot.message_handler(commands=['weather_users_info'])
def users(message):
    conn = sqlite3.connect('../sql/weather.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    weather = cur.fetchall()
    info = ''
    for i in weather:
        info += f'id: {i[0]}, Город: {i[1]}\n'
    cur.close()
    conn.close()
    if not user_is_admin or not message.chat.id in admins_list:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!')


    else:
        bot.send_message(message.chat.id, info)



@bot.message_handler(commands=['users'])
def users(message):
    conn = sqlite3.connect('../sql/ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'id: {el[0]}, Имя: {el[1]}, пароль: {el[2]}\n'
    cur.close()
    conn.close()
    if not user_is_admin or not message.chat.id in admins_list:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!')


    else:
        bot.send_message(message.chat.id, info)



@bot.message_handler(commands=['reg'])
def reg_user(message):
    check_id(message.chat.id)
    global id
    conn = sqlite3.connect('../sql/ober.sql')
    cur = conn.cursor()
    id = message.from_user.id
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int(50), login varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'привет, сейчас тебя зарегистрируем, придумайте логин')
    bot.register_next_step_handler(message, user_login)


@bot.message_handler(commands=['weather'])
def weather(message):
    check_id(message.chat.id)
    global weather_get
    global user_city
    global weather_get_id
    conn = sqlite3.connect('../sql/weather.sql')
    cur = conn.cursor()
    id1 = message.from_user.id
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int(15), city varchar(50))')
    conn.commit()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    res = []
    for i in data:
        res.insert(0, i)
    for i in res:
        if id1 == i[0]:
            if i[1] != None:
                user_city = i[1]
                weather_get = True
                weather_get_id = message.message_id
                res = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={TOKEN}&units=metric")
                try:
                    res = json.loads(res.text)
                    markup1 = types.InlineKeyboardMarkup()
                    btn_yes = types.InlineKeyboardButton('Да', callback_data='Yes_izm')
                    btn_no = types.InlineKeyboardButton('Нет', callback_data='No')
                    markup1.add(btn_no, btn_yes)
                    bot.send_message(message.chat.id,
                                     f'Погода в {user_city}: {round(int(res["main"]["temp"]))}°C, {translator.translate(res["weather"][0]["description"])}\nВетер: {res["wind"]["speed"]}м/с\nВлажность: {res["main"]["humidity"]}% ',
                                     )
                    bot.send_message(message.chat.id, 'Изменить город?', reply_markup=markup1)
                    weather_get = False
                except:
                    bot.send_message(message.chat.id,
                                     'Город указан не верно. Если вы уверенны, что город введен верно - напишите /feedback')
                    weather_get = False
                cur.close()
                conn.close()

                return

    bot.send_message(message.chat.id, 'Введите свой город:')
    weather_get = True
    weather_get_id = message.message_id

    cur.close()
    conn.close()


@bot.message_handler(commands=['auth'])
def auth_user(message):
    check_id(message.chat.id)
    global auth_process
    auth_process = True
    try:
        bot.send_message(message.chat.id, 'НЕ ВВОДИТЕ НИКАКИЕ КОМАНДЫ В ПРОЦЕССЕ АВТОРИЗАЦИИ!\nВведите Логин:')
        bot.register_next_step_handler(message, login_auth)
    except:
        pass


@bot.message_handler(commands=['DeleteMsg'])
def delete_msg(message):
    if user_is_admin and message.chat.id in admins_list:
        bot.send_message(message.chat.id, 'Кол-во сообщений:')
        bot.register_next_step_handler(message, delete_colvo_message)
        return
    bot.send_message(message.chat.id, 'У вас недостаточно прав!')


def delete_colvo_message(message):
    x = 0
    if message.text == 'all':
        while True:
            try:
                bot.delete_message(message.chat.id, message.message_id - x)
                x += 1
            except:
                pass

    else:
        try:
            count = int(message.text)
            for i in range(count):
                bot.delete_message(message.chat.id, message.message_id - x)
                x += 1
        except:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id - 2)


def login_auth(message):
    global auth_process
    global user_input_login
    if not '/' in message.text:
        user_input_login = (message.text)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(message, password_auth)
    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False


def password_auth(message):
    global account
    global auth_process
    global user_input_password
    global user_is_admin
    global information
    if not '/' in message.text:
        user_input_password = (message.text)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False
        return
    conn = sqlite3.connect('../sql/ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    for i in users:
        if i[1] == user_input_login:
            if i[2] == user_input_password:
                account = i[0]
                cur.close()
                conn.close()
                conn = sqlite3.connect('../sql/adm.sql')
                cur = conn.cursor()
                cur.execute('SELECT * FROM admins')
                users = cur.fetchall()
                for j in users:
                    if str(j[1]) == str(i[1]) and str(j[2]) == str(i[2]):
                        if message.chat.id in admins_list:
                            bot.send_message(message.chat.id,
                                             f'Добро пожаловать, {i[1]} (id:{message.from_user.id}) Статус - администратор\n /leave - выйти с аккаунта')
                        else:
                            admins_list.append(message.chat.id)
                            bot.send_message(message.chat.id,
                                             f'Добро пожаловать, {i[1]} (id:{message.from_user.id}) Статус - администратор\n /leave - выйти с аккаунта')

                        user_is_admin = True
                        information = (check_is_admin.check_info_adm(user_is_admin,  message.chat.id, admins_list))
                        auth_process = False
                        cur.close()
                        conn.close()
                        return
                cur.close()
                conn.close()
                bot.send_message(message.chat.id,
                                 f'Добро пожаловать, {i[1]} (id:{message.from_user.id}) Статус - пользователь\n/leave - выйти с аккаунта')
                auth_process = False
                return
    bot.send_message(message.chat.id, 'Не удачно.')
    auth_process = False
    cur.close()
    conn.close()




def user_login(message):
    global users_list
    global login
    conn = sqlite3.connect('../sql/ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT login FROM users')
    users1 = cur.fetchall()
    for i in users1:
        users_list.append(i)
    cur.close()
    conn.close()
    if not '/' in message.text.strip():
        if not message.text.strip() in str(users_list):
            login = message.text.strip()

            bot.send_message(message.chat.id, 'введите пароль')
            bot.register_next_step_handler(message, user_pass)
        else:
            bot.send_message(message.chat.id, "Придумайте другой login:")
            bot.register_next_step_handler(message, user_login)
            return
    else:
        bot.send_message(message.chat.id, 'У вас не должно быть / в логине')



def user_pass(message):
    if not '/' in message.text.strip():
        password = message.text.strip()
        conn = sqlite3.connect('../sql/ober.sql')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (id, login, pass) VALUES ("%s", "%s","%s")' % (id, login, password))
        conn.commit()
        cur.close()
        conn.close()

        marcup = types.InlineKeyboardMarkup()
        marcup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
        bot.send_message(message.chat.id, 'Вы зарегистрированны!\nИспользуйте /auth для входа в учетную запись',
                         reply_markup=marcup)

    else:
        bot.send_message(message.chat.id, 'У вас не должно быть / в логине')



@bot.message_handler(commands=['feedback'])
def feedback(message):
    markup = types.InlineKeyboardMarkup()
    btn_feedback = types.InlineKeyboardButton('Связь с разработчиком', callback_data='feedback_logs')
    markup.add(btn_feedback)
    bot.send_message(message.chat.id, parse_mode='html',
                     text='<b>Для связи</b>:\ndiscord - Ober11#7777\ntg - @Oberrrr\nИли вы можете оставить Feedback по кнопке ниже:',
                     reply_markup=markup)



@bot.message_handler(commands=['example'])
def example(message):
    check_id(message.chat.id)
    global example_text
    global example_id
    bot.send_message(message.chat.id, 'Отправьте ваш пример:')
    example_text = True
    example_id = message.message_id



@bot.message_handler(commands=["audio"])
def audio(message):
    file = open('../audio/voice.mp3', 'rb')
    bot.send_audio(message.chat.id, file)

def check_id(id):
    y = []
    with open('../sql/users.txt', 'r+', encoding='utf-8')as file:
        x = file.readlines()
        for i in x:
            y.append(str(i.replace('\n', '')))
        if str(id) not in y:
            file.write(f'{id}\n')


@bot.message_handler(commands=["start"])
def main(message):
    check_id(message.chat.id)

    bot.send_message(message.chat.id,
                     f"Привет {message.from_user.first_name} {message.from_user.username}!\nЯ бот помощник, напиши /help")








@bot.message_handler(commands=["help"])
def help1(message):
    check_id(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url="https://ober1.st8.ru/"))
    information = (check_is_admin.check_info_adm(user_is_admin, message.chat.id, admins_list))

    bot.send_message(message.chat.id, information, parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=["photo"])
def send_photo(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Удалить фото', callback_data='delete_last')
    markup.row(btn1)
    file = open(f'../img/flower{random.randint(1, 3)}.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)



@bot.message_handler(commands=["id"])
def id(message):
    bot.reply_to(message, f'Ваш id : {message.from_user.id}')



@bot.message_handler(commands=["website", "site"])
def website(message):
    webbrowser.open("https://ober1.st8.ru/")

@bot.message_handler(commands=['status'])
def status(message):
    if user_is_admin and message.chat.id in admins_list:
        bot.send_message(message.chat.id, f'Администратор ({message.from_user.id})')
    else:
        bot.send_message(message.chat.id, f'Пользователь ({message.from_user.id})')


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn2 = types.InlineKeyboardButton('Убрать кнопки', callback_data='edit')
    markup.row(btn1, btn2)
    markup.add()
    bot.reply_to(message, "Какое красивое фото!", reply_markup=markup)



@bot.message_handler()
def info(message):
    global example_text
    global example_id
    global feedback_enable
    global feedback_id
    global weather_get
    global user_city
    if message.message_id - 2 == weather_get_id:
        user_city = message.text.strip().lower()
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={TOKEN}&units=metric")

        try:
            data = json.loads(res.text)
            markup1 = types.InlineKeyboardMarkup()
            btn_yes = types.InlineKeyboardButton('Да', callback_data='Yes')
            btn_no = types.InlineKeyboardButton('Нет', callback_data='No')
            markup1.add(btn_no, btn_yes)
            bot.send_message(message.chat.id, f'Погода в {user_city}: {round(int(data["main"]["temp"]))}°C\n')
            bot.send_message(message.chat.id, 'Сохранить город?', reply_markup=markup1)
            weather_get = False

        except:
            bot.send_message(message.chat.id,
                             'Город указан не верно. Если вы уверенны, что город введен верно напишите /feedback')
            weather_get = False


    elif message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Здарова")
    elif message.text == "Помощь по командам":
        help1(message)
    else:
        if feedback_enable == True and feedback_id + 2 == message.id:
            with open('../sql/vip.txt', 'r', encoding='utf-8')as file5:
                all_vips = file5.readlines()
                vip_list = []
                for i in all_vips:
                    i = i.replace('\n', '')
                    vip_list.append(i)
            with open('../sql/feedback.txt', 'a', encoding='utf-8')as file:
                if str(message.from_user.id) in vip_list:
                    file.write(f'Пользователь vip*{message.from_user.first_name} (id:{message.from_user.id}) сообщил об ошибке. text:{message.text}\n')
                else:
                    file.write(
                        f'Пользователь {message.from_user.first_name} (id:{message.from_user.id}) сообщил об ошибке. text:{message.text}\n')

                    print('dont work')
            feedback_enable = False
            bot.send_message(message.chat.id, 'Обращение отправлено')


        elif example_text == True and message.message_id - 2 == example_id:
            try:
                example_text = False
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Решить еще', callback_data='example_repeat'))
                bot.send_message(message.chat.id, eval(str(message.text)), reply_markup=markup)
                return
            except:
                bot.send_message(message.chat.id, "Повторите ввод.")
        else:
            bot.send_message(message.chat.id, 'Такой команды нет. /help - чтобы узнать команды')



@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global example_text
    global example_id
    global feedback_enable
    global feedback_id

    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Фото удалено!")


    elif callback.data == 'edit':
        bot.edit_message_text("Какое красивое фото!", callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'report_yes':
        report_check_audio(callback.message)

    elif callback.data == 'report_no':
        pass
    elif callback.data == 'report_yes1':
        report_check_feedback(callback.message)

    elif callback.data == 'report_no1':
        pass
    elif callback.data == 'Recognition_not_correct':
        try:
            os.mkdir(f'../errors/{str(callback.message.chat.id)}')
        except:
            pass
        try:
            error = str(random.randint(1,100000000))
            os.mkdir(f'../errors/{str(callback.message.chat.id)}/error:{error}')
        except:
            error = str(random.randint(1, 100000000))
            os.mkdir(f'../errors/{str(callback.message.chat.id)}/error{error}')
        bot.send_message(callback.message.chat.id, 'Спасибо! Отчет об ошибке отправлен, при необходимости с вами свяжется администратор.')
        bug_report(error, str(callback.message.chat.id), f'errors/{str(callback.message.chat.id)}/error{error}')

    elif callback.data == 'delete_last':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Фото удалено!")


    elif callback.data == 'example_repeat':
        example_text = True
        bot.send_message(callback.message.chat.id, 'Введите пример:')
        example_id = callback.message.message_id



    elif callback.data == 'feedback_logs':
        feedback_enable = True
        feedback_id = callback.message.id
        bot.send_message(callback.message.chat.id, "Опишите вашу проблему:")

    elif callback.data == 'Yes':
        conn = sqlite3.connect('../sql/weather.sql')
        cur = conn.cursor()
        id1 = callback.message.chat.id
        cur.execute(f'INSERT INTO users (id, city) VALUES ("%s", "%s")' % (id1, user_city))
        conn.commit()
        cur.close()
        conn.close()
    elif callback.data == 'No':
        pass
    elif callback.data == 'Yes_izm':
        bot.send_message(callback.message.chat.id, 'Введите новый город')
        bot.register_next_step_handler(callback.message, edit_city)

    elif callback.data == 'feedback_type':
        report_check_feedback(callback.message)

    elif callback.data == 'text_to_audio_type':
        report_check_audio(callback.message)

    if callback.data == "repeat_convert":
        try:
            bot.send_message(callback.message.chat.id, '<b>Введите сумму</b>\nДля отмены введите cancel',
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, convert_step2)
        except:
            bot.send_message(callback.message.chat.id,
                             '<b>Произошла ошибка, введите сумму заново.</b>\nДля отмены введите cancel\nЕсли ошибка повторится используйте /feedback',
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, convert_step2)
            return

    elif callback.data == 'usd/eur' or callback.data == "eur/usd" or callback.data == 'usd/rub' or callback.data == 'rub/usd' or callback.data == 'eur/rub' or callback.data == 'rub/eur':
        try:
            values = callback.data.upper().split('/')
            res = currency.convert(amount, values[0], values[1])
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton('Повторить', callback_data='repeat_convert')
            markup.add(btn)
            bot.send_message(callback.message.chat.id, f'{amount}{values[0]} = {round(res, 3)}{values[1]}',
                             reply_markup=markup)
        except:
            bot.send_message(callback.message.chat.id,
                             '<b>Произошла ошибка, введите сумму заново.</b>\nДля отмены введите cancel\nЕсли ошибка повторится используйте /feedback',
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, convert_step2)
            return

    elif callback.data == 'else_curr':
        try:
            bot.send_message(callback.message.chat.id,
                             'Введите валюту в формате rub/usd (Ваша валюта/валюта  в которую нужно перевести)')
            bot.register_next_step_handler(callback.message, convert_step3)
        except:
            bot.send_message(callback.message.chat.id,
                             '<b>Произошла ошибка, введите сумму заново.</b>\nДля отмены введите cancel\nЕсли ошибка повторится используйте /feedback',
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, convert_step2)
            return

def edit_city(message):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={TOKEN}&units=metric")
    if res.status_code == 200:
        conn = sqlite3.connect('../sql/weather.sql')
        cur = conn.cursor()
        id1 = message.chat.id
        cur.execute(f'INSERT INTO users (id, city) VALUES ("%s", "%s")' % (id1, message.text))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, 'Успешно!')
    else:
        bot.send_message(message.chat.id, 'Не правильный город')



@bot.callback_query_handler(func=lambda call: True)
def callback2(call):
    conn = sqlite3.connect('../sql/ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'id: {el[0]}, Имя: {el[1]}, пароль: {el[2]}\n'
    cur.close()
    conn.close()
    if not user_is_admin or not call.message.chat.id in admins_list:
        bot.send_message(call.message.chat.id, 'У вас недостаточно прав!')
    else:
        bot.send_message(call.message.chat.id, info)

if __name__ == '__main__':
    bot.polling(none_stop=True)
