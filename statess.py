import datetime
import sqlite3

from aiogram import types, executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from geopy import distance

from adminlar import is_superadmin
from baza import add_user, add_user_name, add_user_numb, db_connect, add_user_location, add_item, add_zakaz, \
    zakaz_otmen, zakaz_oladi, add_admin, add_tovar_turi_bazaga
from config import TOKEN, gruppa, gruppa_sale, sherali, xa_yuq
from excel import add_excel, add_zakaz_excel, add_users_excel
from keyboard import markup_request_admin, markup_request_client, markup_request, markup_request_superadmin, \
    state_finish
from surov import tovar_reg, del_tovar, plus_admin, del_admin, del_tovar_turi_admin, add_tovar_turi_admin, user_reg

storage = MemoryStorage

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
database = sqlite3.connect('bot_lite.sqlite')
cursor = database.cursor()

async def on_startup1(_):
    await db_connect()



@dp.message_handler(state=del_tovar.id)
async def del_item_by_id(message: types.Message, state: FSMContext):
    try:
        cursor.execute('UPDATE tovar SET status = 2, user_id= ? WHERE id= ?', (int(message.from_user.id), int(message.text),))
        database.commit()
    except:
        pass
    await state.finish()
    await message.answer(f"ID = { message.text} - raqamli tovar ro'yxatdan olib tashlandi!", reply_markup=markup_request_admin)


@dp.message_handler(commands=['-tovar_turi'])
async def add_tovar_turi(message: types.Message):
    if is_superadmin(message.from_user.id):
        await del_tovar_turi_admin.nomi.set()
        try:
            cursor.execute('SELECT * FROM tovar_turi')
            tovar_turi = cursor.fetchall()
            keyboard_inline = InlineKeyboardMarkup(row_width=3)
            for t in tovar_turi:
                keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
        except:
            pass
        await message.answer('?', reply_markup=state_finish)
        try:
            await message.answer("Tovar turi nomini tanlang", reply_markup=keyboard_inline)
        except:
            await message.answer("Tovar turi nomini tanlang", reply_markup=markup_request_admin)
    else:
        await message.answer('?', reply_markup=state_finish)

@dp.callback_query_handler(state=del_tovar_turi_admin.nomi)
async def add_tovar_turi_del(call: types.CallbackQuery,  state: FSMContext):
    async with state.proxy() as data:
        data['tovar_turi1'] = call.message.text
        tovar_turi = call['data']
    await state.finish()
    cursor.execute("DELETE FROM tovar_turi WHERE tovar_turi=?", (tovar_turi,))
    database.commit()
    await bot.send_message(call.from_user.id, f'{tovar_turi} - nomli tovar turi tizimdan o\'chirildi', reply_markup=markup_request_superadmin)
    await call.message.delete()


@dp.message_handler(commands=['+tovar_turi'])
async def add_tovar_turi(message: types.Message):
    if is_superadmin(message.from_user.id):
        await add_tovar_turi_admin.nomi.set()
        await message.answer("Tovar turi nomini probellarsiz lotin alifbosida yozing", reply_markup=state_finish)
    else:
        await message.answer('?', reply_markup=state_finish)
        await add_tovar_turi_admin.next()

@dp.message_handler(state=add_tovar_turi_admin.nomi)
async def add_menyu_admin(message: types.Message, state: FSMContext):
    if is_superadmin(message.from_user.id):
        async with state.proxy() as data:
            data['nomi'] = message.text
        # await message.reply(str(data))
        await add_tovar_turi_admin.next()
        await message.answer("Tovar turini izohini yozing", reply_markup=state_finish )
    else:
        await message.answer('?', reply_markup=state_finish)


