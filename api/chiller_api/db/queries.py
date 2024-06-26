from chiller_api.db import db

def add_user(name):
    print(name)
    conn = db.get_db()
    try:
        conn.execute("INSERT INTO user (name) VALUES (?)", (name,))
        conn.commit()
    except conn.IntegrityError:
        return False
    else:
        return True

