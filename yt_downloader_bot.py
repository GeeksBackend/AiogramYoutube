from dotenv import load_dotenv
import os, logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from function import is_youtube_link, resolutions, download_video, download_audio, MAX_SIZE

load_dotenv('.env')
bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

buttons1 = [KeyboardButton('/video'), KeyboardButton('/audio')]
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons1)

buttons2 = [KeyboardButton('/cancel')]
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons2)

buttons4 = [KeyboardButton('/yes'), KeyboardButton('/no')]
keyboard4 = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons4)


class States_for_video(StatesGroup):
    video_link = State()
    res = State()
    quality = State()


class States_for_audio(StatesGroup):
    audio_link = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}! '
                         f'Я помогу вам скачать видео или аудио с YouTube.'
                         , reply_markup=keyboard1)


@dp.message_handler(commands=['video'], state=None)
async def video(message: types.Message):
    await States_for_video.video_link.set()
    await message.reply(f'Отправьте ссылку на видео, которое хотите скачать',
                        reply_markup=keyboard2)


@dp.message_handler(text=['/cancel'], state=States_for_video.all_states)
async def video_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f'Операция отменена.', reply_markup=keyboard1)


@dp.message_handler(text=['/no'], state=States_for_video.all_states)
async def video_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f'Операция отменена.', reply_markup=keyboard1)


@dp.message_handler(content_types=['text'], state=States_for_video.video_link)
async def video_set_link(message: types.Message, state: FSMContext):
    if is_youtube_link(message.text):
        await state.update_data(video_link=message.text)
        await message.answer('Секундочку...', reply_markup=types.ReplyKeyboardRemove())
        buttons3 = []
        await state.update_data(res=resolutions(message.text))
        res = await state.get_data()
        for i in res['res']:
            buttons3.append(i)
        buttons3.append('/cancel')
        keyboard3 = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons3)
        await message.answer("Выберите качество видео.", reply_markup=keyboard3)
        await States_for_video.quality.set()
    else:
        await message.reply(f'Похоже это не ссылка на YouTube, попробуйте ещё раз.', reply_markup=keyboard2)


@dp.message_handler(text=['/yes'], state=States_for_video.quality)
async def video_set_quality(message: types.Message, state: FSMContext):
    await message.answer('Скачиваем...', reply_markup=types.ReplyKeyboardRemove())
    res = await state.get_data()
    name = download_video(res['video_link'], res['quality'])
    if os.stat(name).st_size >= MAX_SIZE:
        os.remove(name)
        await state.finish()
        await message.answer('Похоже, этот файл слишком большой для телеграмм. '
                             'Попробуйте выбрать меньшее качество...', reply_markup=keyboard1)
    else:
        await bot.send_video(message.chat.id, open(name, 'rb'))
        await state.finish()
        os.remove(name)
        await message.answer('Скачивание завершено, хотите скачать ещё что-то?', reply_markup=keyboard1)


@dp.message_handler(content_types=['text'], state=States_for_video.quality)
async def video_set_quality(message: types.Message, state: FSMContext):
    res = await state.get_data()
    if message.text in res['res']:
        await state.update_data(quality=message.text)
        await message.answer('Качество выбрано, скачать видео?', reply_markup=keyboard4)
    else:
        await message.reply('Это не похоже на качество видео, поробуйте ещё раз...')


@dp.message_handler(commands=['audio'], state=None)
async def audio(message: types.Message):
    await States_for_audio.audio_link.set()
    await message.reply(f'Отправьте ссылку на аудио, которое хотите скачать',
                        reply_markup=keyboard2)


@dp.message_handler(text=['/cancel', '/no'], state=States_for_audio.all_states)
async def audio_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(f'Операция отменена.', reply_markup=keyboard1)


@dp.message_handler(text=['/yes'], state=States_for_audio.audio_link)
async def audio_download(message: types.Message, state: FSMContext):
    await message.answer('Скачиваем...', reply_markup=types.ReplyKeyboardRemove())
    res = await state.get_data()
    name = download_audio(res['audio_link'])
    if os.stat(name).st_size >= MAX_SIZE:
        os.remove(name)
        await state.finish()
        await message.answer('Похоже, этот файл слишком большой для телеграмм. '
                             'Попробуйте выбрать меньшее качество...', reply_markup=keyboard1)
    else:
        await bot.send_audio(message.chat.id, open(name, 'rb'))
        await state.finish()
        os.remove(name)
        await message.answer('Скачивание завершено, хотите скачать ещё что-то?', reply_markup=keyboard1)


@dp.message_handler(content_types=['text'], state=States_for_audio.audio_link)
async def audio_link(message: types.Message, state: FSMContext):
    if is_youtube_link(message.text):
        await state.update_data(audio_link=message.text)
        await message.answer('Ссылка определена, скачать аудио?', reply_markup=keyboard4)
    else:
        await message.reply(f'Похоже это не ссылка на YouTube, попробуйте ещё раз.', reply_markup=keyboard2)


executor.start_polling(dp)