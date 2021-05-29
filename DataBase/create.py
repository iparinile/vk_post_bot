import sqlite3


def create_tables():
    db = sqlite3.connect('data.sqlite')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE Users(\n'
                   'user_id INTEGER PRIMARY KEY NOT NULL)')

    cursor.execute("CREATE TABLE Posts(\n"
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n'
                   'group_domain VARCHAR(30),\n'
                   'post_id VARCHAR(30),\n'
                   'post_text VARCHAR(30),\n'
                   'post_date INTEGER)')

    db.commit()


if __name__ == '__main__':
    create_tables()
