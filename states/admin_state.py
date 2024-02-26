from aiogram.fsm.state import State,StatesGroup

class CategoryState(StatesGroup):
    addcategory = State()

    startEditCategoryState = State()
    finishEditCategoryState = State()

    startDeleteCategoryState = State()
    finishDeleteCategoryState = State()

    addproduct = State()






class ProductState(StatesGroup):
    add_SelectCategoryPS = State()
    add_TitlePS = State()
    add_TextPS = State()
    add_ImagePS = State()
    add_PricePS = State()
    add_PhonePS = State()

    startDeleteProductState = State()
    finishDeleteProductState = State()

    addsstate = State()


