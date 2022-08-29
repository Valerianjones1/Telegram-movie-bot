import requests
from PIL import Image
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def getdata(url):
    r = requests.get(url)
    return r.text


# def imdb_button(movie, cursor):
#     movie = str(movie)
#     for_imdb_show = movie[:len(movie)-7]
#     print(for_imdb_show)
#     id_for_imdb = cursor.execute(
#         "SELECT id FROM movies WHERE title LIKE ?", (for_imdb_show)).fetchall()[0][0]

#     button = InlineKeyboardMarkup.add(InlineKeyboardButton(
#         'Imdb', url=f"https://www.imdb.com/title/tt{id_for_imdb}/", callback_data="imdb"))
#     return button


def soup(movie_name):
    html_data = getdata(
        f"https://www.google.com/search?tbm=isch&q={movie_name}")
    soup = BeautifulSoup(html_data, 'html.parser')
    try:
        show_img_url = soup.find_all("img")[1]["src"]
    except IndexError:
        show_img_url = 0

    if show_img_url:
        img_url = soup.find_all("img")[1]["src"]
    else:
        img_url = "https://i.ytimg.com/vi/6kCSVT3r_Qg/hqdefault.jpg"

    return img_url


def insert(title, cursor):
    cursor.execute("INSERT INTO movies (title,timestamp,date) VALUES(?,?,?);",
                   (title, int(time.time()), str(datetime.date.today().strftime("%d-%m-%Y"))))
