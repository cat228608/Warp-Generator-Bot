import random
import sqlite3
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import api

API_TOKEN = 'Токен'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
conn.commit()

APIS = {
    "Limonix": "Limonix",
    "WG": "WG",
    "STR Bypass": "STR Bypass"
}

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("🎲 Случайный Warp"))
main_kb.add(KeyboardButton("🔧 Выбрать API"))

api_kb = InlineKeyboardMarkup(row_width=2)
api_kb.add(
    InlineKeyboardButton("Limonix", callback_data="api_Limonix"),
    InlineKeyboardButton("WG", callback_data="api_WG"),
    InlineKeyboardButton("STR Bypass", callback_data="api_STR Bypass")
)

wg_kb = InlineKeyboardMarkup(row_width=2)
wg_kb.add(
    InlineKeyboardButton("Получить файл", callback_data="wg_file"),
    InlineKeyboardButton("Получить ссылку", callback_data="wg_url")
)

device_kb = InlineKeyboardMarkup(row_width=2)
device_kb.add(
    InlineKeyboardButton("Телефон", callback_data="device_phone"),
    InlineKeyboardButton("Компьютер", callback_data="device_computer")
)

user_choice = {}

last_message_id = {}

async def safe_delete_message(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await safe_delete_message(message.chat.id, message.message_id)

    sent = await message.answer("Добро пожаловать!\nВыберите действие:", reply_markup=main_kb)
    last_message_id[user_id] = sent.message_id


@dp.message_handler(lambda message: message.text == "🎲 Случайный Warp")
async def handle_random(message: types.Message):
    user_id = message.from_user.id

    await safe_delete_message(message.chat.id, message.message_id)

    api_name = random.choice(list(APIS.keys()))

    if api_name in ["Limonix", "STR Bypass"]:
        device = random.choice(["phone", "computer"])
        await send_config_file(message, user_id, api_name, device)
    elif api_name == "WG":
        sent = await message.answer("Выберите формат получения конфига WG:", reply_markup=wg_kb)
        last_message_id[user_id] = sent.message_id


@dp.message_handler(lambda message: message.text == "🔧 Выбрать API")
async def handle_select_api(message: types.Message):
    user_id = message.from_user.id

    await safe_delete_message(message.chat.id, message.message_id)

    sent = await message.answer("Выберите API:", reply_markup=api_kb)
    last_message_id[user_id] = sent.message_id


@dp.callback_query_handler(lambda c: c.data in ["wg_file", "wg_url"])
async def handle_wg_choice(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id in last_message_id:
        await safe_delete_message(callback_query.message.chat.id, last_message_id[user_id])
        last_message_id.pop(user_id)

    choice = callback_query.data
    if choice == "wg_file":
        filename = 'mafiozi_cgv.conf'
        result = api.requests_wg('file')
        if result == 'good':
            await callback_query.message.answer_document(open(filename, 'rb'))
            os.remove(filename)
        else:
            await callback_query.message.answer("Ошибка при получении конфига WG.")
    else:  # wg_url
        url = api.requests_wg('url')
        if url != 'error':
            await callback_query.message.answer(f"Вот ваша ссылка: \n<code>{url}</code>", parse_mode="HTML")
        else:
            await callback_query.message.answer("Ошибка при получении ссылки WG.")
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("api_"))
async def handle_specific_api(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id in last_message_id:
        await safe_delete_message(callback_query.message.chat.id, last_message_id[user_id])
        last_message_id.pop(user_id)

    api_name = callback_query.data.split("api_")[1]

    if api_name in ["Limonix", "STR Bypass"]:
        user_choice[user_id] = api_name
        sent = await callback_query.message.answer(f"Выберите устройство для {api_name}:", reply_markup=device_kb)
        last_message_id[user_id] = sent.message_id
    elif api_name == "WG":
        sent = await callback_query.message.answer("Выберите формат получения конфига WG:", reply_markup=wg_kb)
        last_message_id[user_id] = sent.message_id

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("device_"))
async def handle_device_choice(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_id in last_message_id:
        await safe_delete_message(callback_query.message.chat.id, last_message_id[user_id])
        last_message_id.pop(user_id)

    device = callback_query.data.split("device_")[1]

    if user_id not in user_choice:
        await callback_query.answer("Ошибка: API не выбран.")
        return

    api_name = user_choice.pop(user_id)

    await send_config_file(callback_query.message, user_id, api_name, device)
    await callback_query.answer()


async def send_config_file(message: types.Message, user_id: int, api_name: str, device: str):
    filename = None
    if api_name == "Limonix":
        filename = api.warp_limonix(device)
    elif api_name == "STR Bypass":
        filename = api.warp_str(device)

    if filename and os.path.exists(filename):
        await message.answer_document(open(filename, 'rb'))
        os.remove(filename)
    else:
        await message.answer(f"Ошибка при получении конфига {api_name}.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
