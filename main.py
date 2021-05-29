import sqlite3
import telebot
import threading

from DataBase.commands import add_user

bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
db = sqlite3.connect('DataBase/data.sqlite', check_same_thread=False)
cursor = db.cursor()


@bot.message_handler(commands=["start"])
def start(message):
    try:
        add_user(message.chat.id, cursor, db)
    except ValueError:
        print('Что-то пошло не так')
    bot.send_message(message.chat.id, 'Привет! Я записал тебя в свой список. Теперь я буду твоим рабом')


def async_function():
    threading.Timer(5.0, async_function).start()  # Перезапуск через 5 секунд
    print("Hello, world!")
    bot.send_message(813672369, 'Я пишу это каждые 5 секунд')


async_function()

bot.polling()
