def add_user(user_id, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Users (user_id) VALUES ({user_id})")
    db.commit()

def add_post(group_domain, post_id,post_text,post_date, cursor,db):
    cursor.execute(f"INSERT INTO Posts(group_domain, post_id,post_text,post_date) VALUES ({group_domain},{post_id},{post_text},{post_date})")
    db.commit()
