def add_user(user_id: int, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Users (user_id) VALUES ({user_id})")
    db.commit()


def get_last_post_date(group_domain: str, cursor) -> int:
    cursor.execute(f"SELECT MAX(post_date) FROM Posts WHERE group_domain='{group_domain}'")
    data = cursor.fetchall()[0][0]
    if data is None:
        return 0
    else:
        return data


def add_post(group_domain, post_id, post_text, post_date, cursor, db):
    params = (group_domain, post_id, post_text, post_date)
    cursor.execute(
        "INSERT INTO Posts (group_domain,post_id,post_text,post_date) VALUES (?, ?, ?, ?)", params)
    db.commit()
