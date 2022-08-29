from email.message import Message
import logging
import sqlite3
import requests
from aiogram import Bot, Dispatcher, executor, types
import keyboard as kb
from recommendation import reccomend_movie, start_movies
from helping_func import soup, getdata, insert
import time
import datetime


conn = sqlite3.connect("shows.db")
cursor = conn.cursor()


# API токен
API_TOKEN = "5540328842:AAEUm8EnrvQ6CIa4HwPxjC9HyKVad4KSc88"

# Логи
logging.basicConfig(level=logging.INFO)

# Иницилизурем бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def getdata(url):
    r = requests.get(url)
    return r.text


@dp.callback_query_handler(lambda c: c.data == "recommend")
async def process_callback_recommend(callback_query: types.CallbackQuery):
    random_show = start_movies()
    img_url = soup(random_show)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_photo(callback_query.from_user.id, photo=img_url, caption=f"{random_show}", reply_markup=kb.inline_kb1)


@dp.callback_query_handler(lambda c: c.data == "like")
async def process_like_text(call: types.CallbackQuery):
    random_show = call.message.caption

    cursor.execute("INSERT INTO movies (title,timestamp,date) VALUES(?,?,?);",
                   (random_show, int(time.time()), str(datetime.date.today().strftime("%d-%m-%Y"))))

    recommended = reccomend_movie(random_show, cursor)
    img_url = soup(recommended)

    cursor.connection.commit()
    await bot.answer_callback_query(call.id, text="You like this movie")
    await bot.send_photo(call.from_user.id, photo=img_url, caption=f"{recommended}", reply_markup=kb.inline_kb1)


@dp.callback_query_handler(lambda c: c.data == "dislike")
async def process_dislike_text(call: types.CallbackQuery):
    random_show = str(cursor.execute(
        "SELECT title FROM movies ORDER BY RANDOM() LIMIT 1;").fetchall()[0][0])
    img_url = soup(random_show)

    await bot.answer_callback_query(call.id, cache_time=50)
    await bot.send_photo(call.from_user.id, photo=img_url, caption=f"{random_show}", reply_markup=kb.inline_kb1)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hi, I am FilmsToWatch bot\nI'll help you to find an interesting movie to watch\nPress /help to work with bot.")


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply("Press /recommend and I'll help you to find an interesting movie to watch.")


@dp.message_handler(commands=["recommend"])
async def process_reccomend_command(message: types.Message):
    random_show = start_movies()
    img_url = soup(str(random_show))
    await bot.send_photo(message.from_user.id, photo=img_url, caption=f"{random_show}", reply_to_message_id=message.message_id, reply_markup=kb.inline_kb1)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
