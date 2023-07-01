def check_info_adm(user):
    global information
    if user == True:
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
/TextToAudio - Перевод текста в аудио
/Send_Message - Отправить сообщение на любой id (Для администрации)
/reports - просмотр и закрытие репортов (для администрации)
Так-же ты можешь отправить мне фото!
'''
    else:
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
/leave - Выход с аккаунта
/status - Статус
/weather - Узнать погоду
/TextToAudio - Перевод текста в аудио
Так-же ты можешь отправить мне фото!
'''
    return information
