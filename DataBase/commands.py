from time import sleep

import psycopg2
from psycopg2.errors import SyntaxError

from Requests_to_VK.get_posts import get_post

owners_id = {'-115081032': 'bu_truba_zovet', '-203046727': 'translom_pererabotka', '-28483397': 'truba24club',
             '-89513171': 'prodam_trubu', '-152238835': 'transfer1tube', '-66234848': 'tryba_by_vosstanovlenay',
             '-116166768': 'public116166768', '-17083336': 'club17083336', '-80026197': 'metalopt',
             '-40447148': 'nelikvid', '324213859': 'id324213859', '530570695': 'neewtruba',
             '-161503615': 'club161503615', '-177235715': 'truba.bu_ot159_1420'}


def add_user(user_id: int, cursor, db):
    cursor.execute(f"INSERT INTO Users (user_id) VALUES ({user_id})")
    db.commit()


def is_user_already_recorded(user_id: int, cursor) -> bool:
    cursor.execute(f"SELECT user_id FROM Users WHERE user_id='{user_id}'")
    try:
        data = cursor.fetchall()[0][0]
    except IndexError:
        return False
    if user_id == data:
        return True
    else:
        return False


def get_last_post_date(group_domain: str, cursor) -> int:
    cursor.execute(f"SELECT MAX(post_date) FROM Posts WHERE group_domain='{group_domain}'")
    data = cursor.fetchall()[0][0]
    if data is None:
        return 0
    else:
        return data


def add_post(group_domain: str, post_id: str, post_date: int, post_text: str, cursor, db):
    cursor.execute(f"INSERT INTO Posts (group_domain,post_text,post_id,post_date) "
                   f"VALUES ('{group_domain}','{post_text}','{post_id}', '{post_date}')")
    db.commit()


def get_all_users(cursor):
    cursor.execute("SELECT DISTINCT user_id FROM Users")
    data = cursor.fetchall()
    users = []
    if len(data) > 0:
        for user in data:
            users.append(user[0])
    return users


def delete_unnecessary_posts(group_domain: str, last_post_date: int, cursor, db):
    if last_post_date != 0:
        cursor.execute(f"DELETE FROM posts WHERE group_domain='{group_domain}' AND post_date!={last_post_date}")
    db.commit()


def is_text_not_in_db(post_text: str, cursor):
    cursor.execute(f"SELECT id FROM posts WHERE post_text='{post_text}'")
    try:
        data = cursor.fetchall()[0][0]
    except IndexError:
        return True
    except SyntaxError:
        return False
    if post_text == '':
        return True
    return False


def is_advert_id_not_in_db(advert_id: str, cursor) -> bool:
    cursor.execute(f"SELECT post_id FROM trubamet WHERE post_id='{advert_id}'")
    data = cursor.fetchone()
    if data is None:
        return True
    else:
        return False


def add_advert_id_to_db(advert_id: str, db, cursor) -> None:
    cursor.execute(f"INSERT INTO trubamet (post_id, create_at) VALUES ('{advert_id}', CURRENT_TIMESTAMP)")
    db.commit()


def delete_old_adverts(db, cursor) -> None:
    cursor.execute(f"DELETE FROM trubamet WHERE create_at<(CURRENT_TIMESTAMP - INTERVAL '30 DAY')")
    db.commit()


if __name__ == '__main__':
    db = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/vk_to_telegram")
    cursor = db.cursor()

    delete_old_adverts(db, cursor)
