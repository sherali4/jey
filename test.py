from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN

API_TOKEN = TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



async def update_buttons(message: types.Message, value: int):
    markup = InlineKeyboardMarkup()
    plus_button = InlineKeyboardButton("+", callback_data="plus")
    minus_button = InlineKeyboardButton("-", callback_data="minus")
    markup.add(plus_button, minus_button)

    if message:
        await bot.edit_message_text(f'Value is now {value}', chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup)
    else:
        await bot.send_message(chat_id=message.chat.id, text=f"Value is now {value}", reply_markup=markup)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    inital_value = 0
    await update_buttons(message, inital_value)


@dp.message_handler()
async def echo(message: types.Message):
    inline_kb = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton('Press me', callback_data='button pressed')
    inline_kb.add(inline_btn)
    await bot.send_message(message.chat.id, "Press the button", reply_markup=inline_kb)


@dp.callback_query_handler(lambda call: call.data)
async def callback_inline(call: types.CallbackQuery):
    action = call.data
    current_value = int(call.message.text.split(" ")[3])

    if action == 'plus':
        current_value += 1
    elif action =='minus':
        current_value -=1
    await bot.answer_callback_query(call.id)
    await update_buttons(call.message, current_value)



# @dp.callback_query_handler(lambda c: c.data =='button pressed')
# async def proccess_callback_button(callback_query: types.CallbackQuery):
#     button_data = callback_query.data
#     await bot.send_message(callback_query.from_user.id, f'You passed data: {button_data}')


if __name__ == '__main__':
   from aiogram import executor
   executor.start_polling(dp, skip_updates=True)

