import random
import time
from datetime import datetime
import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot("6184823844:AAE7JvBRB4shgFkLd2353I9ihWf4Ggtkr74")

admins = [['ruslan','111']]

login = None
id = None
auth_process = None
account = None
user_input_login = None
user_input_password = None
user_input_login = None
auth_process = None
user_is_admin = None
users_list = []
example_text = None
example_id = None
feedback_enable = None

INFORMATION = '''
<b>Information:</b>
/start - Старт бота
/help - Помощь
/id - Узнать ваш id в telegram
/website - Открыть сайт
/photo - Я отправлю вам фото
/audio - Я отправлю вам аудио
/example - Решить пример
/feedback - связь с разработчиком
/auth - Вход в аккаунт
/reg - Регистрация
/users - Список пользователей (для администрации)
/leave - Выход с аккаунта
/status - Статус
Так-же ты можешь отправить мне фото!
'''

@bot.message_handler(commands=['leave'])
def leave(message):
    global account
    global user_is_admin
    account = None
    user_is_admin = None
    bot.send_message(message.chat.id,'Выход успешен!')
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Выполнил выход из аккаунта')

@bot.message_handler(commands=['users'])
def users(message):
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'id: {el[0]}, Имя: {el[1]}, пароль: {el[2]}\n'
    cur.close()
    conn.close()
    if user_is_admin:
        bot.send_message(message.chat.id, info)
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) посмотрел список учетных записей')

    else:
        bot.send_message(message.chat.id, 'У вас не достаточно прав')
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) не смог посмотреть учетные записи из-за отсутствия прав администратора')



@bot.message_handler(commands=['reg'])
def reg_user(message):
    global id
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    id = message.from_user.id
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int(50), login varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'привет, сейчас тебя зарегистрируем, придумайте логин')
    bot.register_next_step_handler(message, user_login)


@bot.message_handler(commands=['auth'])
def auth_user(message):
    global auth_process
    auth_process = True
    try:
        bot.send_message(message.chat.id, 'НЕ ВВОДИТЕ НИКАКИЕ КОМАНДЫ В ПРОЦЕССЕ АВТОРИЗАЦИИ!\nВведите Логин:')
        bot.register_next_step_handler(message, login_auth)
    except:
        pass

def login_auth(message):
    global auth_process
    global user_input_login
    if not '/' in message.text:
        user_input_login = (message.text)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(message, password_auth)
    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Авторизация безуспешна')
        auth_process = False


def password_auth(message):
    global account
    global auth_process
    global user_input_password
    global user_is_admin
    if not '/' in message.text:
        user_input_password = (message.text)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Авторизация успешная')
    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Авторизация безуспешна')
        return
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    for i in users:
        if i[1] == user_input_login:
            if i[2] == user_input_password:
                account = i[0]
                cur.close()
                conn.close()
                for k in admins:
                    if str(k[0]) == str(i[1]) and str(k[1]) == str(i[2]):
                        bot.send_message(message.chat.id, f'Добро пожаловать, {i[1]} (id:{message.from_user.id}) Статус - администратор\n /leave - выйти с аккаунта')
                        user_is_admin = True
                        auth_process = False
                        return
                bot.send_message(message.chat.id, f'Добро пожаловать, {i[1]} (id:{message.from_user.id}) Статус - пользователь\n/leave - выйти с аккаунта')
                auth_process = False
                return
    bot.send_message(message.chat.id, 'Не удачно.')
    auth_process = False
    cur.close()
    conn.close()






def user_login(message):
    global users_list
    global login
    conn = sqlite3.connect('ober.sql')
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
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Регистрация безуспешна')

def user_pass(message):
    if not '/' in message.text.strip():
        password = message.text.strip()
        conn = sqlite3.connect('ober.sql')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users (id, login, pass) VALUES ("%s", "%s","%s")' % (id, login, password))
        conn.commit()
        cur.close()
        conn.close()

        marcup = types.InlineKeyboardMarkup()
        marcup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
        bot.send_message(message.chat.id, 'Вы зарегистрированны!\nИспользуйте /auth для входа в учетную запись', reply_markup=marcup)
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Успешно зарегистрировался')
    else:
        bot.send_message(message.chat.id, 'У вас не должно быть / в логине')
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Регистрация безуспешна')




@bot.message_handler(commands=['feedback'])
def feedback(message):
    markup = types.InlineKeyboardMarkup()
    btn_feedback = types.InlineKeyboardButton('Связь с разработчиком', callback_data='feedback_logs')
    markup.add(btn_feedback)
    bot.send_message(message.chat.id, parse_mode='html', text='<b>Для связи</b>:\ndiscord - Ober11#7777\ntg - @Oberrrr\nИли вы можете оставить Feedback по кнопке ниже:', reply_markup=markup)
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку feedback_information')
@bot.message_handler(commands=['example'])
def example(message):
    global example_text
    global example_id
    bot.send_message(message.chat.id, 'Отправьте ваш пример:')
    example_text = True
    example_id = message.message_id
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку example')