@dp.message_handler(state=add_tovar_turi_admin.izohi)
async def add_menyu_admin(message: types.Message, state: FSMContext):
    if is_superadmin(message.from_user.id):
        async with state.proxy() as data:
            data['izohi'] = message.text
        await message.reply(str(data))
        await message.answer("Ushbu tovar turi tizimga kiritildi", reply_markup=markup_request_superadmin )
        print(state)
        try:
            await add_tovar_turi_bazaga(state)
        except:
            await message.answer('Ushbu tovar turi avval kiritilgan', reply_markup=markup_request_superadmin)
        await state.finish()
    else:
        await message.answer('?', reply_markup=state_finish)




@dp.message_handler(commands=['otmena'], state='*')
async def finish_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Adminni kiritish bekor qilindi.", reply_markup=markup_request_admin)



@dp.message_handler(commands=['-admin'])
async def del_items(message: types.Message):
    if is_superadmin(message.from_user.id):
        await del_admin.id_user.set()
        await message.reply("Administratorning id raqamini kiriting:", reply_markup=markup_request_superadmin)
    else:
        await message.answer('eeeeeeeeee', reply_markup=markup_request_client)


@dp.message_handler(state=del_admin.id_user)
async def del_admin_by_id(message: types.Message, state: FSMContext):
    try:
        cursor.execute('DELETE FROM admin WHERE id_user=?', (int(message.text),))
        database.commit()
    except:
        pass
    await state.finish()
    await message.answer(f"ID = { message.text} - raqamli admin ro'yxatdan olib tashlandi!", reply_markup=markup_request_superadmin)





@dp.message_handler(commands=['+admin'])
async def del_items(message: types.Message):
    if is_superadmin(message.from_user.id):
        await plus_admin.user_id.set()
        await message.answer("Adminning ID raqamini kiriting.", reply_markup=state_finish)
    else:
        await message.answer('?', reply_markup=state_finish)




@dp.message_handler(state=plus_admin.user_id)
async def add_ifo_admin(message: types.Message, state: FSMContext):
    if is_superadmin(message.from_user.id):
        async with state.proxy() as data:
            data['user_id'] = message.text
        await message.answer("Adminning nomini kiriting" )
        await plus_admin.next()
    else:
        await message.answer('?', reply_markup=state_finish)


@dp.message_handler(state=plus_admin.ifo)
async def add_ifo_admin(message: types.Message, state: FSMContext):
    if is_superadmin(message.from_user.id):
        async with state.proxy() as data:
            data['ifo'] = message.text
        try:

            cursor.execute('SELECT * FROM tovar_turi')
            tovar_turi = cursor.fetchall()
            keyboard_inline = InlineKeyboardMarkup()
            for t in tovar_turi:
                keyboard_inline.add(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))

        except:
            pass
        await message.answer("Adminga tegishli tovar turini tanlang", reply_markup=keyboard_inline )
        await plus_admin.next()
    else:
        await message.answer('?', reply_markup=state_finish)

@dp.callback_query_handler(state=plus_admin.tovar_turi)
async def add_tovar_turi(call: types.CallbackQuery,  state: FSMContext):
    tovar_turi = call['data']
    async with state.proxy() as data:
        data['tovar_turi'] = tovar_turi
    await bot.send_message(call.from_user.id, 'Admin ruxsat etiladigan menyu turlarini vergul bilan ajratib yozing')
    await plus_admin.next()

@dp.message_handler(state=plus_admin.menyu)
async def add_menyu_admin(message: types.Message, state: FSMContext):
    if is_superadmin(message.from_user.id):
        async with state.proxy() as data:
            data['menyu'] = message.text
        await message.reply(str(data))
        await message.answer("Admin tizimga qo'shildi." )
        print(state)
        await add_admin(state)
        await state.finish()
    else:
        await message.answer('?', reply_markup=state_finish)


@dp.message_handler(commands=['qaytish'])
async def del_items(message: types.Message):
    if is_superadmin(message.from_user.id):
        await message.answer('?', reply_markup=markup_request_admin)
    else:
        await message.answer('?', reply_markup=markup_request_client)

@dp.message_handler(commands=['admin'], state=None)
async def del_items(message: types.Message):
    if is_superadmin(message.from_user.id):
        await message.answer('Siz Administratortiz. Sizga Barcha imkoniyatlardan foydalanishga ruxsatingiz bor.', reply_markup=markup_request_superadmin)
    else:
        await message.answer('Siz Admin emassiz.')

