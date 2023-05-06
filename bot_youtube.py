from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pytube import YouTube
from dotenv import load_dotenv
import os, logging

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

buttons = [
    KeyboardButton('/video'),
    KeyboardButton('/audio')
]
keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}!\nЯ вам помогу скачать видео и аудио", reply_markup=keyboard_one)

class VideoState(StatesGroup):
    download = State()

@dp.message_handler(commands='video')
async def get_url_video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и я вам его скачаю в mp4 формате")
    await VideoState.download.set()

@dp.message_handler(state=VideoState.download)
async def download_video(message:types.Message, state:FSMContext):
    if message.text == "Geeks":
        await message.answer("Go")
    else:
        await message.answer("Я вас понял")
    await state.finish()

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp, skip_updates=True)