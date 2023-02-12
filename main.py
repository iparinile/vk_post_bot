import psycopg2
from psycopg2.errors import InFailedSqlTransaction, SyntaxError
import telebot
from telebot.types import InputMediaPhoto
import threading
from datetime import datetime
from time import sleep
import os
from dotenv import load_dotenv

from DataBase.commands import add_post, get_last_post_date, get_all_users, \
    delete_unnecessary_posts, is_text_not_in_db, delete_old_adverts
from Requests_to_VK.get_posts import get_post, edit_post_to_correct
from requests_to_trubamet.get_posts import get_posts_from_trubamet

load_dotenv()

bot = telebot.TeleBot(os.getenv('bot_token'))
db = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = db.cursor()

owners_id = {'-115081032': 'bu_truba_zovet'}


def search_new_posts():
    threading.Timer(1 * 60.0, search_new_posts).start()  # Перезапуск через 1 минуту

    for owner in owners_id.items():

        try:
            last_post_date = get_last_post_date(owner[0], cursor)

            current_time = datetime.now().time()
            if (current_time.hour == 1) and (0 <= current_time.minute <= 3):  # Если время 01:00 - 01:05
                delete_unnecessary_posts(owner[0], last_post_date, cursor, db)
                delete_old_adverts(db, cursor)

            users = get_all_users(cursor)
            if len(users) > 0:
                adverts = get_posts_from_trubamet(db, cursor)
                for advert in adverts:
                    bot.send_message(users[0], advert)

                posts = get_post(owner_id_of_group=owner, data_of_last_post=last_post_date, count_of_posts=10)
                for post in posts:

                    post_text = edit_post_to_correct(post)['text']

                    if len(post_text) == 0:
                        post_text = ['']

                    try:
                        if is_text_not_in_db(post_text[0], cursor):

                            images_array = post['image_url']

                            for user_id in users:

                                sleep(0.5)

                                if len(images_array) == 1:
                                    if (post_text[0] == '') and (len(post_text) == 1):
                                        bot.send_photo(chat_id=user_id, photo=images_array[0])
                                    else:
                                        bot.send_photo(chat_id=user_id, photo=images_array[0],
                                                       caption=post_text[0])
                                        if len(post_text) > 1:
                                            for text in post_text[1:]:
                                                if text != '':
                                                    bot.send_message(chat_id=user_id, text=text)

                                elif len(images_array) > 1:
                                    if (post_text[0] == '') and (len(post_text) == 1):
                                        media = [InputMediaPhoto(images_array[0])]
                                        for image in images_array[1:]:
                                            media.append(InputMediaPhoto(image))
                                        bot.send_media_group(chat_id=user_id, media=media)
                                    else:
                                        media = [InputMediaPhoto(images_array[0],
                                                                 caption=post_text[0])]
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
                                            bot.send_message(chat_id=user_id, text=post_text[0])
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
                    except SyntaxError:
                        cursor.execute("ROLLBACK")
                        db.commit()
        except InFailedSqlTransaction:
            cursor.execute("ROLLBACK")
            db.commit()


try:
    search_new_posts()
except InFailedSqlTransaction:
    cursor.execute("ROLLBACK")
    db.commit()

bot.polling(none_stop=True)