@dp.message_handler(commands=['tovar'])
async def del_itemss(message: types.Message):
    if is_superadmin(message.from_id, menyu='tovar'):
    # if message.from_id == 6456875695 or message.from_id == 6158978005 or message.from_id == 496958227 or message.from_id == 5954851285 or message.from_id== 5163491786 or message.from_id== 6292591760 or message.from_id== 6652659593 or message.from_id== 6591515474 or message.from_id== 2060764847:
        # await bot.send_document(message.from_user.id, ('tovar.xlsx', 'file'))
        add_excel()
        add_users_excel()
        add_zakaz_excel()
        await bot.send_document(message.from_user.id, open('tovar.xlsx', 'rb'), caption=f'{datetime.datetime.now()}')
        await bot.send_document(message.from_user.id, open('users.xlsx', 'rb'), caption=f'{datetime.datetime.now()}')
        await bot.send_document(message.from_user.id, open('zakaz.xlsx', 'rb'), caption=f'{datetime.datetime.now()}', reply_markup=markup_request_admin)
    else:
         await message.reply('Sizda ushbu yo\'nalish bo\'yicha ruxsat yo\'q.')


@dp.message_handler(commands=['delete'], state=None)
async def del_items(message: types.Message):
    if is_superadmin(message.from_id, menyu='delete'):
        await del_tovar.id.set()
        await message.reply('Tovarning id raqamini kiriting:', reply_markup=state_finish)
    else:
         await message.reply('Siz Admin emassiz')

@dp.message_handler(state=del_tovar.id)
async def del_item_by_id(message: types.Message, state: FSMContext):
    try:
        cursor.execute('UPDATE tovar SET status = 2, user_id= ? WHERE id= ?', (int(message.from_user.id), int(message.text),))
        database.commit()
    except:
        pass
    await state.finish()
    await message.answer(f"ID = { message.text} - raqamli tovar ro'yxatdan olib tashlandi!", reply_markup=markup_request_admin)

@dp.message_handler(commands=['katalog'], state=None)
async def add_items(message: types.Message):
    if is_superadmin(message.from_id, menyu='katalog'):
        await tovar_reg.turi.set()
        try:
            cursor.execute('SELECT * FROM tovar_turi')
            tovar_turi = cursor.fetchall()
            keyboard_inline = InlineKeyboardMarkup(row_width=3)
            for t in tovar_turi:
                keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
        except:
            pass
        await message.reply(text='Tovar turini tanlang:', reply_markup=keyboard_inline)
        await message.answer('?', reply_markup=state_finish)
    else:
         await message.reply("Sizda ushbu yo'nalish bo'yicha ruxsat yo'q.")

@dp.callback_query_handler(state=tovar_reg.turi)
async def add_item_turi(call: types.CallbackQuery,  state: FSMContext):
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    print(call.data)
    async with state.proxy() as data:
        data['turi'] = call.data
    await bot.send_message(call.from_user.id, 'Tovarning nomini kiriting', reply_markup=state_finish)
    await tovar_reg.next()

