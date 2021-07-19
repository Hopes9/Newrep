# -*- coding: utf8 -*-

from os import system
from sys import platform
import random
import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from db import dbworker

db = dbworker()

if platform.lower() == 'win32':
    system('cls')
else:
    system('clear')


bot = telebot.TeleBot('1808896589:AAFFt6r5V1dKhjp6dpy0T9CM2ou7CIbe_40')


def f():
    pass


def create_main_db():
    markup = InlineKeyboardMarkup()
    for i in db.return_all_shop():
        markup.add(InlineKeyboardButton(
            f'{i[1]} | На складе: {i[2]} Цена: {i[3]}', callback_data=f'buy_{i[0]}_{i[2]}_{i[3]}'))
    return markup


@bot.callback_query_handler(f())
def callback(call):
    markup = InlineKeyboardMarkup()
    data = call.data
    print(data)
    if data.split('_')[0] == 'buy':
        markup.add(InlineKeyboardButton(
            f'Купить', callback_data=f'buynow_{data.split("_")[1]}'))
        bot.edit_message_text(
            text=f'{db.return_name_by_id(data.split("_")[1])}', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif data.split('_')[0] == 'buynow':
        product = db.return_about_product(data.split("_")[1])
        if db.chek_money(call.from_user.id)[0][0] > product[0][2]:
            db.update_money(call.from_user.id, product[0][2])
            db.buy_product(data.split("_")[1])

            markup.add(InlineKeyboardButton(
                f'Купить ещё?', callback_data=f'buymore'))
            bot.edit_message_text(text=f'Товар куплен', chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, reply_markup=markup)
        else:
            bot.edit_message_text(
                text=f'Денег нет', chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif data == 'buymore':
        # bot.edit_message_text(text=f'Товар куплен', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_main_db())


@bot.message_handler(commands=['start'])
def start_messages(message):
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Список товаров📖'))
    if len(db.chek_users(message.from_user.id)) == 0:
        db.insert_into_db(message.from_user.id,
                          f'{message.chat.first_name} {message.chat.last_name}')

    bot.send_message(message.chat.id, 'Магазин', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Список товаров📖':

        bot.send_message(text=f'Список товаров📖',
                         chat_id=message.chat.id, reply_markup=create_main_db())
        # db.create_random_product(20)


bot.polling()
