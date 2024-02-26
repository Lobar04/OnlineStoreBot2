from aiogram.types import BotCommand
from aiogram.filters import Command, CommandStart


admin_commands = [
    BotCommand(command='start', description='Start / restart bot'),
    BotCommand(command='categories', description='get categories'),
    BotCommand(command='add_categories', description='add new category'),
    BotCommand(command='update_category', description='update category name'),
    BotCommand(command='del_category', description='delete categories'),
    BotCommand(command='add_product', description='add new category'),
    BotCommand(command='del_product', description='delete product'),
    BotCommand(command='edit_product', description='edit product name'),
    BotCommand(command='products', description='get products')
]

user_commands = [
    BotCommand(command='start', description='Start / restart bot'),
    BotCommand(command='help', description='manuel for bot')]