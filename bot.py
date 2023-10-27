import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import sqlite3
from env import bot
from functions import sql
from parsing import picture, information, years, reiti

i = 0


@bot.message_handler(commands=['start'])
def start(message):
    sql()
    markup = types.InlineKeyboardMarkup()
    item_film = types.InlineKeyboardButton('Нажать', callback_data='peremen')
    markup.add(item_film)
    bot.send_message(message.chat.id, 'Нажми, чтобы посмотреть подборку фильмов', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global i
    i = 0
    if callback.data == 'peremen':
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('следующая страница'))
        bot.send_message(callback.message.chat.id, 'Незабудьте добавить понравившиеся фильмы в свой список',
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text(message):
    global i, k
    if message.text == 'следующая страница':
        i += 5
        on_click(message, i)
        delete(message)
    if message.text == 'предыдущая страница':
        i -= 5
        on_click(message, i)
        delete(message)
    if message.text == 'Добавить фильм в список':
        k = i
        knopki(message, k)
    if message.text == 'Посмотреть список':
        for q in range(6, 4, -1):
            bot.delete_message(message.chat.id, message.message_id - q)
        k = i
        sp(message)



def knopki(message, k):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('1'), types.KeyboardButton('2'),
               types.KeyboardButton('3'), types.KeyboardButton('4'),
               types.KeyboardButton('5'))
    bot.send_message(message.chat.id, 'Какой фильм хотите добавить в свой список?', reply_markup=markup)
    bot.register_next_step_handler(message, film, k)

@bot.message_handler(content_types=['text'])
def sp(message):

    conn = sqlite3.connect('database/data.db')
    cur = conn.cursor()
    cur.execute("SELECT films FROM users WHERE name= ?", (message.from_user.username,))
    b = []
    c = []
    p = 0
    for res in cur:
        b.append(res)
        p += 1
    if b != []:
        for l in range(p):
            c.append(b[l][0])
        text = '\n'.join(c)
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Упс, кажется ваш список пуст, добавьте понравившиейся Вам фильм!')

@bot.message_handler(content_types=['text'])
def film(message, k):
    for q in range(8, 1, -1):
        bot.delete_message(message.chat.id, message.message_id - q)
    nomer = message.text.strip()
    choose_film = a[int(nomer) - 1]
    bot.send_message(message.chat.id, 'Отлично фильм занесен в список')
    on_click(message, k)
    conn = sqlite3.connect('database/data.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (films, name) VALUES (?, ?);', (choose_film, message.from_user.username,))
    conn.commit()
    cur.close()
    conn.close()


def delete(message):
    for k in range(6, -1, -1):
        if i >= 5:
            bot.delete_message(message.chat.id, message.message_id - k)


def on_click(message, i):
    global a
    a = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if i <= 50:
        markup.add(types.KeyboardButton('следующая страница'))
    if i > 5:
        markup.add(types.KeyboardButton('предыдущая страница'))
    markup.add(types.KeyboardButton('Добавить фильм в список'))
    markup.add(types.KeyboardButton('Посмотреть список'))
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(picture[i - 5],
                                                                 caption=f'1. {information[i - 5]}, {years[i - 5]} Рейтинг: {reiti[i - 5]} \n \n'
                                                                         f'2. {information[i - 4]}, {years[i - 4]} Рейтинг: {reiti[i - 4]} \n \n'
                                                                         f'3. {information[i - 3]}, {years[i - 3]} Рейтинг: {reiti[i - 3]} \n \n'
                                                                         f'4. {information[i - 2]}, {years[i - 2]} Рейтинг: {reiti[i - 2]} \n \n'
                                                                         f'5. {information[i - 1]}, {years[i - 1]} Рейтинг: {reiti[i - 1]} \n \n'),
                                           types.InputMediaPhoto(picture[i - 4]),
                                           types.InputMediaPhoto(picture[i - 3]),
                                           types.InputMediaPhoto(picture[i - 2]),
                                           types.InputMediaPhoto(picture[i - 1])])
    bot.send_message(message.chat.id, '---------------------------------', reply_markup=markup)
    for j in range(5, 0, -1):
        a.append(information[i - j])


bot.infinity_polling()
