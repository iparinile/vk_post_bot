import sqlite3
import telebot
import threading

from DataBase.commands import add_user, add_post, get_last_post_date
from Requests_to_VK.get_posts import get_post

bot = telebot.TeleBot('1742929878:AAExqh7JcRATPAFr7iVc5pv9OE8B8eebDYQ')
db = sqlite3.connect('DataBase/data.sqlite', check_same_thread=False)
cursor = db.cursor()

domains = ['bu_truba_zovet', 'translom_pererabotka', 'prodam_trubu', 'transfer1tube', 'tryba_by_vosstanovlenay',
           'public116166768', 'club17083336', 'metalopt', 'nelikvid', 'onamazov2014', 'id324213859', 'neewtruba']


@bot.message_handler(commands=["start"])
def start(message):
    try:
        add_user(message.chat.id, cursor, db)
    except ValueError:
        print('Что-то пошло не так')
    bot.send_message(message.chat.id, 'Привет! Я записал тебя в свой список. Теперь я буду твоим рабом')


def search_new_posts():
    threading.Timer(10.0, search_new_posts).start()  # Перезапуск через 10 секунд

    for domain in domains:
        last_post_date = get_last_post_date(domain, cursor)
        posts = get_post(owner_id_of_group=domain, data_of_last_post=last_post_date, count_of_posts=10)
        print(domain)
        for post in posts:
            add_post(
                group_domain=domain,
                post_id=post['post_id'],
                post_text=post['text'],
                post_date=post['date'],
                cursor=cursor,
                db=db
            )

            bot.send_message(813672369, post['text'])


search_new_posts()

bot.polling()
