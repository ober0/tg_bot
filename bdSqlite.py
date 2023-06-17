from telebot import types
import telebot
import sqlite3
from datetime import datetime

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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет.\n/auth - авторизация\n/reg - регистрация')

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

    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False
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
            bot.send_message(message.chat.id, "Придумайте другой login")
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


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
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