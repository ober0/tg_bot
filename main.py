import random
import time
from datetime import datetime
import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot("6113316955:AAH9zbWFe1lzDPyj6H57MMoJ9Y0B_w34S_Y")

example_text = None
example_id = None

@bot.message_handler(commands=['example'])
def example(message):
    global example_text
    global example_id
    bot.send_message(message.chat.id, 'Отправьте ваш пример:')
    example_text = True
    example_id = message.message_id



@bot.message_handler(commands=["audio"])
def audio(message):
    file = open('voice.mp3', 'rb')
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


@bot.message_handler(commands=["help"])
def help1(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url="https://ober1.st8.ru/"))
    bot.send_message(message.chat.id, "<b>Information:</b>\n/start - Старт бота\n/id - Узнать ваш id в telegram\n/website - Открыть сайт\n/photo - Я отправлю вам фото\n/audio - Я отправлю вам аудио\nТак-же ты можешь отправить мне фото!",
                     parse_mode='html', reply_markup=markup)
    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку help')


@bot.message_handler(commands=["photo"])
def send_photo(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Удалить фото', callback_data='delete_last')
    markup.row(btn1)
    file = open(f'flower{random.randint(1,3)}.png', 'rb')
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

    print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) отправил сообщение id:{message.message_id-1} text:{message.text}')
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Здарова")
    elif message.text == "Помощь по командам":
        help1(message)
    else:
        if example_text == True and message.message_id-2 == example_id:
            try:
                bot.send_message(message.chat.id, eval(str(message.text)))
                example_text = False

            except:
                bot.send_message(message.chat.id, "Произошла ошибка. Скорее всего вы ввели не цифры, попробуйте еще раз")
        else:
            bot.send_message(message.chat.id, 'Такой команды нет. /help - чтобы узнать команды')

@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'edit':
        bot.edit_message_text("Какое красивое фото!",callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'delete_last':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Фото удалено!")
        print(f'{datetime.now()}: Пользователь {message.from_user.first_name} (id:{message.from_user.id}) Нажал на кнопку удалить фото')

bot.polling(none_stop=True)
