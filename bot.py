import time

import telebot
import data
# from main import *
from telebot import types

import main

bot = telebot.TeleBot(data.tg_api_token)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Ну что начнём?...".format(message.from_user))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton("Что я умею?")
    item2 = types.KeyboardButton("Приступить к работе")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Что делаем?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_send_message(message):
    if message.text == "Что я умею?":
        bot.send_message(message.chat.id, "Да особо нихуя :(")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item2 = types.KeyboardButton("Приступить к работе")

        bot.send_message(message.chat.id, "   ?", reply_markup=markup)
    elif message.text == "Приступить к работе":
        bot.send_message(message.chat.id, "Дай мне минутку проверю твою подписку...")
        user_id = message.from_user.id
        print(user_id)
        access = main.check_sub(user_id)
        print(access)
        time.sleep(2)

        if access == True:
            bot.send_message(message.chat.id, "⭐ ️Кажется всё в проядке! Хорошей погоды на рынке...")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            menu1 = types.KeyboardButton("Изменить таргет процент")
            menu2 = types.KeyboardButton("Посмотреть курс монеты")

            markup.add(menu1, menu2)

            bot.send_message(message.chat.id, "Выбери один из пунктов", reply_markup=markup)

            @bot.message_handler(content_types=['text'])
            def change_procent(message):
                if message.text == "Изменить таргет процент":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                    item1 = types.KeyboardButton("3%")
                    item2 = types.KeyboardButton("3%")
                    item3 = types.KeyboardButton("3.5%")
                    item4 = types.KeyboardButton("3.7%")
                    item5 = types.KeyboardButton("4%")
                    item6 = types.KeyboardButton("4.5%")

                    markup.add(item1, item2, item3, item4, item5, item6)

                    bot.send_message(message.chat.id, "Выбери один из пунктов", reply_markup=markup)

                if message.text == "3%":
                    bot.send_message(message.chat.id, "Процет поменял, перезапускаю отслеживание разанцы с 3%...")

                        # main.main(3)

        elif access == False:
            bot.send_message(message.chat.id, "Упс кажется у Вас нет подиски 😳")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item1 = types.KeyboardButton("Купить подписку 🤑")
            item2 = types.KeyboardButton("Пробный период 🙉")

            markup.add(item1, item2)

            bot.send_message(message.chat.id, "Возможнные варианты", reply_markup=markup)

    if message.text == 'Купить подписку 🤑':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton("START 1$/месяц 🥸")
        item2 = types.KeyboardButton("MEDIUM 5$/месяц 🙂")
        item3 = types.KeyboardButton("GOLD 10$/мксяц 🤩")
        item4 = types.KeyboardButton("⬅️ Назад")

        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "😘 Выбери удобную подписку", reply_markup=markup)

    if message.text == "⬅️ Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item1 = types.KeyboardButton("Купить подписку 🤑")
        item2 = types.KeyboardButton("Пробный период 🙉")

        markup.add(item1, item2)

        bot.send_message(message.chat.id, "Возможнные варианты", reply_markup=markup)





bot.polling(none_stop=True)
