from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
import functions.common as com

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        'Зарегистрируйтесь (/regist)',
        reply_markup=types.ReplyKeyboardRemove()
    )

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())

# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def cmd_whoami(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        user = com.db.sqlFind('users', 'chat_username', f'id = "{message.chat.id}"')
        await message.answer(f'Привет, {user[0][0]}.')
    except:
        await message.answer(
        'Зарегистрируйтесь (/regist)',
        reply_markup=types.ReplyKeyboardRemove()
    )
    com.db.sqlDisconnect()

async def cmd_search(message: types.Message):
    try:
        if len(message.get_args().split()[0:]) > 0:
            await message.answer('Мне нужно подумать...')
            answer = com.search_(message.get_args()[0:])
            if len(answer) < 4096:
                await message.answer(answer)
            else:
                for i in range(0, len(answer), 4096):
                    await message.answer(answer[i:i+4096])
            media = types.MediaGroup()
            files = com.os.listdir('functions/processing/data/')
            files.sort()
            for i in range(1, 3):
                media.attach_photo(types.InputFile(f'functions/processing/wc{i}.png'))
            await message.answer_media_group(media=media)
            media = types.MediaGroup()
            for i in range(0, len(files), 10):
                for j in files[i:i+10]:
                    media.attach_photo(types.InputFile('functions/processing/data/'+j))
                await message.answer_media_group(media=media)
                media = types.MediaGroup()
        else:
            await message.answer('Неверный ввод')
    except:
        await message.answer('Неверный ввод')

# async def cmd_weather(message: types.Message):
#     if com.weath.connect(message.get_args().split()[0], message.get_args().split()[1]) != 'ok':
#         await message.answer('Неверный ввод')
#     else:
#         com.weath.now()
#         await message.answer_document(open('output.png', 'rb'))

async def cmd_secret_command_list(message: types.Message):
    cl = ['/get_file_id', 
    '/get_bot_log',
    '/get_bot_exel',
    '/bot_dialog_list',
    '/bot_dialog',
    '/bot_answer_add',
    '/bot_answer_remove',
    '/bot_question_add',
    '/bot_question_remove',
    '/bot_topic_remove',
    # '/bot_all_topic_remove', 
    ]
    await message.answer('Пожалуйста, выберите команду, используя клавиатуру ниже.', reply_markup=com.keyboardCreate(types.ReplyKeyboardMarkup(resize_keyboard=True), 2, int(len(cl) / 2), cl))

async def cmd_secret_get_file_id(message: types.Message):
    try:
        await getattr(message, 'answer_' + message.get_args().split()[0])(message.get_args().split()[1])
    except:
        await message.answer('Неверный ввод')

async def cmd_secret_get_bot_log(message: types.Message):
    await message.answer_document(open('bot_log.log', 'rb'))