@bot.message_handler(commands=["audio"])
def audio(message):
    file = open('audio/voice.mp3', 'rb')
    bot.send_audio(message.chat.id, file)
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку audio')


@bot.message_handler(commands=["start"])
def main(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Помощь по командам")
    markup.row(btn1)
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} {message.from_user.username}!\nЯ бот помощник, напиши /help",reply_markup=markup)
    bot.register_next_step_handler(message, on_click_help)
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку start')

def on_click_help(message):
    if message.text == "Помощь по командам" or "/help":
        help1(message)
    else:
        bot.send_message(message.chat.id, "Ошибка. Попробуйте еще раз. Логи ошибки уже доставлены разработчику")
        print(f"\nERROR    Пользователь {message.from_user.first_name} (id:{message.from_user.id}  Команда не обработана\n")



@bot.message_handler(commands=["help"])
def help1(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url="https://ober1.st8.ru/"))
    bot.send_message(message.chat.id, INFORMATION, parse_mode='html', reply_markup=markup)
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку help')


@bot.message_handler(commands=["photo"])
def send_photo(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Удалить фото', callback_data='delete_last')
    markup.row(btn1)
    file = open(f'img/flower{random.randint(1,3)}.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку фото')




@bot.message_handler(commands=["id"])
def id(message):
    bot.reply_to(message, f'Ваш id : {message.from_user.id}')
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку id')


@bot.message_handler(commands=["website","site"])
def website(message):
    webbrowser.open("https://ober1.st8.ru/")
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку site')

@bot.message_handler(commands=['status'])
def status(message):
    if user_is_admin:
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
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) отправил фото')

@bot.message_handler()
def info(message):
    global example_text
    global example_id
    global feedback_enable
    global feedback_id

    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Здарова")
    elif message.text == "Помощь по командам":
        help1(message)
    else:
        if feedback_enable == True and feedback_id+2 == message.id:
            print("\033[31m{}".format(f'\n{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) сообщил об ошибке:\ntext:{message.text}'))
            feedback_enable = False
            bot.send_message(message.chat.id, 'Обращение доставлено')
            print('\033[0m{}'.format(''))

        elif example_text == True and message.message_id-2 == example_id:
            try:
                print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) ввел пример:{message.text} (id:{message.message_id - 1}) ')
                example_text = False
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Решить еще', callback_data='example_repeat'))
                bot.send_message(message.chat.id, eval(str(message.text)), reply_markup=markup)
                return
            except:
                bot.send_message(message.chat.id, "Произошла ошибка. Скорее всего вы ввели не цифры, попробуйте еще раз  /example")
        else:
            bot.send_message(message.chat.id, 'Такой команды нет. /help - чтобы узнать команды')
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) отправил сообщение id:{message.message_id - 1} text:{message.text}')

@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global example_text
    global example_id
    global feedback_enable
    global feedback_id

    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Фото удалено!")
        print(f'{datetime.now()}: Пользователь {callback.message.from_user.first_name} (id:{callback.message.from_user.id}) Нажал на кнопку delete_photo')

    elif callback.data == 'edit':
        bot.edit_message_text("Какое красивое фото!",callback.message.chat.id, callback.message.message_id)

    elif callback.data == 'delete_last':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Фото удалено!")
        print(f'{datetime.now()}: Пользователь {callback.message.from_user.first_name} (id:{callback.message.from_user.id}) Нажал на кнопку delete_last_photo')

    elif callback.data == 'example_repeat':
        example_text = True
        bot.send_message(callback.message.chat.id, 'Введите пример:')
        example_id = callback.message.message_id

        print(f'{datetime.now()}: Пользователь {callback.message.from_user.first_name} (id:{callback.message.from_user.id}) Нажал на кнопку Решить еще')

    elif callback.data == 'feedback_logs':
        feedback_enable = True
        feedback_id = callback.message.id
        bot.send_message(callback.message.chat.id, "Введите сообщение:")

@bot.callback_query_handler(func=lambda call: True)
def callback2(call):
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'id: {el[0]}, Имя: {el[1]}, пароль: {el[2]}\n'
    cur.close()
    conn.close()
    if user_is_admin:
        bot.send_message(call.message.chat.id, info)
    else:
        bot.send_message(call.message.chat.id, 'У вас не достаточно прав')

bot.polling(none_stop=True)
