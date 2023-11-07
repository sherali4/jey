import sqlite3

db = sqlite3.connect('bot_lite.sqlite')
cursor = db.cursor()

def is_superadmin(user, menyu = '-'):
    try:
        cursor.execute("SELECT * FROM 'admin' WHERE id_user=?", (user,))
        user = cursor.fetchone()
        if not user:
            return False
        elif user[2]==1:
            return True
        else:
            menyular = user[4].split(sep=', ')
            if menyu in menyular:
                return True
            else:
                return False
            # return False

        # db.close()
    except:
        pass