@dp.message_handler(state=tovar_reg.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(f"Tovarning o'lchov birligini kiriting", reply_markup=state_finish)
    await tovar_reg.next()

@dp.message_handler(state=tovar_reg.ulchov)
async def add_item_ulchov(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ulchov'] = message.text
    await message.answer(f"Tovarning narxini kiriting", reply_markup=state_finish)
    await tovar_reg.next()

@dp.message_handler(state=tovar_reg.narx)
async def add_item_narx(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['narx'] = message.text
    await message.answer(f"Tovarning tarifini kiriting", reply_markup=state_finish)
    await tovar_reg.next()

@dp.message_handler(content_types=['sticker'])
async def check_sticker(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAANQZNdBBu9v-gLYA5PULJvsbu9ZJR0AAi8AAy1xhhUAAVh83pZaoZcwBA')
    await message.answer("Stiker yubormang. foydasi yo\'q")

@dp.message_handler(state=tovar_reg.tarifi)
async def add_item_tarifi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tarifi'] = message.text
    await message.answer(f"Tovarning rasmini kiriting", reply_markup=state_finish)
    await tovar_reg.next()

@dp.message_handler(lambda message: not message.photo, state=tovar_reg.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Bu rasm emas')

# yangi tovar qo'shish
@dp.message_handler(content_types=['photo'], state=tovar_reg.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            data['user'] = message.from_user.id
    await add_item(state)
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.answer('Mahsulot kiritildi', reply_markup=markup_request_admin)
    button2 = InlineKeyboardButton(text="Yangi tovarlarni ko'rish", callback_data="yangi-tovar")
    keyboard_inline = InlineKeyboardMarkup().add(button2)
    await state.finish()
    await bot.send_message(xa_yuq, "Yangi mahsulot qo'shildi", reply_markup=keyboard_inline)

@dp.message_handler(content_types=['photo'])
async def start_message(message: types.Message):
    print(message)

@dp.message_handler(content_types=['contact'])
async def start_message(message: types.Message):
    add_user_numb(message)


# noinspection PyTypeChecker
@dp.message_handler(content_types=['location'])
async def start_message(message: types.Message):
    long = message.location.longitude
    lat = message.location.latitude
    add_user_location(message)
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="http")
    global location
    location = geolocator.reverse(f"{message.location.latitude}, {message.location.longitude}", language=f'{message.from_user.language_code}',
                                 namedetails=True)
    location = str(location)
    res = tuple(map(str, location.split(', ')))
    ress = res[::-1]
    ress = str(ress)
    await bot.send_location(sherali, lat, long)
    await bot.send_message(sherali, ress)
    # noinspection PyTypeChecker
    await bot.send_message(sherali, message)




@dp.message_handler(content_types=["video"])
async def start_message(message: types.Message):
    file_id = message.video.file_id  # Get file id
    await bot.send_message(sherali, file_id)
    print(file_id)

@dp.message_handler(content_types=["document"])
async def start_message(message: types.Message):
    file_id = message.document.file_id  # Get file id
    await bot.send_message(sherali , file_id)
    print(file_id)

@dp.message_handler(state=user_reg.name)
async def add_name(message: types.Message):
    chat_id = message.chat.id
    add_user_name(message)
    await bot.send_message(chat_id, 'SEND Your number')
    await message.reply("Шестое - запрашиваем контакт и геолокацию\nЭти две кнопки не зависят друг от друга",
                        reply_markup=markup_request)

@dp.message_handler(state=user_reg.numb)
async def add_numb(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    user_status = add_user_numb(message)
    if user_status == False:
        pass
    else:
        await bot.send_message(chat_id, "Registration Successfully")
        await state.finish()


@dp.message_handler(commands=['video'])
async def video_start(message: types.Message):
    await bot.send_video(message.from_user.id, video="BAACAgIAAxkBAAIBtmUq9e6TAy0ptHLX8nV3sdVvSIsVAAJ1NgACha2oS2yJ82ozxs5gMAQ")


@dp.message_handler(commands=['start'])
async def cmd_startt(message: types.Message):

    chat_id = message.chat.id
    add_user(message)
    await bot.send_message(chat_id, f'Assalomu Aleykum {message.chat.first_name}')
    if is_superadmin(message.from_id):
        # print('Siz_admin')
        await message.answer("Botning barcha imkoniyatlaridan foydalanish uchun telefon raqamingizni kiriting va lokatsiya jo'nating tugmasini bosing", reply_markup=markup_request_admin)
    else:
        await message.answer("Botning barcha imkoniyatlaridan foydalanish uchun telefon raqamingizni kiriting va lokatsiya jo'nating tugmasini bosing", reply_markup=markup_request_client)
        print('Siz admin emassiz')
    try:
        cursor.execute('SELECT * FROM tovar_turi')
        tovar_turi = cursor.fetchall()
        keyboard_inline = InlineKeyboardMarkup(row_width=3).insert(InlineKeyboardButton(text='Barcha tovarlar', callback_data='barcha'))
        for t in tovar_turi:
            keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
    except:
        pass
    finally:
        keyboard_inline.row(InlineKeyboardButton(text='Printerlar va elektron qurilmalar', callback_data='Printerlar'))
        # keyboard_inline.insert(InlineKeyboardButton(text='Kompyuter va elektron qurilmalar', callback_data='El-qurilmalar'))


    await message.answer('?', reply_markup=keyboard_inline)




@dp.callback_query_handler(text=["Printerlar"])
async def check_button_qurilma(call: types.CallbackQuery):
    kitob = {
        'printer': 'BQACAgIAAxkBAAIWy2U95S5hCOyL8iy0tyuatibt8xFwAAL0MAACFSfwSRQ0QVTU4YwLMAQ',
        'printer1': 'BQACAgIAAxkBAAIWzGU95S5QPWAxhdVqacOjRTRRM2IWAAL1MAACFSfwSbjwSjndGN3_MAQ',
        'qurilma': 'BQACAgIAAxkBAAIWzWU95S6K9qGfC2szwwABKCDvx25m_gAC9jAAAhUn8EmNS-9RRsD8SDAE',

    }
    for k in kitob:
        # print(f"key={k} va value={kitob[k]}")
        await call.message.answer_document(document=kitob[k], caption=datetime.datetime.now())

    # await bot.send_document(call.message.from_user.id, open('printer.xlsx', 'rb'), caption='datetime.datetime.now()')
    # await bot.send_document(call.message.from_user.id, open('excel/tovar.xlsx', 'rb'), caption=datetime.datetime.now())
    # await bot.send_document(call.message.from_user.id, open('excel/tovar.xlsx', 'rb'), caption=datetime.datetime.now())







# sotib olishni bosganda
@dp.callback_query_handler(text=["In_First_button", "In_Second_button"])
async def check_button(call: types.CallbackQuery):
    id_client = call.values['from']['id']
    sher = call.values['message']['reply_markup']['inline_keyboard']
    for sh in sher:
        global nomer
        nomer = sh[0]['text']
    nomer = nomer
    mess = call.values['message']['message_id']
    await add_zakaz(id_client, int(nomer))
    await bot.send_message(id_client, 'Buyurtmangiz qabul qilindi. tez orada operatorlar telefon qilishadi.', reply_to_message_id=mess)

    # adminga boradi
    cursor.execute("SELECT * FROM users WHERE id=?", (id_client,))
    klient = cursor.fetchone()
    cursor.execute("SELECT * FROM tovar WHERE id=?", (int(nomer),))
    tovar = cursor.fetchone()
    cursor.execute("SELECT * FROM users WHERE id=?", (tovar[8],))
    sotuvchi = cursor.fetchone()


    # print('Tovarni kiritgan odam', tovar[8])
    button1 = InlineKeyboardButton(text=f"{tovar[0]}", callback_data="In_First_admin")
    button12 = InlineKeyboardButton(text=f"{id_client}", callback_data="In_eleven_admin")
    button13 = InlineKeyboardButton(text=f"{tovar[8]}", callback_data="In_tvelve_admin")
    button2 = InlineKeyboardButton(text="sotib olmaydi", callback_data="In_Second_admin")
    button3 = InlineKeyboardButton(text="sotib oladi", callback_data="In_Third_admin")
    keyboard_inline = InlineKeyboardMarkup().add(button1, button12, button13, button2, button3)
    await bot.send_location(gruppa, klient[4], klient[5])
    masofa = distance.distance((sotuvchi[5], sotuvchi[4]),(klient[5], klient[4])).km
    masofa_km = '{:.1f}-km'.format(masofa)
    await bot.send_photo(chat_id=gruppa, photo=tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- "
                                                                 f"{tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]} \nxaridor nomeri"
                                                                 f" - +{klient[2]} \nXaridor Ismi - {klient[1]}"
                                                                 f"\n <b>Respublika</b> - {klient[7]}"
                                                                 f"\n <b>Viloyat</b> - {klient[8]}"
                                                                 f"\n <b>Shahar(tuman)</b> - {klient[9]}"
                                                                 f"\n <b>hudud</b> - {klient[10]}"
                                                                 f"\n <b>To'liq</b> - {klient[6]}"
                                                                 f"\n <b>Masofa</b> - {masofa_km}", parse_mode='HTML', reply_markup=keyboard_inline)


# oladini bosganda
@dp.callback_query_handler(text=["In_First_admin", "In_Second_admin"])
async def check_button(call: types.CallbackQuery):
    id_tovar = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    id_client = call.values['message']['reply_markup']['inline_keyboard'][0][1]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    user_id = call.from_user.id
    zakaz_otmen(id_client, id_tovar, user_id=user_id)
    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    next_message = message_id+1
    try:
        await bot.delete_message(message_id=next_message, chat_id=chat_id)
    except:
        pass


# sotib sotib oladini bosganda
@dp.callback_query_handler(text=["In_First_admin", "In_Third_admin"])
async def check_button(call: types.CallbackQuery):
    id_tovar = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    id_client = call.values['message']['reply_markup']['inline_keyboard'][0][1]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    saler_id = call.values['message']['reply_markup']['inline_keyboard'][0][2]['text']
    user_id = call.from_user.id
    zakaz_oladi(id_client, id_tovar, user_id=user_id)
    next_message = message_id+1
    await bot.forward_message(chat_id=gruppa_sale, from_chat_id=gruppa, message_id=message_id)
    await bot.forward_message(chat_id=saler_id, from_chat_id=gruppa, message_id=message_id)
    try:
        await bot.forward_message(chat_id=gruppa_sale, from_chat_id=gruppa, message_id=next_message)
        await bot.forward_message(chat_id=saler_id, from_chat_id=gruppa, message_id=next_message)
    except:
        pass

    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    try:
        await bot.delete_message(message_id=next_message, chat_id=chat_id)
    except:
        pass
    await call.answer('Sotuv bo\'limiga yuborildi')


@dp.callback_query_handler(text=["yangi-tovar", ])
async def check_button():
    cursor.execute("SELECT * FROM tovar WHERE status=0")
    yangi_tovar = cursor.fetchall()
    # for t in yangi_tovar:
    #     await bot.send_message(xa_yuq, f'{t[0]} - raqamli Yangi tovarni kurildi')
    #     await bot.send_photo(chat_id=xa_yuq, photo=t[5])

    for tovar in yangi_tovar:
        # await bot.send_message(xa_yuq, f'{tovar[0]} - raqamli 11111Yangi tovarni kurildi')
        # # print(f"{tovar[0]}")
        button = InlineKeyboardButton(text=f"{tovar[0]}", callback_data="tovar")
        button1 = InlineKeyboardButton(text="O'chirish", callback_data="uchirish")
        button2 = InlineKeyboardButton(text="Qo'shish", callback_data="qushish")
        keyboard_inline = InlineKeyboardMarkup().add(button, button1, button2)
        # # await bot.send_photo(chat_id=xa_yuq, photo=tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]}", parse_mode='HTML', reply_markup=keyboard_inline)
        await bot.send_photo(chat_id=xa_yuq, photo=tovar[5],
                             caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]}",
                             parse_mode='HTML', reply_markup=keyboard_inline)
# @dp.callback_query_handler(text=["yangi-tovar",])
# async def check_button(call: types.CallbackQuery):
#     cursor.execute("SELECT * FROM 'tovar' WHERE status =?", (0,))
#     yangi_tovar = cursor.fetchall()++
#     for tovar in yangi_tovar:
#         # print(f"{tovar[0]}")
#         button = InlineKeyboardButton(text=f"{tovar[0]}", callback_data="tovar")
#         button1 = InlineKeyboardButton(text="O'chirish", callback_data="uchirish")
#         button2 = InlineKeyboardButton(text="Qo'shish", callback_data="qushish")
#         keyboard_inline = InlineKeyboardMarkup().add(button, button1, button2)
#         await bot.send_photo(chat_id=xa_yuq, photo=tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]}", parse_mode='HTML', reply_markup=keyboard_inline)


@dp.callback_query_handler(text=["uchirish",])
async def check_button(call: types.CallbackQuery):
    kod = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    cursor.execute('UPDATE tovar SET status=2 WHERE id=?', (kod, ))
    database.commit()
    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    # print(message_id)
# yangi yaratilgan tovarni aktivlashtirish
@dp.callback_query_handler(text=["qushish"])
async def check_button(call: types.CallbackQuery):

    kod = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    cursor.execute('UPDATE tovar SET status=1 WHERE id=?', (kod, ))
    database.commit()
    # print(chat_id)
    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    cursor.execute("SELECT * FROM tovar WHERE id=?", (kod,))
    tovar = cursor.fetchone()
    cursor.execute("SELECT * FROM users WHERE id=?", (int(tovar[8]),))
    sotuvchi = cursor.fetchone()
    button1 = InlineKeyboardButton(text=f"{tovar[0]}", callback_data="In_First_button")
    button2 = InlineKeyboardButton(text="Sotib olish", callback_data="In_Second_button")
    keyboard_inline = InlineKeyboardMarkup().add(button1, button2)
    if tovar[10] == 'burger':
        await bot.send_photo(chat_id='@jeypaygroup', message_thread_id='7', photo=tovar[5],
                             caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]}"
                                     f"\n<b>o'lchov birligi</b>- {tovar[2]}"
                                     f"\n<b>💵 narxi</b>- {tovar[3]}"
                                     f"\n<b>tarifi</b>- {tovar[4]}"
                                     f"\n<b>Sotuvchi nomeri</b>- +{sotuvchi[2]}"
                                     f"\n<b>Viloyat</b>- {sotuvchi[8]}"
                                     f"\n<b>Shahar(tuman)</b>- {sotuvchi[9]}"
                                     f"\n<b>Hudud</b>- {sotuvchi[10]}", parse_mode='HTML', reply_markup=keyboard_inline)


# tovar turini tanlaganda
@dp.callback_query_handler(state=None)
async def check_button_hh(call: types.CallbackQuery):
    tanlangan_tovar_turi=call.data
    await call.message.answer(f'SIZ {call.data} ni tanladingiz')
    await call.message.delete()
    try:
        cursor.execute('SELECT * FROM tovar_turi')
        tovar_turi = cursor.fetchall()

        keyboard_inline = InlineKeyboardMarkup(row_width=3).insert(InlineKeyboardButton(text='Barcha tovarlar', callback_data='barcha'))
        for t in tovar_turi:
            keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
    except:
        pass



    cursor.execute("SELECT * FROM tovar WHERE status = '1' AND turi=? ORDER BY id", (f'{tanlangan_tovar_turi}',))
    tovar = cursor.fetchall()
    # print(f'tovar - {tovar}')
    # print(call.message.chat.id)
    cursor.execute("SELECT * FROM users WHERE id=?", (call.message.chat.id,))
    xaridor = cursor.fetchone()
    for x in tovar:
        cursor.execute("SELECT * FROM users WHERE id=?", (int(x[8]),))
        sotuvchi = cursor.fetchone()
        masofa = distance.distance((xaridor[5], xaridor[4]), (sotuvchi[5], sotuvchi[4])).km
        masofa_km = '{:.1f}-km'.format(masofa)
        sotuvchi_nomeri = sotuvchi[2]
        button1 = InlineKeyboardButton(text=f"{x[0]}", callback_data="In_First_button")
        button2 = InlineKeyboardButton(text="Sotib olish", callback_data="In_Second_button")
        keyboard_inline = InlineKeyboardMarkup().add(button1, button2)
        if sotuvchi[8]==xaridor[8] and not sotuvchi[9]==xaridor[9]:
            await call.message.answer_photo(x[5], caption=f"<b>ID</b> - {x[0]} \n<b>nomi</b>- {x[1]} "
                                                     f"\n<b>o'lchov birligi</b>- {x[2]} "
                                                     f"\n<b>💵 narxi</b>- {x[3]} "
                                                     f"\n<b>tarifi</b>- {x[4]} "
                                                     f"\n<b>Sotuvchi nomeri</b>- +{sotuvchi_nomeri}"
                                                     f"\n<b>Tovar sizning viloyatingizda joylashgan</b>"
                                                     f"\n<b>Shahar(tuman)</b>- {sotuvchi[9]}"
                                                     f"\n<b>Hudud</b>- {sotuvchi[10]}"
                                                     f"\n<b>Masofa</b>- {masofa_km}", parse_mode='HTML', reply_markup=keyboard_inline)
            try:
                cursor.execute('SELECT * FROM tovar_turi')
                tovar_turi = cursor.fetchall()

                # soni = len(tovar_turi)
                keyboard_inline = InlineKeyboardMarkup(row_width=3).insert(
                    InlineKeyboardButton(text='Barcha tovarlar', callback_data='barcha'))
                for t in tovar_turi:
                    keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
            except:
                pass
        elif sotuvchi[8]==xaridor[8] and sotuvchi[9]==xaridor[9]:
            await call.message.answer_photo(x[5], caption=f"<b>ID</b> - {x[0]} \n<b>nomi</b>- {x[1]} "
                                                     f"\n<b>o'lchov birligi</b>- {x[2]} "
                                                     f"\n<b>💵 narxi</b>- {x[3]} "
                                                     f"\n<b>tarifi</b>- {x[4]} "
                                                     f"\n<b>Sotuvchi nomeri</b>- +{sotuvchi_nomeri}"
                                                     f"\n<b>Tovar sizning shahringiz(tumaningiz)da joylashgan</b>"
                                                     f"\n<b>Hudud</b>- {sotuvchi[10]}"
                                                     f"\n<b>Masofa</b>- {masofa_km}", parse_mode='HTML', reply_markup=keyboard_inline)
            try:
                cursor.execute('SELECT * FROM tovar_turi')
                tovar_turi = cursor.fetchall()
                keyboard_inline = InlineKeyboardMarkup(row_width=3).insert(
                    InlineKeyboardButton(text='Barcha tovarlar', callback_data='barcha'))
                for t in tovar_turi:
                    keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
            except:
                pass
        else:
            await call.message.answer_photo(x[5], caption=f"<b>ID</b> - {x[0]} \n<b>nomi</b>- {x[1]} "
                                                     f"\n<b>o'lchov birligi</b>- {x[2]} "
                                                     f"\n<b>💵 narxi</b>- {x[3]} "
                                                     f"\n<b>tarifi</b>- {x[4]} "
                                                     f"\n<b>Sotuvchi nomeri</b>- +{sotuvchi_nomeri}"
                                                     f"\n<b>Viloyat</b>- {sotuvchi[8]}"
                                                     f"\n<b>Shahar(tuman)</b>- {sotuvchi[9]}"
                                                     f"\n<b>Hudud</b>- {sotuvchi[10]}"
                                                     f"\n<b>Masofa</b>- {masofa_km}", parse_mode='HTML', reply_markup=keyboard_inline)

            try:
                cursor.execute('SELECT * FROM tovar_turi')
                tovar_turi = cursor.fetchall()

                keyboard_inline = InlineKeyboardMarkup(row_width=3).insert(
                    InlineKeyboardButton(text='Barcha tovarlar', callback_data='barcha'))
                for t in tovar_turi:
                    keyboard_inline.insert(InlineKeyboardButton(text=f"{t[2]}", callback_data=f"{t[1]}"))
            except:
                pass

    await call.message.answer('?', reply_markup=keyboard_inline)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup1,)
