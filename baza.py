import sqlite3

async def db_connect()-> None:
    global db, cur
    db = sqlite3.connect('bot_lite.sqlite')
    cur = db.cursor()
    # cur.execute('CREATE TABLE IF NOT EXISTS products(name TEXT, photo TEXT)')
    db.commit()

database = sqlite3.connect('bot_lite.sqlite')
cursor = database.cursor()

async def add_zakaz(id_client, id_tovar):
    cursor.execute("INSERT INTO zakaz (id_client, id_tovar) VALUES (?, ?)", (id_client, id_tovar,))
    database.commit()
def zakaz_otmen(id_client, id_tovar, user_id):
    cursor.execute('UPDATE zakaz SET sotib_olishi = 2,  delete_user = ? WHERE id_client= ? AND id_tovar = ?', (int(user_id), int(id_client), int(id_tovar),))
    database.commit()

def tovar_spy(id, user_id):
    try:
        cursor.execute('UPDATE tovar SET status = 2, user_id= ? WHERE id= ?', (int(user_id), int(id),))
        database.commit()
    except:
        pass

def zakaz_oladi(id_client, id_tovar, user_id):
    cursor.execute('UPDATE zakaz SET sotib_olishi = 1,  delete_user = ? WHERE id_client= ? AND id_tovar = ?', (int(user_id), int(id_client), int(id_tovar),))
    database.commit()



async def add_item(state):
    async with state.proxy() as data:
        # print(tuple(data.values()))
        send = tuple(data.values())
        cursor.execute("INSERT INTO tovar (turi, name, ulchov, narx, tarifi, photo, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (send[0], send[1], send[2], send[3], send[4], send[5], send[6],))
        # cursor.execute("INSERT INTO tovar (name, ulchov, narx, photo, tarifi) VALUES (?, ?, ?, ?, ?)", (data['name'], data['ulchov'], data['narx'], data['photo'], data['tarifi']))
        database.commit()


async def add_admin(state):
    async with state.proxy() as data:
        # print(tuple(data.values()))
        send = tuple(data.values())
        cursor.execute("INSERT INTO admin (id_user, ifo, tovar_turi, menyu) VALUES (?, ?, ?, ?)", (send[0], send[1], send[2], send[3],))
        # cursor.execute("INSERT INTO tovar (name, ulchov, narx, photo, tarifi) VALUES (?, ?, ?, ?, ?)", (data['name'], data['ulchov'], data['narx'], data['photo'], data['tarifi']))
        database.commit()
# cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, numb INTEGER)')
# database.commit()
    database.close()


async def add_tovar_turi_bazaga(state):

    async with state.proxy() as data:
        # print(tuple(data.values()))
        send = tuple(data.values())
        cursor.execute("INSERT INTO tovar_turi (tovar_turi, izoh) VALUES (?, ?)", (send[0], send[1],))
        # cursor.execute("INSERT INTO tovar (name, ulchov, narx, photo, tarifi) VALUES (?, ?, ?, ?, ?)", (data['name'], data['ulchov'], data['narx'], data['photo'], data['tarifi']))
        database.commit()
        # database.close()


def add_tovar(message):
    cursor.execute('INSERT INTO tovar (name) VALUES(?);', (message,))
    database.commit()

def katalog():
    cursor.execute("SELECT * FROM tovar")
    tovar = cursor.fetchall()
    for x in range(len(tovar)):
        print(x)


def delete_tovar(message):
    cursor.execute("DELETE FROM tasks WHERE id=?", (message,))
    database.commit()


def delete_tovar_turi(message):
    cursor.execute("DELETE FROM tovar_turi WHERE tovar_turi=?", (message,))
    database.commit()


def add_user(message):
    try:
        cursor.execute("SELECT * FROM 'users' WHERE id =?", (message.chat.id,))
        user = cursor.fetchone()
        # print(message.from_user.language_code)
        if not user:
            cursor.execute('INSERT INTO users (id, name, numb, lang) VALUES(?, ? ,?, ?);', (message.chat.id, message.chat.first_name, '14521', message.from_user.language_code))
            database.commit()
        else:
            cursor.execute('UPDATE users SET name=? && lang =? WHERE id=?', (message.chat.first_name, message.from_user.language_code, message.chat.id))
            return False
    except:
        pass
def add_user_name(message):
    cursor.execute('UPDATE users SET name=? WHERE id=?', (message.text, message.chat.id, ))
    database.commit()


def add_user_numb(message):

    cursor.execute('UPDATE users SET numb=?, lang=? WHERE id=?', (message.contact.phone_number, message.from_user.language_code, message.chat.id, ))
    database.commit()
# jkjdlkjsadk jaskldjlkj
def add_user_location(message):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="http")
    global location
    location = geolocator.reverse(f"{message.location.latitude}, {message.location.longitude}", language='uz',
                                  namedetails=True)
    location = str(location)
    res = tuple(map(str, location.split(', ')))
    ress = res[::-1]
    adres = str(ress)

    if len(ress) >0: respublika = ress[0]
    else: respublika = ' '
    if len(ress) >2: viloyat = ress[2]
    else: viloyat = ' '
    if len(ress) >3: tuman = ress[3]
    else: tuman = ' '
    if len(ress) >4: hudud = ress[4]
    else: hudud = '-'
    cursor.execute('UPDATE users SET long=?, lat=?, lang=?, location_name=?, respublika=?, viloyat=?, tuman=?, hudud=? WHERE id=?', (message.location.longitude, message.location.latitude, message.from_user.language_code, adres, respublika, viloyat, tuman, hudud, message.chat.id,))
    database.commit()


