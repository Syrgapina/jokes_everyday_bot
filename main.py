# Импортирую необходимые библиотеки
import telebot
import requests
import base64
from PIL import Image


# Функция для изменения размера картинок
def size_img(image_path):
    img = Image.open(image_path)
    # пропорциональное изменение картинки
    img.thumbnail(size=(600, 600))
    img.save(image_path)


# Токен чат-бота
TOKEN = '6136532365:AAGv5TdaVjnHm1xx-sknPtFh0qlMch7UYdM'

# Инициализирую бота, передав в него токен, полученный от BotFather
bot = telebot.TeleBot(TOKEN)


# Реакция на команду start
@bot.message_handler(commands=['start'])
def start(message):
    img = open('mr-bean-funny.gif', 'rb')
    bot.send_video(message.chat.id, img)
    img.close()
    bot.send_message(message.chat.id, text=f'Приветствую, {message.from_user.username}!'
                                           f'\n\nЯ чат-бот, который может тебя развеселить. Просто отправляй команды:'
                                           f'\n/new_joke или\n/joke_picture')


# Выдаем шутку в виде текста и переводим
@bot.message_handler(commands=['new_joke'])
def get_joke(message):
    url = 'https://dad-jokes.p.rapidapi.com/random/joke'
    headers = {
        "X-RapidAPI-Key": "17246431e5msh3bab630222204dbp10f9bfjsnc41b02f79d11",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        setup = data["body"][0]['setup']
        punchline = data["body"][0]['punchline']
        joke = f'- {setup}\n- {punchline}'
        bot.send_message(message.chat.id, joke)
        url_translate = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        payload = f"q={joke}&target=ru"
        headers_translate = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Key": "8630f618ffmsh951673e861edf65p1dea6ejsncdd5bced8059",
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
        }
        response = requests.request("POST", url_translate, data=payload.encode('utf-8'), headers=headers_translate)
        if response.status_code == 200:
            joke_translation = response.json()['data']['translations'][0]['translatedText']
            bot.send_message(message.chat.id, joke_translation)
            # print(joke_translation)
        return joke
    else:
        bot.send_message(message.chat.id, 'проблемы с API сайта')


# Выдаем шутку в виде картинки
@bot.message_handler(commands=['joke_picture'])
def joke_picture(message):
    url = "https://dad-jokes.p.rapidapi.com/random/joke/png"
    headers = {
        "X-RapidAPI-Key": "17246431e5msh3bab630222204dbp10f9bfjsnc41b02f79d11",
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    r = requests.get(url=url, headers=headers)

    if r.status_code == 200:
        data = r.json()
        picture = data["body"]["image"].split(',')[1]

        with open('file.png', 'wb') as img:
            img_name = base64.b64decode(picture, '!-')
            img.write(img_name)

        size_img('file.png')

        with open('file.png', 'rb') as img:
            bot.send_photo(message.chat.id, img)
    else:
        bot.send_message(message.chat.id, 'проблемы с API сайта')


bot.polling(none_stop=True)
