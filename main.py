import datetime
import re
import time
from geopy.geocoders import Nominatim
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions, ChatMemberUpdated, ChatActions
from aiogram.utils import executor
import random
from glob import glob
import os, shutil
from telethon.sync import TelegramClient
import asyncio
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.filters import Text
from config import api_id, api_hash, phone_number, API_TOKEN



# Создайте экземпляр бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)












# Запустите бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
