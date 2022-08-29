from ctypes import resize
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


buttons_rec = [InlineKeyboardButton('👎', callback_data='dislike'), InlineKeyboardButton('Next', callback_data='recommend'), InlineKeyboardButton(
    '👍', callback_data='like'), InlineKeyboardButton("IMDB", url="https://www.imdb.com/")]
inline_kb1 = InlineKeyboardMarkup(
    row_width=3).add(*buttons_rec)

# button_start = KeyboardButton(text="Start")
# start_kb = ReplyKeyboardMarkup()
# start_kb.add(button_start)
