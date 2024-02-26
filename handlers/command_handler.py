from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import db_name
from keyboars.admin_inline_kb import make_category_kb, make_confirm_kb, make_product_kb
from states.admin_state import CategoryState
from utils.Database import Database

from config import admins
from utils.my_commands import admin_commands, user_commands

db = Database(db_name)
command_router = Router()

@command_router.message(CommandStart())
async def start_handler(message:Message):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=admin_commands)
        await message.answer('Dear admin, welcome!')
    else:
        await message.bot.set_my_commands(commands=user_commands)
        await message.answer('Welcome!')


@command_router.message(Command('categories'))
async def get_category_handler(message:Message):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=admin_commands)
        await message.answer(text='All categories:', reply_markup=make_category_kb())
    else:
        await message.bot.set_my_commands(commands=user_commands)
        await message.answer('Welcome!')

@command_router.message(Command('add_categories'))
async def add_category_handler(message:Message, state: FSMContext):
    if message.from_user.id in admins:
        await message.bot.set_my_commands(commands=admin_commands)
        await state.set_state(CategoryState.addcategory)
        await message.answer(text='Please, send name for new category.')
    else:
        await message.bot.set_my_commands(commands=user_commands)
        await message.answer('Sorry, you are not admin.')


@command_router.message(CategoryState.addcategory)
async def insert_category_handler(message: Message, state=FSMContext):
    if db.check_category_exists(message.text):
        if db.add_category(new_category  =message.text):
            await state.clear()
            await message.answer(
                f"New category by name '{message.text}' successfully added!"
            )
        else:
            await message.answer(
                f"Something error, resend category"
                f"Send again or click /cancel for cancel process!"
            )
    else:
        await message.answer(
            f"Category \"{message.text}\" already exists\n"
            f"Send other name or click /cancel for cancel process!"
        )


@command_router.message(Command('update_category'))
async def edit_category_handler(message: Message, state=FSMContext):
    await state.set_state(CategoryState.startEditCategoryState)
    await message.answer(
        text="Select category which you want change:",
        reply_markup=make_category_kb()
    )


@command_router.callback_query(CategoryState.startEditCategoryState)
async def select_category_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CategoryState.finishEditCategoryState)
    await state.update_data(cat_name=callback.data)
    await callback.message.edit_text(f"Please, send new name for category \"{callback.data}\":")


@command_router.message(CategoryState.finishEditCategoryState)
async def update_category_handler(message: Message, state=FSMContext):
    if db.check_category_exists(message.text):
        all_data = await state.get_data()
        if db.rename_category(old_name=all_data.get('cat_name'), new_name=message.text):
            await state.clear()
            await message.answer(
                f"Category name successfully modified!"
            )
    else:
        await message.answer(
            f"Category \"{message.text}\" already exists\n"
            f"Send other name or click /cancel for cancel process!"
        )


@command_router.message(Command('del_category'))
async def del_category_handler(message: Message, state=FSMContext):
    await state.set_state(CategoryState.startDeleteCategoryState)
    await message.answer(
        text="Select category which you want to delete:",
        reply_markup=make_category_kb()
    )


@command_router.callback_query(CategoryState.startDeleteCategoryState)
async def select_category_del_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CategoryState.finishDeleteCategoryState)
    await state.update_data(cat_name=callback.data)
    await callback.message.edit_text(
        text=f"Do you want to delete category \"{callback.data}\":",
        reply_markup=make_confirm_kb()
    )


@command_router.callback_query(CategoryState.finishDeleteCategoryState)
async def remove_category_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        all_data = await state.get_data()
        if db.delete_category(all_data.get('cat_name')):
            await callback.message.answer("Category successfully deleted!")
            await callback.message.delete()
            await state.clear()
        else:
            await callback.message.answer(
                f"Something went wrong!"
                f"Try again later or click /cancel for cancel process!"
            )
    else:
        await state.clear()
        await callback.message.answer('Process canceled!')
        await callback.message.delete()


