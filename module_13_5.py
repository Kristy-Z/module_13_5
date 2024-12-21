from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb.row(button1, button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)

    await message.answer('Введите свой рост:')
    await UserState.next()


@dp.message_handler(state=UserState.growth)
async def set_growth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['growth'] = float(message.text)

    await message.answer('Введите ваш вес:')
    await UserState.next()


@dp.message_handler(state=UserState.weight)
async def set_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = float(message.text)

    user_data = await state.get_data()
    age = user_data['age']
    growth = user_data['growth']
    weight = user_data['weight']

    bmr = 10 * weight + 6.25 * growth - 5 * age - 161
    tdee = bmr * 1.55

    await message.answer(f'Ваша норма калорий {int(tdee)} ')
    await state.finish()

@dp.message_handler(text=['/start'])
async def all_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью!", reply_markup = kb)

@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
