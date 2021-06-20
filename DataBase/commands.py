import psycopg2


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


def delete_unnecessary_posts(group_domain: str, cursor, db):
    last_post_date = get_last_post_date(group_domain, cursor)
    if last_post_date != 0:
        cursor.execute(f"DELETE FROM posts WHERE group_domain='{group_domain}' AND post_date!='{last_post_date}'")
    db.commit()


def is_text_not_in_db(post_text: str, cursor):
    cursor.execute(f"SELECT id FROM posts WHERE post_text='{post_text}'")
    try:
        data = cursor.fetchall()[0][0]
    except IndexError:
        return True
    if post_text == '':
        return True
    return False


if __name__ == '__main__':
    db = psycopg2.connect(dbname='data', user='postgres', password='1', host='localhost')
    cursor = db.cursor()
    print(is_text_not_in_db('привето', cursor))
