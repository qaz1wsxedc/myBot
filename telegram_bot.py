
# -*- coding: utf-8 -*-

from requests.structures import CaseInsensitiveDict

import telebot

import requests

API_KEY = '6109825560:AAHrPjST6FmfJJA6KGfQMG8Ea1mKQp_yUeE'

POST_URLS = {
    'Fantasy Name': 'https://randomall.ru/api/general/fantasy_name',
    'Plot': 'https://randomall.ru/api/general/plot',
    'Saying': 'https://randstuff.ru/saying/generate/',
    'Number': 'https://randstuff.ru/number/',
}

print("Script enabled")

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 'Это бот предназначен для генерации текста и чисел.\n'\
                         'Вы можете использовать команду "/comands", чтобы получить список со всеми доступными командами.')


@bot.message_handler(commands=['comands'])
def comands(message):
    out = '{:<10} - получить случайная идея для сюжета\n'\
          '{:<10} - получить случайное имя\n'\
          '{:<10} - получить случайное высказывание\n'\
          '{:<10} - получить случайное число'.format("'/plot'", "'/name'", "'/saying'", "'/number'")
    bot.send_message(message.chat.id, out)


@bot.message_handler(commands=['plot'])
def plot(message):
    r = requests.post(POST_URLS['Plot'])
    bot.send_message(message.chat.id, r.text)


@bot.message_handler(commands=['name'])
def fantasy_name(message):
    r = requests.post(POST_URLS['Fantasy Name'])
    out = list(map(str.strip, r.text.replace('<br>', ' ').replace(
        '"', '').replace('  ', ' ') .split(' ')))
    try:
        bot.send_message(message.chat.id, out[0])
    except:
        bot.send_message(message.chat.id, out[1])


@bot.message_handler(commands=['saying'])
def saying(message):
    headers = CaseInsensitiveDict()
    headers["x-requested-with"] = "XMLHttpRequest"
    r = requests.post(POST_URLS['Saying'], headers=headers).json()['saying']
    saying = r['text']
    author = r['author']
    out = saying + '\n(c) ' + author
    bot.send_message(message.chat.id, out)


bot.polling(none_stop=True)

print("Script disabled")
