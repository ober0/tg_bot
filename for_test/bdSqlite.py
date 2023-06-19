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