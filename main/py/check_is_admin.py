def check_info_adm(user, p1, p2):
    global information
    if user == True and p1 in p2:
        information = '''
<b>information:</b>
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
/weather - Узнать погоду
/weather_users_info - Список городов (для администрации)
/DeleteMsg - удалить сообщения (для администрации) (багает)
/text_to_audio - Перевод текста в аудио
/Send_Message - Отправить сообщение на любой id (Для администрации)
/reports - просмотр и закрытие репортов (для администрации)
/send_all - отправить всем (для администрации)
/convert_currency - конвертатор валют
/vip_info - информация о вип
/buy_vip - купить вип
/get_vip - выдать вип (для администрации)
/rem_vip - удалить vip комуто (для администрации)
/check_orders - Заказы ботов (для администрации)
/bot_shop - Заказать телеграмм бота
Так-же ты можешь отправить мне фото!
'''
    else:
        information = '''
<b>information:</b>
/start - Старт бота
/help - Помощь
/id - Узнать ваш id в telegram
/bot_shop - Заказать телеграмм бота
/website - Открыть сайт
/photo - Я отправлю вам фото
/audio - Я отправлю вам аудио
/example - Решить пример
/feedback - связь с разработчиком
/auth - Вход в аккаунт
/reg - Регистрация
/leave - Выход с аккаунта
/status - Статус
/weather - Узнать погоду
/text_to_audio - Перевод текста в аудио
/convert_currency - конвертатор валют
/vip_info - информация о вип
/buy_vip - купить вип
Так-же ты можешь отправить мне фото!

<b>У нас можно преобрести качественного tg-бота /bot_shop</b>
'''
    return information
