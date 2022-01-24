from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import functions.common as com

p_lg_l = ['Python', 'Java', 'C']

class сhoice(StatesGroup):
    name = State()
    p_lg = State()

async def сhoice_start(message: types.Message):
    name_l = [message.chat.username, message.chat.first_name, message.chat.last_name]
    while name_l.count(None) != 0:
        name_l.remove(None)

    await сhoice.name.set()
    await message.answer('Пожалуйста, введите имя: ', reply_markup=com.keyboardCreate(types.ReplyKeyboardMarkup(resize_keyboard=True), 2, 2, name_l))

async def set_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.html_text
    await сhoice.next()
    await сhoice.p_lg.set()
    await message.answer('Пожалуйста, выберите язык программирования: ', reply_markup=com.keyboardCreate(types.ReplyKeyboardMarkup(resize_keyboard=True), 2, 2, p_lg_l))

async def p_lg_chosen(message: types.Message, state: FSMContext):
    if message.text not in p_lg_l:
        await message.answer('Пожалуйста, выберите язык программирования, используя клавиатуру ниже.', reply_markup=com.keyboardCreate(types.ReplyKeyboardMarkup(resize_keyboard=True), 2, 2, p_lg_l))
        return
    async with state.proxy() as data:
        data['p_lg'] = message.text
    await message.answer(f"Привет, {data['name']}. Вами был выбран язык: {data['p_lg']}.", parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    if not com.os.path.exists('bot_db.db'):
        com.db.sqlConnect('bot_db')
        users_l = ['chat_type TEXT', 'chat_username TEXT', 'chat_parameters TEXT']
        com.db.sqlCreate('users', users_l)
    com.db.sqlConnect('bot_db')
    user = [message.chat.id, message.chat.type, data['name'], data['p_lg']]
    com.db.sqlAdd('users', user, 4)
    com.db.exelConnect('bot_exel')
    com.db.sqlToExel('users')
    com.db.exelDisconnect()
    com.db.sqlDisconnect()

def register_handlers_choice(dp: Dispatcher):
    dp.register_message_handler(сhoice_start, commands='regist', state=None)
    dp.register_message_handler(set_name, state=сhoice.name)
    dp.register_message_handler(p_lg_chosen, state=сhoice.p_lg)
