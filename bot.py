from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ContentType
from aiogram.types import ChatActions
from aiogram.utils.markdown import text

from config import TOKEN
from keyboard import keyboard
from parse_mal import get_response


HELP_MESSAGE = text(
    "Hi! I'm a bot that allows you to get information about top anime and recently released anime based on data on myanimelist.net.",
    "To get a keyboard with a list of commands, type the command /start.",
    "Information about available commands:",
    "1) /top_anime_series - sends top 10 anime series",
    "2) /top_anime_movies - sends top 10 anime movies",
    "3) /top_OVA's - sends top 10 OVA's",
    "4) /top_ONA's - sends top 10 ONA's",
    "5) /random_new_anime_list - sends 10 random seasonal anime",
    sep='\n'
)

ERROR_MESSAGE = text(
    "Sorry, but I don't understand.",
    "To get information about my abilities please send /help comand.",
    sep='\n'
)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await message.reply(HELP_MESSAGE, reply=False)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('The keyboard has been set up', reply_markup=keyboard, reply=False)


@dp.message_handler(commands=['top_anime_series'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.TYPING)
    await message.reply(get_response(1), reply=False, parse_mode="HTML")


@dp.message_handler(commands=['top_anime_movies'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.TYPING)
    await message.reply(get_response(2), reply=False, parse_mode="HTML")


@dp.message_handler(commands=["top_OVA's"])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.TYPING)
    await message.reply(get_response(3), reply=False, parse_mode="HTML")


@dp.message_handler(commands=["top_ONA's"])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.TYPING)
    await message.reply(get_response(4), reply=False, parse_mode="HTML")
    

@dp.message_handler(commands=["random_new_anime_list"])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.TYPING)
    await message.reply(get_response(5), reply=False, parse_mode="HTML")


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    await msg.reply(ERROR_MESSAGE)


if __name__ == '__main__':
    executor.start_polling(dp)
    