from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import sqlite3

db = sqlite3.connect('bot.sqlite')
cursor = db.cursor()



products = CallbackData('product', 'id', 'action')

def get_start_kb()-> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('prosmotr vsex produktov', callback_data='get_all_products')],
        [InlineKeyboardButton('dobavit noviy produkt', callback_data='add_new_product')]
    ])
    return ikb

markup_request_client = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Raqamingiz ☎️', request_contact=True),
    KeyboardButton("Lokatsiyangiz 🗺️", request_location=True)
).row(
    KeyboardButton("/video"),
    KeyboardButton("/start")
)




markup_request_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(

    KeyboardButton('Telefon raqam ☎️', request_contact=True),
    KeyboardButton("Lokatsiya 🗺️", request_location=True)

).row(
    KeyboardButton("/video"),
    KeyboardButton('/katalog')
).row(
    KeyboardButton('/delete'),
    KeyboardButton('/tovar')
).row(
    KeyboardButton('/start'),
    KeyboardButton('/admin')
)


markup_request_superadmin = ReplyKeyboardMarkup(resize_keyboard=True).row(

    KeyboardButton('/+admin'),
    KeyboardButton("/-admin")
).add(
    KeyboardButton('/+tovar_turi'),
    KeyboardButton('/-tovar_turi')

).add(
    KeyboardButton('/turini_tanlash'),
    KeyboardButton('/narxini_uzgartirish')

).add(
    KeyboardButton('/qaytish')
)

state_finish = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/otmena'))

# ).row(
#     KeyboardButton("/video"),
#     KeyboardButton('/katalog')
# ).row(
#     KeyboardButton('/delete'),
#     KeyboardButton('/tovar')
# ).row(
#     KeyboardButton('/start'),
#     KeyboardButton('/admin')
# )

# markup_request_admin1 = ReplyKeyboardMarkup(resize_keyboard=True).add(
#     KeyboardButton('Telefon raqamingizni kiriting ☎️', request_contact=True)
# ).add(
#     KeyboardButton("Lokatsiya jo'nating 🗺️", request_location=True)
# ).add(
#     KeyboardButton("/video")
# ).add(
#     KeyboardButton('/katalog')
# ).add(
#     KeyboardButton('/delete')
# ).add(
#     KeyboardButton('/tovar')
# )
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Telefon raqamingizni kiriting ☎️', request_contact=True)
).add(
    KeyboardButton("Lokatsiya jo'nating 🗺️", request_location=True)
).add(
    KeyboardButton("/video")
).add(
    KeyboardButton('/katalog')
).add(
    KeyboardButton('/delete')
).add(
    KeyboardButton('/tovar')
)
