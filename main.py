import psycopg2
import telebot
from telebot.types import InputMediaPhoto
import threading
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv

from DataBase.commands import add_user, add_post, get_last_post_date, is_user_already_recorded, get_all_users, \
    delete_unnecessary_posts, is_text_not_in_db
from Requests_to_VK.get_posts import get_post, edit_post_to_correct

load_dotenv()

bot = telebot.TeleBot(os.getenv('bot_token'))
db = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = db.cursor()

owners_id = {'-115081032': 'bu_truba_zovet', '-203046727': 'translom_pererabotka', '-28483397': 'truba24club',
             '-89513171': 'prodam_trubu', '-152238835': 'transfer1tube', '-66234848': 'tryba_by_vosstanovlenay',
             '-116166768': 'public116166768',
             '-40447148': 'nelikvid', '324213859': 'id324213859', '530570695': 'neewtruba',
             '-161503615': 'club161503615'}


@bot.message_handler(commands=["start"])
def start(message):
    try:
        if is_user_already_recorded(message.chat.id, cursor):
            bot.send_message(message.chat.id, 'Я уже запомнил тебя')
        else:
            add_user(message.chat.id, cursor, db)
            bot.send_message(message.chat.id, 'Привет! Я записал тебя в свой список')
    except psycopg2.Error:
        print('прилетела ошибка')
        cursor.execute('END TRANSACTION;')


def search_new_posts():
    threading.Timer(1 * 60.0, search_new_posts).start()  # Перезапуск через 1 минуту

    for owner in owners_id.items():

        last_post_date = get_last_post_date(owner[0], cursor)

        current_time = datetime.now().time()
        if (current_time.hour == 1) and (0 <= current_time.minute <= 3):  # Если время 01:00 - 01:05
            delete_unnecessary_posts(owner[0], last_post_date, cursor, db)

        users = get_all_users(cursor)
        if len(users) > 0:
            posts = get_post(owner_id_of_group=owner, data_of_last_post=last_post_date, count_of_posts=10)
            for post in posts:

                post_text = edit_post_to_correct(post)['text']
                if len(post_text) == 0:
                    post_text = ['']

                if is_text_not_in_db(post_text[0], cursor):

                    images_array = post['image_url']

                    for user_id in users:

                        sleep(0.5)

                        if len(images_array) == 1:
                            if (post_text[0] == '') and (len(post_text) == 1):
                                bot.send_photo(chat_id=user_id, photo=images_array[0], caption=post['link'])
                            else:
                                bot.send_photo(chat_id=user_id, photo=images_array[0],
                                               caption=post['link'] + '\n' + post_text[0])
                                if len(post_text) > 1:
                                    for text in post_text[1:]:
                                        if text != '':
                                            bot.send_message(chat_id=user_id, text=text)

                        elif len(images_array) > 1:
                            if (post_text[0] == '') and (len(post_text) == 1):
                                media = [InputMediaPhoto(images_array[0], caption=post['link'] + '\n')]
                                for image in images_array[1:]:
                                    media.append(InputMediaPhoto(image))
                                bot.send_media_group(chat_id=user_id, media=media)
                            else:
                                media = [InputMediaPhoto(images_array[0], caption=post['link'] + '\n' + post_text[0])]
                                for image in images_array[1:]:
                                    media.append(InputMediaPhoto(image))
                                bot.send_media_group(chat_id=user_id, media=media)
                                if len(post_text) > 1:
                                    for text in post_text[1:]:
                                        if text != '':
                                            bot.send_message(chat_id=user_id, text=text)
                        elif len(images_array) == 0:
                            try:
                                if post_text[0] != '':
                                    bot.send_message(chat_id=user_id, text=post['link'] + '\n' + post_text[0])
                            except IndexError:
                                pass
                            try:
                                for text in post_text[1:]:
                                    if text != '':
                                        bot.send_message(chat_id=user_id, text=text)
                            except ValueError:
                                pass
                    add_post(
                        group_domain=owner[0],
                        post_text=post_text[0],
                        post_id=post['post_id'],
                        post_date=post['date'],
                        cursor=cursor,
                        db=db
                    )


search_new_posts()

bot.polling(none_stop=True)