async def cmd_secret_get_bot_exel(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        com.db.exelConnect('bot_exel')
        com.db.sqlToExel(message.get_args().split()[0])
        com.db.exelDisconnect()
        await message.answer_document(open('bot_exel.xlsx', 'rb'))
    except:
        await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        answer = com.db.sqlFind('dict', 'questions, answers', f'id = "{int(message.get_args().split()[0])}"')
        await message.answer(answer[0][0])
        await message.answer(answer[0][1])
    except:
        try:
            answer = com.db.sqlFind('dict', 'questions, answers', f'topic = "{message.get_args().split()[0]}"')
            await message.answer(answer[0][0])
            await message.answer(answer[0][1])
        except:
            await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog_list(message: types.Message):
    com.db.sqlConnect('bot_db')
    answer = com.db.sqlFind('dict', 'topic', 'id != ""')
    topics = []
    for i, topic in enumerate(answer):
        topics.append(str(i) + ': ' + topic[0])
        # await message.answer(topic[0])
    # await message.answer(('\n').join(topics))
    answer = ('\n').join(topics)
    if len(answer) < 4096:
        await message.answer(answer)
    else:
        for i in range(0, len(answer), 4096):
            await message.answer(answer[i:i+4096])
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog_answer_add(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        answer = com.db.sqlFind('dict', 'answers', f'id = "{int(message.get_args().split()[0])}"')
        answer = answer[0][0].split(' | ')
        answer.append((' ').join(message.get_args().split()[1:]))
        answer = (' | ').join(answer)
        com.db.sqlUpd('dict', f'answers = "{answer}"', f'id = "{int(message.get_args().split()[0])}"')
        answer = com.db.sqlFind('dict', 'answers', f'id = "{int(message.get_args().split()[0])}"')
        await message.answer(answer[0][0])
    except:
        try:
            answer = com.db.sqlFind('dict', 'answers', f'topic = "{message.get_args().split()[0]}"')
            answer = answer[0][0].split(' | ')
            answer.append((' ').join(message.get_args().split()[1:]))
            print(answer)
            answer = (' | ').join(answer)
            com.db.sqlUpd('dict', f'answers = "{answer}"', f'topic = "{message.get_args().split()[0]}"')
            answer = com.db.sqlFind('dict', 'answers', f'topic = "{message.get_args().split()[0]}"')
            await message.answer(answer[0][0])
        except:
            await message.answer('Неверный ввод')
    com.db.sqlDisconnect()
    
async def cmd_secret_bot_dialog_answer_remove(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        answer = com.db.sqlFind('dict', 'answers', f'id = "{int(message.get_args().split()[0])}"')
        answer = answer[0][0].split(' | ')
        answer.remove((' ').join(message.get_args().split()[1:]))
        answer = (' | ').join(answer)
        com.db.sqlUpd('dict', f'answers = "{answer}"', f'id = "{int(message.get_args().split()[0])}"')
        answer = com.db.sqlFind('dict', 'answers', f'id = "{int(message.get_args().split()[0])}"')
        await message.answer(answer[0][0])
    except:
        try:
            answer = com.db.sqlFind('dict', 'answers', f'topic = "{message.get_args().split()[0]}"')
            answer = answer[0][0].split(' | ')
            answer.remove((' ').join(message.get_args().split()[1:]))
            answer = (' | ').join(answer)
            com.db.sqlUpd('dict', f'answers = "{answer}"', f'topic = "{message.get_args().split()[0]}"')
            answer = com.db.sqlFind('dict', 'answers', f'topic = "{message.get_args().split()[0]}"')
            await message.answer(answer[0][0])
        except:
            await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog_question_add(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        question = com.db.sqlFind('dict', 'questions', f'id = "{int(message.get_args().split()[0])}"')
        question = question[0][0].split(' | ')
        question.append((' ').join(message.get_args().split()[1:]))
        question = (' | ').join(question)
        com.db.sqlUpd('dict', f'questions = "{question}"', f'id = "{int(message.get_args().split()[0])}"')
        question = com.db.sqlFind('dict', 'questions', f'id = "{int(message.get_args().split()[0])}"')
        await message.answer(question[0][0])
    except:
        try:
            question = com.db.sqlFind('dict', 'questions', f'topic = "{message.get_args().split()[0]}"')
            question = question[0][0].split(' | ')
            question.append((' ').join(message.get_args().split()[1:]))
            question = (' | ').join(question)
            com.db.sqlUpd('dict', f'questions = "{question}"', f'topic = "{message.get_args().split()[0]}"')
            question = com.db.sqlFind('dict', 'questions', f'topic = "{message.get_args().split()[0]}"')
            await message.answer(question[0][0])
        except:
            await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog_question_remove(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        question = com.db.sqlFind('dict', 'questions', f'id = "{int(message.get_args().split()[0])}"')
        question = question[0][0].split(' | ')
        question.remove((' ').join(message.get_args().split()[1:]))
        question = (' | ').join(question)
        com.db.sqlUpd('dict', f'questions = "{question}"', f'id = "{int(message.get_args().split()[0])}"')
        question = com.db.sqlFind('dict', 'questions', f'id = "{int(message.get_args().split()[0])}"')
        await message.answer(question[0][0])
    except:
        try:
            question = com.db.sqlFind('dict', 'questions', f'topic = "{message.get_args().split()[0]}"')
            question = question[0][0].split(' | ')
            question.remove((' ').join(message.get_args().split()[1:]))
            question = (' | ').join(question)
            com.db.sqlUpd('dict', f'questions = "{question}"', f'topic = "{message.get_args().split()[0]}"')
            question = com.db.sqlFind('dict', 'questions', f'topic = "{message.get_args().split()[0]}"')
            await message.answer(question[0][0])
        except:
            await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog_topic_remove(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        if len(com.db.sqlFind('dict', 'id', f'id = "{int(message.get_args().split()[0])}"')) == 0:
            await message.answer(f'Тема "{int(message.get_args().split()[0])}" уже удалена')
        elif com.db.sqlFind('dict', 'id', f'id = "{int(message.get_args().split()[0])}"')[0][0] < 85:
            await message.answer(f'Тема "{int(message.get_args().split()[0])}" заблокирована от удаления')
        else:
            com.db.sqlDel('dict', f'id = "{int(message.get_args().split()[0])}"')
            await message.answer(f'Тема "{int(message.get_args().split()[0])}" сейчас будет удалена')
            fix = int(com.db.sqlFind('dict', 'id', 'id != ""')[84:][-1][0])
            fix_l = []
            for i in range(85, fix, 1):
                fix_l.append(i)
            db_l = []
            for i in range(0, len(com.db.sqlFind('dict', 'id', 'id != ""')[85:]), 1):
                db_l.append(int(com.db.sqlFind('dict', 'id', 'id != ""')[85:][i][0]))
            for i in range(len(db_l)):
                com.db.sqlUpd('dict', f'id = {fix_l[i]}', f'id = {db_l[i]}')
    except:
        try:
            if len(com.db.sqlFind('dict', 'id', f'topic = "{message.get_args().split()[0]}"')) == 0:
                await message.answer(f'Тема "{message.get_args().split()[0]}" уже удалена')
            elif com.db.sqlFind('dict', 'id', f'topic = "{message.get_args().split()[0]}"')[0][0] < 85:
                await message.answer(f'Тема "{message.get_args().split()[0]}" заблокирована от удаления')
            else:
                com.db.sqlDel('dict', f'topic = "{message.get_args().split()[0]}"')
                await message.answer(f'Тема "{message.get_args().split()[0]}" сейчас будет удалена')
                fix = int(com.db.sqlFind('dict', 'id', 'id != ""')[84:][-1][0])
                fix_l = []
                for i in range(85, fix, 1):
                    fix_l.append(i)
                db_l = []
                for i in range(0, len(com.db.sqlFind('dict', 'id', 'id != ""')[85:]), 1):
                    db_l.append(int(com.db.sqlFind('dict', 'id', 'id != ""')[85:][i][0]))
                for i in range(len(db_l)):
                    com.db.sqlUpd('dict', f'id = {fix_l[i]}', f'id = {db_l[i]}')
        except:
            await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

async def cmd_secret_bot_dialog_all_topic_remove(message: types.Message):
    com.db.sqlConnect('bot_db')
    try:
        com.db.sqlDel('dict', 'id > 84')
        await message.answer('Готово')
    except:
        await message.answer('Неверный ввод')
    com.db.sqlDisconnect()

# async def cmd_search(message: types.Message):
#     print(message)
#     await message.answer(message)

async def cmd_secret_exit(message: types.Message):
    await message.answer('Бот прекратил работу')
    # com.sys.exit()
    com.os._exit()

def register_handlers_common(dp: Dispatcher, admin_id: int, bot):
    global Bot
    Bot = bot
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(cmd_whoami, commands='whoami')
    dp.register_message_handler(cmd_search, commands='search')
    # dp.register_message_handler(cmd_weather, commands='weather')
    dp.register_message_handler(cmd_secret_command_list, IDFilter(user_id=admin_id), commands='cl')
    dp.register_message_handler(cmd_secret_get_file_id, IDFilter(user_id=admin_id), commands='get_file_id')
    dp.register_message_handler(cmd_secret_get_bot_log, IDFilter(user_id=admin_id), commands='get_bot_log')
    dp.register_message_handler(cmd_secret_get_bot_exel, IDFilter(user_id=admin_id), commands='get_bot_exel')
    dp.register_message_handler(cmd_secret_bot_dialog, IDFilter(user_id=admin_id), commands='bot_dialog')
    dp.register_message_handler(cmd_secret_bot_dialog_list, IDFilter(user_id=admin_id), commands='bot_dialog_list')
    dp.register_message_handler(cmd_secret_bot_dialog_answer_add, IDFilter(user_id=admin_id), commands='bot_answer_add')
    dp.register_message_handler(cmd_secret_bot_dialog_answer_remove, IDFilter(user_id=admin_id), commands='bot_answer_remove')
    dp.register_message_handler(cmd_secret_bot_dialog_question_add, IDFilter(user_id=admin_id), commands='bot_question_add')
    dp.register_message_handler(cmd_secret_bot_dialog_question_remove, IDFilter(user_id=admin_id), commands='bot_question_remove')
    dp.register_message_handler(cmd_secret_bot_dialog_topic_remove, IDFilter(user_id=admin_id), commands='bot_topic_remove')
    dp.register_message_handler(cmd_secret_bot_dialog_all_topic_remove, IDFilter(user_id=admin_id), commands='bot_all_topic_remove')
    dp.register_message_handler(cmd_secret_exit, IDFilter(user_id=admin_id), commands='exit')
    # dp.register_message_handler(cmd_search, commands='search')
    