from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import db_name
from utils.Database import Database
db = Database(db_name)

def make_category_kb():
    categories = db.get_categories()
    rows = [
        [InlineKeyboardButton(text=cat[1],callback_data=cat[1])]
        for cat in categories
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=rows
    )
    return inl_kb

def make_confirm_kb():
    rows = [
        InlineKeyboardButton(text='YES', callback_data='YES'),
        InlineKeyboardButton(text='NO', callback_data='NO')
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=[rows]
    )
    return inl_kb

def make_product_kb():
    products = db.get_products()
    rows = [
        [InlineKeyboardButton(text=p[1],callback_data=str(p[0]))]
        for p in products
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=rows
    )
    return inl_kb


def make_category2_kb():
    categories = db.get_categories()
    rows = [
        [InlineKeyboardButton(text=cat[1],callback_data=str(cat[0]))]
        for cat in categories
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=rows
    )
    return inl_kb


def make_product3_kb():
    products = db.get_products()
    rows = [
        [InlineKeyboardButton(text=p[1],callback_data=str(p[0]))]
        for p in products
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=rows
    )
    return inl_kb