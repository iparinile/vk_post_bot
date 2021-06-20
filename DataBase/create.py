import psycopg2


def create_tables():
    db = psycopg2.connect(dbname='data', user='postgres', password='1', host='localhost')
    cursor = db.cursor()

    cursor.execute('CREATE TABLE Users(\n'
                   'user_id INTEGER PRIMARY KEY NOT NULL)')

    cursor.execute("CREATE TABLE Posts(\n"
                   'id SERIAL PRIMARY KEY,\n'
                   'group_domain VARCHAR(30),\n'
                   'post_text VARCHAR(4100),\n'
                   'post_id VARCHAR(30),\n'
                   'post_date INTEGER)')

    db.commit()


if __name__ == '__main__':
    create_tables()
