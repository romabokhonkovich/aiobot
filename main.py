from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from config import api_id, api_hash, phone_number, API_TOKEN
from commands import *
from other_functions import *
from aiogram import types, Dispatcher, Bot

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.register_message_handler(start_command_handler, commands=['start'])
dp.register_message_handler(help_command_handler, commands=['mute', 'unmute'])
dp.register_message_handler(joke_command_handler, commands=['joke'])
dp.register_message_handler(summer_command_handler, commands=['summer'])
dp.register_message_handler(weather_command_handler, commands=['weather'])
dp.register_message_handler(image_command_handler, commands=['image'])
dp.register_message_handler(help_command_handler, commands=['help'])
dp.register_message_handler(currency_command_handler, commands=['currency'])
dp.register_message_handler(delete_join_messages, content_types=[types.ContentType.NEW_CHAT_MEMBERS,types.ContentType.LEFT_CHAT_MEMBER])
dp.register_message_handler(filter_messages)


async def default_commands(dp):
    await bot.set_my_commands(commands = [types.BotCommand(command="/start", description="Начать диалог"),
                types.BotCommand(command="/help", description="Показать справку"),
                types.BotCommand(command="/weather", description="Погода в Жабинке"),
                types.BotCommand(command="/currency", description="Курсы валют"),
                types.BotCommand(command="/summer", description="Дни до лета"),
                types.BotCommand(command="/image", description="Три рандомные фото"),
                types.BotCommand(command="/joke", description="Шутка"), ])


# Запустите бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup= default_commands)