@command_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("All actions cancelled!")


# @command_router.message(Command('products'))
# async def get_product_handler(message:Message):
#     if message.from_user.id in admins:
#         await message.bot.set_my_commands(commands=admin_commands)
#         await message.answer(text='All products:', reply_markup=make_product_kb())
#     else:
#         await message.bot.set_my_commands(commands=user_commands)
#         await message.answer('Welcome!')
#
# @command_router.message(Command('add_product'))
# async def add_product_handler(message:Message, state: FSMContext):
#     if message.from_user.id in admins:
#         await message.bot.set_my_commands(commands=admin_commands)
#         await state.set_state(CategoryState.addproduct)
#         await message.answer(text='Please, send name for new product.')
#     else:
#         await message.bot.set_my_commands(commands=user_commands)
#         await message.answer('Sorry, you are not admin.')
#
#
# @command_router.message(CategoryState.addproduct)
# async def insert_product_handler(message: Message, state=FSMContext):
#     if db.check_product_exists(message.text):
#         if db.add_product(new_product=message.text):
#             await state.clear()
#             await message.answer(
#                 f"New product by name '{message.text}' successfully added!"
#             )
#         else:
#             await message.answer(
#                 f"Something error, resend category"
#                 f"Send again or click /cancel for cancel process!"
#             )
#     else:
#         await message.answer(
#             f"Category \"{message.text}\" already exists\n"
#             f"Send other name or click /cancel for cancel process!"
#         )
#
#
# @command_router.message(Command('edit_product'))
# async def edit_product_handler(message: Message, state=FSMContext):
#     await state.set_state(CategoryState.startEditProductState)
#     await message.answer(
#         text="Select product which you want change:",
#         reply_markup=make_product_kb()
#     )
#
#
# @command_router.callback_query(CategoryState.startEditProductState)
# async def select_product_handler(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(CategoryState.finishEditProductState)
#     await state.update_data(prod_name=callback.data)
#     await callback.message.edit_text(f"Please, send new name for product\"{callback.data}\":")
#
#
# @command_router.message(CategoryState.finishEditProductState)
# async def update_product_handler(message: Message, state=FSMContext):
#     if db.check_product_exists(message.text):
#         all_data = await state.get_data()
#         if db.rename_product(old_name=all_data.get('prod_name'), new_name=message.text):
#             await state.clear()
#             await message.answer(
#                 f"Product name successfully modified!"
#             )
#     else:
#         await message.answer(
#             f"Product \"{message.text}\" already exists\n"
#             f"Send other name or click /cancel for cancel process!"
#         )
#
#
# @command_router.message(Command('del_product'))
# async def del_product_handler(message: Message, state=FSMContext):
#     await state.set_state(CategoryState.startDeleteProductState)
#     await message.answer(
#         text="Select product which you want to delete:",
#         reply_markup=make_product_kb()
#     )
#
#
# @command_router.callback_query(CategoryState.startDeleteProductState)
# async def select_product_del_handler(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(CategoryState.finishDeleteProductState)
#     await state.update_data(prod_name=callback.data)
#     await callback.message.edit_text(
#         text=f"Do you want to delete product \"{callback.data}\":",
#         reply_markup=make_confirm_kb()
#     )
#
#
# @command_router.callback_query(CategoryState.finishDeleteProductState)
# async def remove_product_handler(callback: CallbackQuery, state: FSMContext):
#     if callback.data == 'YES':
#         all_data = await state.get_data()
#         if db.delete_product(all_data.get('prod_name')):
#             await callback.message.answer("product successfully deleted!")
#             await callback.message.delete()
#             await state.clear()
#         else:
#             await callback.message.answer(
#                 f"Something went wrong!"
#                 f"Try again later or click /cancel for cancel process!"
#             )
#     else:
#         await state.clear()
#         await callback.message.answer('Process canceled!')
#         await callback.message.delete()


@command_router.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("All actions cancelled!")