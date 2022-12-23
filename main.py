from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5922591176:AAHLkNGDTRhJbsog9VeQOskNCVfDKSh6dpY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class ApplyOperation(StatesGroup):
    choosing_first_number = State()
    choosing_second_number = State()


@dp.message_handler(commands=["multiply", "add", "subtract", "divide", "raise_to_power"])
async def cmd_food(message: types.Message, state: FSMContext):
    await state.update_data(operation=message.text)
    await message.answer(
        text="Введите первое числo:",
    )
    # Устанавливаем пользователю состояние "выбирает первое число"
    await ApplyOperation.choosing_first_number.set()

@dp.message_handler(state=ApplyOperation.choosing_first_number, regexp='[0-9]+')
async def first_number_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_number=message.text)
    await message.answer(
        text="Введите второе число:",
    )
    await ApplyOperation.next()

@dp.message_handler(state=ApplyOperation.choosing_first_number)
async def first_number_chosen(message: types.Message, state: FSMContext):
    await message.answer(
        text="Введите первое число:",
    )


@dp.message_handler(state=ApplyOperation.choosing_second_number, regexp='[0-9]+')
async def second_number_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if (user_data['operation'] == '/add'):
        await message.answer(
            text=f"Результат: {float(user_data['chosen_number']) + float(message.text)}\n"
        )
    if (user_data['operation'] == '/subtract'):
        await message.answer(
            text=f"Результат: {float(user_data['chosen_number']) - float(message.text)}\n"
        )
    if (user_data['operation'] == '/multiply'):
        await message.answer(
            text=f"Результат: {float(user_data['chosen_number']) * float(message.text)}\n"
        )
    if (user_data['operation'] == '/divide'):
        await message.answer(
            text=f"Результат: {float(user_data['chosen_number']) / float(message.text)}\n"
        )
    if (user_data['operation'] == '/raise_to_power'):
        await message.answer(
            text=f"Результат: {float(user_data['chosen_number']) ** float(message.text)}\n"
        )

    await state.set_state(None)

@dp.message_handler(state=ApplyOperation.choosing_second_number)
async def second_number_chosen(message: types.Message, state: FSMContext):
    await message.answer(
        text="Введите второе число:",
    )

@dp.message_handler()
async def url_command(message: types.Message):
   await message.answer('Выберите операцию:\n /multiply — умножить два числа\n /add — сложить два числа\n /subtract — вычесть из первого числа второе\n /divide — поделить первое число на второе\n /raise_to_power — возвести первое число в степень второго\n')

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
