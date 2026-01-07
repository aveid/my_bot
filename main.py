from decouple import config
import telebot
from telebot import types
from constant_text import NAMES

bot_token = config("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start","привет"])
def start(message):
    send_text = f"Привет {message.chat.first_name}\n" \
                f"Я бот который помогает найти дату " \
                f"рождения твоих коллег\n" \
                f"Выбери пожалуйста имя сотрудника!"
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    murkup.add(types.KeyboardButton("Jibek"))
    murkup.add(types.KeyboardButton("Atai"))
    murkup.add(types.KeyboardButton("Erbol"))
    bot.reply_to(message, send_text, reply_markup=murkup)

@bot.message_handler(func=lambda message : True)
def get_text(message):
    name = message.text
    birth_date = NAMES.get(name).get("date")
    response_text = "Нечего не найдено!"
    if birth_date:
        response_text = f"Коллега по имени {name}\n" \
                        f"родилась {birth_date}"
        keyboard = types.InlineKeyboardMarkup()
        button_save = types.InlineKeyboardButton(text="Фамилия",
                                                         callback_data='last_name')
        button_change = types.InlineKeyboardButton(text="Департамент",
                                                           callback_data='department')
        url = NAMES.get(name).get("url")
        button_url = types.InlineKeyboardButton(text="Биография",
                                    url=url)

        keyboard.add(button_save, button_change, button_url)
    bot.reply_to(message, response_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'last_name')
def get_last_name(call):
    message = call.message.reply_to_message.text
    last_name = NAMES.get(message).get("last_name")
    bot.send_message(call.message.chat.id, last_name)

@bot.callback_query_handler(func=lambda call: call.data == 'department')
def get_last_name(call):
    message = call.message.reply_to_message.text
    department = NAMES.get(message).get("department")
    bot.send_message(call.message.chat.id, department)

bot.polling()