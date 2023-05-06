from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'go'])
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}! Вот мои комманды:\n/start - запустить бота")
    print(message)

@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.reply("Вот мои комманды:\n/start - запустить бота")

@dp.message_handler(text=['Привет', 'привет'])
async def hello(message:types.Message):
    await message.reply("Привет")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    await message.reply("Тест")
    await message.answer("Тест")
    await message.answer_location(40.51932423585271, 72.80303238627863)
    await message.answer_photo('https://thumb.tildacdn.com/tild6235-3762-4330-a463-623936356436/-/format/webp/_2.png')
    with open('photo.png', 'rb') as photo:
        await message.answer_photo(photo)
    with open('lesson_7.pdf', 'rb') as pdf:
        await message.answer_document(pdf)

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял введите /help")

executor.start_polling(dp)