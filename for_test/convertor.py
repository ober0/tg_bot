import telebot
from telebot import types

from currency_converter import CurrencyConverter
currency = CurrencyConverter()
amount = 0

bot = telebot.TeleBot("6184823844:AAE7JvBRB4shgFkLd2353I9ihWf4Ggtkr74")

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
        bot.send_message(message.chat.id, '<b>Неверный формат, введите сумму заново.</b>\nДля отмены введите cancel 1', parse_mode='html')
        bot.register_next_step_handler(message, convert_step2)
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
    btn3 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
    btn4 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur')
    btn5 = types.InlineKeyboardButton('Другое значение', callback_data='else_curr')
    markup.add(btn1,btn2, btn3,btn4,btn5)
    bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)

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
@bot.callback_query_handler(func=lambda call:True)
def callback(callback):
    if callback.data == "repeat_convert":
        try:
            bot.send_message(callback.message.chat.id, '<b>Введите сумму</b>\nДля отмены введите cancel', parse_mode='html')
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
            bot.send_message(callback.message.chat.id, f'{amount}{values[0]} = {round(res,3)}{values[1]}', reply_markup=markup)
        except:
            bot.send_message(callback.message.chat.id,
                             '<b>Произошла ошибка, введите сумму заново.</b>\nДля отмены введите cancel\nЕсли ошибка повторится используйте /feedback',
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, convert_step2)
            return

    elif callback.data == 'else_curr':
        try:
            bot.send_message(callback.message.chat.id, 'Введите валюту в формате rub/usd (Ваша валюта/валюта  в которую нужно перевести)')
            bot.register_next_step_handler(callback.message, convert_step3)
        except:
            except:
            bot.send_message(callback.message.chat.id,
                             '<b>Произошла ошибка, введите сумму заново.</b>\nДля отмены введите cancel\nЕсли ошибка повторится используйте /feedback',
                             parse_mode='html')
            bot.register_next_step_handler(callback.message, convert_step2)
            return
bot.polling(none_stop=True)