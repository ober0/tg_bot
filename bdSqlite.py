from telebot import types
import telebot
import sqlite3

bot = telebot.TeleBot("6113316955:AAH9zbWFe1lzDPyj6H57MMoJ9Y0B_w34S_Y")

login = None
id = None
auth_process = None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет.\n/auth - авторизация\n/reg - регистрация')

@bot.message_handler(commands=['reg'])
def reg_user(message):
    global id
    conn = sqlite3.connect('ober.sql')
    cur = conn.cursor()
    id = message.from_user.id
    print(id)
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int(50), login varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'привет, сейчас тебя зарегистрируем, придумайте логин')
    bot.register_next_step_handler(message, user_login)




def login_auth(message):
    global auth_process
    if not '/' in message.text:
        print(message.text)
        bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(message, password_auth)
    else:
        bot.send_message(message.chat.id, 'Не используйте символ /')
        auth_process = False


def password_auth(message):
    global auth_process
    if not '/' in message.text:
        print(message.text)
    else:
        bot.send_message('Не используйте символ /')
        auth_process = False



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