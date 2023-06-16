from telebot import types
import telebot
import sqlite3

bot = telebot.TeleBot("6113316955:AAH9zbWFe1lzDPyj6H57MMoJ9Y0B_w34S_Y")

login = None
id = None
auth_process = None
account = None
user_input_login = None
user_input_password = None
user_input_login = None
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
        bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(message, password_auth)
    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False


def password_auth(message):
    global account
    global auth_process
    global user_input_password
    if not '/' in message.text:
        user_input_password = (message.text)

    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False
        return
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    for i in users:
        print(i[1], user_input_login)
        print(i[2], user_input_password)
        if i[1] == user_input_login:
            if i[2] == user_input_password:
                account = i[0]
                cur.close()
                conn.close()
                bot.send_message(message.chat.id, f'Добро пожаловать, {i[1]} (id:{message.from_user.id})')
                auth_process = False
                return
    bot.send_message(message.chat.id, 'Не удачно.')
    cur.close()
    conn.close()






def user_login(message):
    global login
    login = message.text.strip()
    bot.send_message(message.chat.id, 'введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO users (id, login, pass) VALUES ("%s", "%s","%s")' % (id, login, password))
    conn.commit()
    cur.close()
    conn.close()

    marcup = types.InlineKeyboardMarkup()
    marcup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Вы зарегистрированны', reply_markup=marcup)


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

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)