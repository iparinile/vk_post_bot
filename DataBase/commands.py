def add_user(user_id, cursor, db):
    cursor.execute(f"INSERT OR IGNORE INTO Users (user_id) VALUES ({user_id})")
    db.commit()
