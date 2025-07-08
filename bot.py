import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
import pandas as pd

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кошерный прайс-лист")],
        [KeyboardButton(text="Ответы на вопросы")],
        [KeyboardButton(text="Связь с менеджером")],
        [KeyboardButton(text="Предложения")],
        [KeyboardButton(text="Сайт AST")],
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать!\n"
        "Выберите, что вас интересует 👇",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "Кошерный прайс-лист")
async def send_price_list(message: types.Message):
    await message.answer_document(open("c 1.02 прайс лист 35.xlsx", "rb"))

@dp.message(lambda message: message.text == "Ответы на вопросы")
async def send_answers(message: types.Message):
    text = (
        "📦 *В каких пределах действует доставка?*\n"
        "Доставка действует в Москве и в МО.\n\n"
        "💸 *Сколько стоит доставка?*\n"
        "Доставка бесплатная.\n\n"
        "📅 *Детали заказа?*\n"
        "Заказы на завтра принимаем до 16:00. Доставка возможна в любой другой день, кроме субботы и воскресенья. В день доставки вам позвонит водитель и сообщит примерное время (вы можете договориться, если оно неудобно).\n\n"
        "💰 *Как оплачивать?*\n"
        "Оплата строго наличными в руки водителю (лучше без сдачи)."
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(lambda message: message.text == "Связь с менеджером")
async def contact_manager(message: types.Message):
    await message.answer("Связаться с менеджером: 8-925-178-77-09")

@dp.message(lambda message: message.text == "Предложения")
async def handle_proposals(message: types.Message):
    await message.answer("Пишите свои предложения, чего вы еще хотели бы видеть в боте, какой ассортимент добавить?")

@dp.message(lambda message: message.text == "Сайт AST")
async def send_site(message: types.Message):
    await message.answer("Тут вы можете посмотреть дополнительные данные о товаре с картинками:\nhttps://www.ast-inter.ru/")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
