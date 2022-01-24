from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import functions.common as com
# import pickle
# import database
# import cities_test

# cities_test.connect()
# print('загрузка')
# cities = cities_test.filt()[0]
# names = cities_test.filt()[1]

names = ['molly', 'stephen', 'chester', 'irene', 'edward', 'ernie', 'ralph', 'gregory', 'jerry', 'robert']

# available_drinks_names = ["чай", "кофе", "какао"]
# available_drinks_sizes = ["250мл", "0.5л", "1л"]


class OrderNames(StatesGroup):
    waiting_for_Name_name = State()


async def names_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # for i in range(0, 10, 1):
    #     keyboard.add(names[i].lower())
    await message.answer("Выберите имя:", reply_markup=com.keyboardCreate(keyboard, 2, 5, names))
    await OrderNames.waiting_for_Name_name.set()


async def names_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in names[:10]:
        await message.answer("Пожалуйста, выберите имя, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_name=message.text.lower())
    user_data = await state.get_data()
    name = user_data['chosen_name']
    com.save_obj(name, 'name')
    print(user_data['chosen_name'])
    
    await message.answer(f"Вы выбрали имя {user_data['chosen_name'].capitalize()}.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

# def save_obj(obj, name):
#     with open(name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def register_handlers_name(dp: Dispatcher):
    dp.register_message_handler(names_start, commands="name", state="*")
    dp.register_message_handler(names_chosen, state=OrderNames.waiting_for_Name_name)