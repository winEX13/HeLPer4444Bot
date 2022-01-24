# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 23:37:04 2021

@author: winEX
"""


#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.utils.exceptions import Throttled
from config_reader import load_config
from handlers.common import register_handlers_common
from handlers.choice import register_handlers_choice
import functions.common as com
# from contextlib import suppress
import asyncio
import nest_asyncio
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# import os
# import os.path
# from sys import exit
# import re
# import pickle
# import database

# def textFmtH(text, fmt):
#     switcher = 

#         'курсив': '<i>',
#         'экспресс': '<em>',
#         'жирный': '<b>',
#         'важный': '<strong>',
#         # 'выделенный': '<mark>',
#         # 'маленький': '<small>',
#         'удален': '<del>',
#         'зачеркнутый': '<s>',
#         'подчеркнутый': '<ins>',
#         'подчеркнутый по умолчанию': '<u>',
#         # 'нижний': '<sub>',
#         # 'верхний': '<sup>',
#         # 'новый': '<dfn>',
#         # 'время': ''
#     }
    
#     fmt = switcher.get(fmt, 'Invalid')
#     if fmt == 'Invalid':
#         exit('Error: Formats: курсив, экспресс, жирный, важный, удален, зачеркнутый, подчеркнутый, подчеркнутый по умолчанию')
#     text = fmt + text + fmt[:1] + '/' + fmt[1:]
#     return (text)

def textFmtH(text, fmrt):
    switcher = { 
        'курсив': 'hitalic',
        'жирный': 'hbold',
        'подчеркнутый': 'hunderline',
        'зачеркнутый': 'hstrikethrough',
        'моно': 'hcode',
        'моно блок': 'hpre',
        'ссылка': 'hlink',
        'невидимая ссылка': 'hide_link',
        'цитата': 'quote_html',
        'обычный': 'text'
    }
    
    if switcher.get(fmrt, 'Invalid') == 'Invalid':
        exit('Error: Formats: курсив, жирный, подчеркнутый, зачеркнутый, моно, моно блок, ссылка, невидимая ссылка, цитата, обычный')
    elif switcher.get(fmrt, 'Invalid') == 'hlink':
        print(text[:text.find(' ')], text[text.find(' '):])
        return (getattr(fmt, switcher.get(fmrt, 'Invalid'))(text[:text.find(' ')], text[text.find(' ') + 1:]))
    return (getattr(fmt, switcher.get(fmrt, 'Invalid'))(text))

def keyboardCreate(keyboard, row, column, lst):
    buttons_row = []
    buttons = []
    # for b in lst:
    for r in range(0, column + 3, row):
        for c in range(row):
            try:
                buttons_row.append(lst[c+r])
            except IndexError:
                buttons_row.append('')
        buttons.append(buttons_row)
        buttons_row = []
    for row in buttons:
        keyboard.add(*row)
    return(keyboard)

def inlineKeyboardCreate(keyboard, row, column, lst):
    buttons_row = []
    buttons = []
    # for b in lst:
    for r in range(0, column + 3, row):
        for c in range(row):
            try:
                buttons_row.append(types.InlineKeyboardButton(text=str(lst[c+r][0]), callback_data=str(lst[c+r][1])))
            except IndexError:
                pass
                # buttons_row.append('')
        buttons.append(buttons_row)
        buttons_row = []
    for row in buttons:
        if len(row) > 0:
            keyboard.add(*row)
    return(keyboard)

# nest_asyncio.apply()
# __import__('IPython').embed()

# ---->loop = nest_asyncio.apply()
# loop = asyncio.get_event_loop()

# Объект бота
# bot = Bot(token='2121458195:AAGrVB1aoYfNBEE7f8lRQsld-UuTH4UgoC0')
# bot_token = getenv('BOT_TOKEN')

# bot = Bot(token=config.tg_bot.token)

# if not os.path.exists('BOT_TOKEN.txt'):
#     exit('Error: No such file or directory')
# else:
#     with open('BOT_TOKEN.txt', 'r') as f:
#         bot_token = f.read()
#     if not bot_token or bot_token == '':
#         exit('Error: No token provided')
#     else:
#         try:
#             bot = Bot(token=bot_token)
#         except:
#             exit('Error: Token is invalid!')
            
# Диспетчер для бота
# dp = Dispatcher(bot, loop=loop)
# dp = Dispatcher(bot, storage=MemoryStorage())
# register_handlers_common(dp, config.tg_bot.admin_id)
# await set_commands(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)


# Хэндлер на команду /test1
# @dp.message_handler(commands='test1')
# async def cmd_test1(message: types.Message):
    # await message.answer(textFmt('hello', 'экспресс'), parse_mode=types.ParseMode.HTML)
    # await message.answer(fmt(), parse_mode=types.ParseMode.HTML)
    # await message.answer(message.html_text)
    # await message.reply('Test 1')
    # await message.answer('Сообщение с <u>HTML-разметкой</u>')
    # await message.answer(
    #     fmt.text(
    #         fmt.text(fmt.hunderline('Яблоки'), ', вес 1 кг.'),
    #         fmt.text('Старая цена:', fmt.hstrikethrough(50), 'рублей'),
    #         fmt.text('Новая цена:', fmt.hbold(25), 'рублей'),
    #         sep='\n'
    #     ), parse_mode='HTML'
    # )
    # await message.answer(f'<u>Ваш текст</u>:\n\n{message.html_text}', parse_mode='HTML')

# @dp.message_handler(commands='start')
# async def cmd_start(message: types.Message):
#     ls = ['1', '2', '3', '4', '5', '6', '7']
#     await message.answer('Как подавать котлеты?', reply_markup=keyboardCreate(types.ReplyKeyboardMarkup(resize_keyboard=True), 3, 4, ls))
    
# @dp.message_handler(Text(equals='2'))
# async def with_puree(message: types.Message):
#     await message.reply('Отличный выбор!')
    
# @dp.message_handler(commands='special_buttons')
# async def cmd_special_buttons(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text='Запросить геолокацию', request_location=True))
#     keyboard.add(types.KeyboardButton(text='Запросить контакт', request_contact=True))
#     keyboard.add(types.KeyboardButton(text='Создать викторину',
#                                       request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
#     await message.answer('Выберите действие:', reply_markup=keyboard)

# @dp.message_handler(commands='in')
# async def cmd_inline_url(message: types.Message):
#     ls = [
#         ['-1', 'sdsfs'],
#         ['+1', 'num_incr'],
#         ['Подтвердить', 'num_finish'],
#         # ['4', '4'],
#         # ['5', '5'],
#         # ['6', 'random_value'],
#         # ['7', '7'],
#         # ['8', 'random_value']
#         ]
#     await message.answer('Кнопки-ссылки', reply_markup=inlineKeyboardCreate(types.InlineKeyboardMarkup(), 2, 2, ls))
    
# @dp.callback_query_handler(text='sdsfs')
# async def send_random_value(call: types.CallbackQuery):
#     # await call.message.answer('отстань')
#     # await message.edit_text(f'Укажите число: {new_value}', reply_markup=get_keyboard())
#     # await call.answer(text='Спасибо, что воспользовались ботом!', show_alert=True)
#     with suppress(MessageNotModified):
#         await call.message.edit_text(call.message.text)
#         print(call.message)
#     await call.answer()

# @dp.message_handler()
# async def any_text_message2(message: types.Message):
#     # await message.answer(textFmtH(message.html_text, 'ссылка'), parse_mode='HTML')
#     text = message.html_text
#     if re.search('(?P<url>https?://[^\s]+)', text) != None:
#         while re.search('(?P<url>https?://[^\s]+)', text).group('url') != '':
#             print ('а вот и ссылочка: ', re.search('(?P<url>https?://[^\s]+)', text).group('url'))
#             text = text.replace((re.search('(?P<url>https?://[^\s]+)', text).group('url')), '')

# @dp.message_handler(content_types=[types.ContentType.TEXT])
# # async def echo_document(message: types.Message):
# #     await message.reply_animation(message.animation.file_id)
# async def TEXT(message: types.Message):
#     await message.text.download()
   
# @dp.message_handler(content_types=[types.ContentType.ANIMATION])
# async def ANIMATION(message: types.Message):
#     await message.animation.download()
    
# @dp.message_handler(content_types=[types.ContentType.AUDIO])
# async def AUDIO(message: types.Message):
#     await message.audio.download()

# @dp.message_handler(content_types=[types.ContentType.DOCUMENT])
# async def DOCUMENT(message: types.Message):
#     await message.document.download()
    
# # @dp.message_handler(content_types=[types.ContentType.GAME])
# # async def GAME(message: types.Message):
# #     await message.game.download()
    
# @dp.message_handler(content_types=[types.ContentType.PHOTO])
# async def PHOTO(message: types.Message):
#     await message.photo[-1].download()
    
# @dp.message_handler(content_types=[types.ContentType.STICKER])
# async def STICKER(message: types.Message):
#     await message.sticker.download()
    
# @dp.message_handler(content_types=[types.ContentType.VIDEO])
# async def VIDEO(message: types.Message):
#     await message.video.download()
    
# @dp.message_handler(content_types=[types.ContentType.VIDEO_NOTE])
# async def VIDEO_NOTE(message: types.Message):
#     await message.video_note.download()
    
# @dp.message_handler(content_types=[types.ContentType.VOICE])
# async def VOICE(message: types.Message):
#     await message.voice.download()
    
# @dp.message_handler(content_types=[types.ContentType.CONTACT])
# async def CONTACT(message: types.Message):
# #     await message.contact.download()
#     print(message.contact)
    
# @dp.message_handler(content_types=[types.ContentType.LOCATION])
# async def LOCATION(message: types.Message):
# #     await message.location.download()
#     print(message.location)
    
# # @dp.message_handler(content_types=[types.ContentType.VENUE])
# # async def VENUE(message: types.Message):
# #     await message.venue.download()
    
# @dp.message_handler(content_types=[types.ContentType.POLL])
# async def POLL(message: types.Message):
# #     await message.poll.download()
#     print(message.poll)
    
# @dp.message_handler(content_types=[types.ContentType.DICE])
# async def DICE(message: types.Message):
#     # await message.dice.download()
#     print (message.dice)
    
# @dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
# async def NEW_CHAT_MEMBERS(message: types.Message):
#     await message.new_chat_members.download()
    
# @dp.message_handler(content_types=[types.ContentType.LEFT_CHAT_MEMBER])
# async def LEFT_CHAT_MEMBER(message: types.Message):
#     await message.left_chat_members.download()
    
# @dp.message_handler(content_types=[types.ContentType.INVOICE])
# async def INVOICE(message: types.Message):
#     await message.invoice.download()
    
# @dp.message_handler(content_types=[types.ContentType.SUCCESSFUL_PAYMENT])
# async def SUCCESSFUL_PAYMENT(message: types.Message):
#     await message.successful_payment.download()
    
# @dp.message_handler(content_types=[types.ContentType.CONNECTED_WEBSITE])
# async def CONNECTED_WEBSITE(message: types.Message):
#     await message.connected_website.download()
    
# @dp.message_handler(content_types=[types.ContentType.MIGRATE_TO_CHAT_ID])
# async def MIGRATE_TO_CHAT_ID(message: types.Message):
#     await message.migrate_to_chat_id.download()
    
# @dp.message_handler(content_types=[types.ContentType.MIGRATE_FROM_CHAT_ID])
# async def MIGRATE_FROM_CHAT_ID(message: types.Message):
#     await message.migrate_from_chat_id.download()
    
# @dp.message_handler(content_types=[types.ContentType.UNKNOWN])
# async def UNKNOWN(message: types.Message):
#     await message.unknown.download()
    
# @dp.message_handler(content_types=[types.ContentType.ANY])
# async def ANY(message: types.Message):
#     await message.any.download()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/regist', description='Регистрация'),
        BotCommand(command='/whoami', description='Узнать кто ты'),
        BotCommand(command='search', description='Поиск в интернете'),
        BotCommand(command='/start', description='Начать'),
        BotCommand(command='/cancel', description='Отменить текущее действие'),

        BotCommand(command='/cl', description='Список команд'),
        
        # BotCommand(command='/get_file_id', description='Получить любой файл через file_id (Доступно админу)'),
        # BotCommand(command='/get_bot_log', description='Логи бота (Доступно админу)'),
        # BotCommand(command='/get_bot_exel', description='База данных бота (Доступно админу)'),
        
        # BotCommand(command='/bot_dialog_list', description='Просмотр списка тем диалогов (Доступно админу)'),
        # BotCommand(command='/bot_dialog', description='Просмотр параметров диалога (Доступно админу)'),
        # BotCommand(command='/bot_answer_add', description='Добавить ответ бота (Доступно админу)'),
        # BotCommand(command='/bot_answer_remove', description='Убрать ответ бота (Доступно админу)'),
        # BotCommand(command='/bot_question_add', description='Добавить параметр вопроса (Доступно админу)'),
        # BotCommand(command='/bot_question_remove', description='Убрать параметр вопроса (Доступно админу)'),
        
        # BotCommand(command='/bot_topic_remove', description='Убрать тему (Доступно админу)'),
        # BotCommand(command='/bot_all_topic_remove', description='Убрать темы (Доступно админу)'),
    ]
    await bot.set_my_commands(commands)

logger = logging.getLogger(__name__)

anti_flood = {}

async def any_text(message: types.Message):

    if message.chat.id in anti_flood and abs(message.date - anti_flood[message.chat.id]) <= com.datetime.timedelta(seconds=10):
        await message.answer('Мне нужно подумать...')
        print(f'Пользователь "{message.chat.username}" из |{message.chat.id}| спамит сообщения')
    else:
        print(message.chat.type, message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.message_id, message.text)
        # logger.info('Сообщение: ' + str(message.chat.type) + ' ' + str(message.chat.id) + ' ' + str(message.chat.first_name)  + ' ' + str(message.chat.last_name) + ' ' + str(message.chat.username) + ' ' + str(message.message_id) + ' ' + str(message.text))
        if message.text != None and message.text[0] != '/':
            answer = com.dialoge(message.text, 0)
            await message.answer(answer, reply_markup=types.ReplyKeyboardRemove())
            if answer == 'Извините, я вас не понимаю.':
                logger.error('Сообщение: ' + str(message.chat.type) + ' ' + str(message.chat.id) + ' ' + str(message.chat.first_name)  + ' ' + str(message.chat.last_name) + ' ' + str(message.chat.username) + ' ' + str(message.message_id) + ' ' + str(message.text))
            else:
                logger.info('Сообщение: ' + str(message.chat.type) + ' ' + str(message.chat.id) + ' ' + str(message.chat.first_name)  + ' ' + str(message.chat.last_name) + ' ' + str(message.chat.username) + ' ' + str(message.message_id) + ' ' + str(message.text))
        for i in message.entities: 
            print(i.type, i.offset, i.length)
            logger.info('Команда: ' + str(i.type) + ' ' + str(i.offset) + ' ' + str(i.length))
            await message.answer('Команда не сработала. Проверьте правильность или станьте админом.', reply_markup=types.ReplyKeyboardRemove())
        for i in message.photo: 
            print(i.file_id, i.file_size, i.width, i.height)
            logger.info('Фото: ' + str(i.file_id) + ' ' + str(i.file_size) + ' ' + str(i.width) + ' ' + str(i.height))
        if len(message.photo) != 0:
            await message.answer('Мне нужно подумать...')
            await message.photo[-1].download('functions/processing/img.png')
            answer = com.img2dialoge()
            await message.answer(answer)
        if message.animation != None:
            print(message.animation.file_id, message.animation.file_name, message.animation.mime_type, message.animation.file_size, message.animation.duration, message.animation.width, message.animation.height)
            logger.info('Анимация: ' + str(message.animation.file_id) + ' ' + str(message.animation.file_name) + ' ' + str(message.animation.mime_type) + ' ' + str(message.animation.file_size) + ' ' + str(message.animation.duration) + ' ' + str(message.animation.width) + ' ' + str(message.animation.height))
            await message.answer('Извините, меня пока не научили работать с анимацией...')
        if message.document != None:
            print(message.document.file_id, message.document.file_name, message.document.mime_type, message.document.file_size)
            logger.info('Документ: ' + str(message.document.file_id) + ' ' + str(message.document.file_name) + ' ' + str(message.document.mime_type) + ' ' + str(message.document.file_size))
            name = str(message.document.file_name)
            if com.count(list(name))['.'] == 1:
                if '.py' in name:
                    await message.document.download(f'functions/processing/doc{name[name.find("."):]}')
                    with open(f'functions/processing/doc{name[name.find("."):]}', 'r', encoding='UTF-8') as f:
                        lines = f.readlines()
                        file = []
                        for i in range(len(lines)):
                            file.append(str(i+1) + ':' + ' '*(len(str(len(lines))) - len(str(i+1))) + '|' + lines[i])
                        if len(('').join(file)) < 4096:
                            await message.answer(com.textFmtH(('').join(file), 'моно блок'), parse_mode='HTML')
                        else:
                            for i in range(0, len(('').join(file)), 4096):
                                await message.answer(com.textFmtH(('').join(file)[i:i+4096], 'моно блок'), parse_mode='HTML')
                    await message.answer('Мне нужно подумать...')
                    answer = com.pyCheck.getErrors()
                    print(answer)
                    if answer != '':
                        if len(answer) < 4096:
                            await message.answer(answer)
                        else:
                            for i in range(0, len(answer), 4096):
                                await message.answer(answer[i:i+4096])
                    else:
                        await message.answer('Все в порядке!')
                else:
                    await message.answer('Извините, меня пока не научили работать с файлами такого формата...')
            else:
                await message.answer('Я обрабатываю файлы с одной точкой в названии')
                await message.answer('Переименуйте файл')
        if message.location != None:
            print(message.location.latitude, message.location.longitude)
            logger.info('Геопозиция: ' + str(message.location.latitude) + ' ' + str(message.location.longitude))
            await message.answer('Извините, меня пока не научили работать с геопозицией...')
        if message.contact != None:
            print(message.contact.first_name, message.contact.last_name, message.contact.phone_number)
            logger.info('Контакт: ' + str(message.contact.first_name) + ' ' + str(message.contact.last_name) + ' ' + str(message.contact.phone_number))
            await message.answer('Извините, меня пока не научили работать с контактами...')
        if message.audio != None:
            print(message.audio.file_id, message.audio.file_name, message.audio.mime_type, message.audio.duration, message.audio.file_size)
            logger.info('Музыка: ' + str(message.audio.file_id) + ' ' + str(message.audio.file_name) + ' ' + str(message.audio.mime_type) + ' ' + str(message.audio.duration) + ' ' + str(message.audio.file_size))
            await message.answer('Извините, меня пока не научили работать с музыкой...')
        if message.voice != None:
            print(message.voice.file_id, message.voice.mime_type, message.voice.duration, message.voice.file_size)
            logger.info('Аудио: ' + str(message.voice.file_id) + ' ' + str(message.voice.mime_type) + ' ' + str(message.voice.duration) + ' ' + str(message.voice.file_size))
            await message.answer('Мне нужно подумать...')
            await message.voice.download('functions/processing/aud.wav')
            answer = com.aud2dialoge()
            await message.answer(answer)
        if message.video_note != None:
            print(message.video_note.file_id, message.video_note.duration, message.video_note.length, message.video_note.file_size)
            logger.info('Видеозапись: ' + str(message.video_note.file_id) + ' ' + str(message.video_note.duration) + ' ' + str(message.video_note.length) + ' ' + str(message.video_note.file_size))
            await message.answer('Извините, меня пока не научили работать с видеозаписью...')
        if message.video != None:
            print(message.video.file_id, message.video.mime_type, message.video.duration, message.video.width, message.video.height, message.video.file_size)
            logger.info('Видео: ' + str(message.video.file_id) + ' ' + str(message.video.mime_type) + ' ' + str(message.video.duration) + ' ' + str(message.video.width) + ' ' + str(message.video.height) + ' ' + str(message.video.file_size))
            await message.answer('Извините, меня пока не научили работать с видео...')
        # print('\n', message)
    anti_flood[message.chat.id] = message.date

async def main() -> None:
    logging.basicConfig(filename='bot_log.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.error('Starting bot')

    # Парсинг файла конфигурации
    config = load_config('bot.ini')

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    # loop=nest_asyncio.apply()
    loop=None
    dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)

    # Регистрация хэндлеров
    # register_functions_common
    register_handlers_choice(dp)
    register_handlers_common(dp, config.tg_bot.admin_id, bot)
    
    dp.register_message_handler(any_text, content_types=[types.ContentType.ANY])

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    # Запуск бота
    # executor.start_polling(dp, skip_updates=True)
    # nest_asyncio.apply()
    asyncio.run(main())