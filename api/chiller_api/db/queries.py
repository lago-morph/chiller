from psycopg import IntegrityError
from chiller_api.db import db
import pprint

def add_user(name):
    conn = db.get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
    except IntegrityError:
        return False

    return True

# get the user name given the id
def get_user_name(user_id):
    print('get user name', user_id)
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cur.fetchone()
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
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE name = %s", (name, ))
        result = cur.fetchone()
    if result is not None:
        print('   user id:', result[0])
        return result[0]
    else:
        print('   user id not found')
        return None

def add_movie_list(user_id, title):
    conn = db.get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO movielist (user_id, title) VALUES (%s, %s)", (user_id,title,))
            conn.commit()
    except IntegrityError:
        return False

    return True

# gets all movies for a given user
def get_movielist(user_id):
    print('get user list for user id', user_id)
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT title FROM movielist WHERE user_id = %s",(user_id,))
        result = cur.fetchall()
    if len(result) == 0:
        print('   no movies in list')
    else:
        print('   user list result')
        pprint.pp(result)

    return result
