from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboars.admin_inline_kb import make_category2_kb, make_confirm_kb, make_product3_kb, make_product_kb
from states.admin_state import ProductState
from utils.Database import Database
from config import db_name

product_router = Router()

db = Database(db_name)
@product_router.message(Command('add_product'))
async def add_product_handler(message: Message, state: FSMContext):
    await state.set_state(ProductState.add_SelectCategoryPS)
    await message.answer(
        text='Please choose a category which you want to add product...',
        reply_markup=make_category2_kb()
    )



@product_router.callback_query(ProductState.add_SelectCategoryPS)
async def add_product_cat_handler(query:CallbackQuery, state: FSMContext):
    await state.update_data(p_cat_id=query.data)
    await state.set_state(ProductState.add_TitlePS)
    await query.message.answer('Please, send title for product...')
    await query.message.delete()


@product_router.message(ProductState.add_TitlePS)
async def add_title_for_pr(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(p_title=message.text)
        await state.set_state(ProductState.add_TextPS)
        await message.answer('Please, send description for your product...')
    else:
        await message.answer('Please , send only text...')


@product_router.message(ProductState.add_TextPS)
async def add_text_for_pr(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(p_text=message.text)
        await state.set_state(ProductState.add_ImagePS)
        await message.answer('Please, send photo for your product...')
    else:
        await message.answer('Please , send only text...')


@product_router.message(ProductState.add_ImagePS)
async def add_image_for_pr(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(p_image=message.photo[-1].file_id)
        await state.set_state(ProductState.add_PricePS)
        await message.answer('Please, send price for your product...')
    else:
        await message.answer('Please , send only photo...')


@product_router.message(ProductState.add_PricePS)
async def add_price_for_pr(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(p_price=int(message.text))
        await state.set_state(ProductState.add_PhonePS)
        await message.answer('Please, send your contact or phone number in text format...')
    else:
        await message.answer('Please , send only numbers...')


@product_router.message(ProductState.add_PhonePS)
async def add_phone_for_pr(message: Message, state: FSMContext):
    if message.text or message.contact:
        phone = message.text if message.text else message.contact.phone_number
        await state.update_data(p_contact=phone)
        all_data = await state.get_data()
        print(all_data)
        result = db.add_product(
            p_cat_id=all_data.get('p_cat_id'),
            p_name=all_data.get('p_title'),
            p_text=all_data.get('p_text'),
            p_owner=str(message.from_user.id),
            p_phone=all_data.get('p_contact'),
            p_price=all_data.get('p_price'),
            p_image=all_data.get('p_image'))
        # if result:
        await message.answer('Your product successfully added!')
        product = db.get_my_last_pr(message.from_user.id)
        print(product)
        await message.answer_photo(
            photo=product[4],
            caption=f'{product[0]}\n\n{product[1]}\n\nPrice:{product[3]}\n\nContact:{product[2]}'
            )
        await state.clear()
    else:
        await message.answer('Please , send only contact or phone number in text format...')


@product_router.message(Command('del_product'))
async def add_product_handler(message: Message, state: FSMContext):
    await state.set_state(ProductState.startDeleteProductState)
    await message.answer(
        text='Please choose a product which you want to delete...',
        reply_markup=make_product3_kb()
    )


@product_router.callback_query(ProductState.startDeleteProductState)
async def select_product_del_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProductState.finishDeleteProductState)
    await state.update_data(prod_id=callback.data)
    await callback.message.edit_text(
        text=f"Do you want to delete product \"{callback.data}\":",
        reply_markup=make_confirm_kb()
    )


@product_router.callback_query(ProductState.finishDeleteProductState)
async def remove_product_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        all_data = await state.get_data()
        if db.delete_product(all_data.get('prod_id')):
            await callback.message.answer("product successfully deleted!")
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



@product_router.message(Command('products'))
async def get_select_product_handler(message:Message, state: FSMContext):
    await message.answer('Which ad do you want to see?')
    await message.answer(text='All products:', reply_markup=make_product3_kb())
    await state.set_state(ProductState.addsstate)



@product_router.callback_query(ProductState.addsstate)
async def get_product_ad_handler(callback: CallbackQuery, state: FSMContext):
    product = db.get_ad_pr(int(callback.data))
    await callback.message.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=product[4],
        caption=f'{product[0]}\n\n{product[1]}\n\nPrice:{product[3]}\n\nContact:{product[2]}'
    )
    await state.clear()