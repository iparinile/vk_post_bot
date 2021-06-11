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
        print(data)
        return False


def get_last_post_date(group_domain: str, cursor) -> int:
    cursor.execute(f"SELECT MAX(post_date) FROM Posts WHERE group_domain='{group_domain}'")
    data = cursor.fetchall()[0][0]
    if data is None:
        return 0
    else:
        return data


def add_post(group_domain: str, post_id: str, post_date: int, cursor, db):
    cursor.execute(f"INSERT INTO Posts (group_domain,post_id,post_date) "
                   f"VALUES ('{group_domain}', '{post_id}', '{post_date}')")
    db.commit()


def get_all_users(cursor):
    cursor.execute("SELECT DISTINCT user_id FROM Users")
    data = cursor.fetchall()
    users = []
    if len(data) > 0:
        for user in data:
            users.append(user[0])
    return users


if __name__ == '__main__':
    db = psycopg2.connect(dbname='data', user='postgres', password='1', host='localhost')
    cursor = db.cursor()
    print(get_all_users(cursor))
