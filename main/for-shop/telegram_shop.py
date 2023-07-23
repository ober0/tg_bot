import types
from telebot import types
import telebot
import json


bot = telebot.TeleBot("6184823844:AAE7JvBRB4shgFkLd2353I9ihWf4Ggtkr74")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Форма заказа',web_app=types.WebAppInfo(url='https://ober1.st8.ru/tg/new/telegram.html')))
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def web_app(message):
    res = json.loads(message.web_app_data.data)
    name = res['name']
    email = res['email']
    text = res['text']
    tg = res['telegram_id']
    time = res['time']
    print(name,email,tg,text, time)
    string = f'{name},{email},{tg},{time},{text}\n'
    with open('req.txt', 'a', encoding='utf-8')as file:
        file.write(string)

bot.message_handler(commands=['test'])
def test(message):
    res = []
    with open('req.txt', 'r', encoding='utf-8')as file1:
        for i in file1.readlines():
            res.append(i)
    for i in res:
        bot.send_message(message.chat.id, i)


bot.polling(none_stop=True)