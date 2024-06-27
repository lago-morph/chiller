from chiller_api.db import db
import pprint

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

# get the user name given the id
def get_user_name(user_id):
    print('get user name', user_id)
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM user WHERE id = ?", (user_id,))
    result = cur.fetchone()
    cur.close()
    if result is not None:
        print('   user name:', result[0])
        return result[0]
    else:
        print('   user name not found')
        return None

# look up the user id given the name
def get_user_id(name):
    print('get user id', name)
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM user WHERE name = ?", (name,))
    result = cur.fetchone()
    cur.close()
    if result is not None:
        print('   user id:', result[0])
        return result[0]
    else:
        print('   user id not found')
        return None

def add_movie_list(user_id, title):
    conn = db.get_db()
    try:
        conn.execute("INSERT INTO movielist (user_id, title) VALUES (?,?)", (user_id, title,))
        conn.commit()
    except conn.IntegrityError:
        return False
    else:
        return True

# gets all movies for a given user
def get_movielist(user_id):
    print('get user list for user id', user_id)
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT title FROM movielist WHERE user_id = ?", (user_id,))
    result = cur.fetchall()
    cur.close()

    if len(result) == 0:
        print('   no movies in list')
    else:
        print('   user list result')
        pprint.pp(result)

    return result
