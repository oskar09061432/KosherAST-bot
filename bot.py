
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import pandas as pd
from datetime import datetime
import os

API_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("📦 Кошерный прайс-лист"))
keyboard.add(KeyboardButton("❓ Ответы на вопросы"))
keyboard.add(KeyboardButton("📞 Связь с менеджером"))
keyboard.add(KeyboardButton("💬 Предложения"))
keyboard.add(KeyboardButton("🌐 Сайт AST"))

# Путь к файлам
PRICE_PATH = "c 1.02 прайс лист 35.xlsx"
LOG_PATH = "bot_logs.xlsx"
SUGGESTIONS_PATH = "предложения.xlsx"

def log_user(user_id, username, full_name, action):
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    df = pd.DataFrame([[time, user_id, username, full_name, action]],
                      columns=["Время", "ID", "Username", "Имя", "Действие"])
    if os.path.exists(LOG_PATH):
        df.to_excel(LOG_PATH, index=False, header=False, startrow=len(pd.read_excel(LOG_PATH)))
    else:
        df.to_excel(LOG_PATH, index=False)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    log_user(message.from_user.id, message.from_user.username, message.from_user.full_name, "start")
    await message.answer(
        "Добро пожаловать!"
"
        "Мы предлагаем кошерный алкоголь для частных мероприятий.
"
        "Выберите, что вас интересует:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📦 Кошерный прайс-лист")
async def send_price(message: types.Message):
    log_user(message.from_user.id, message.from_user.username, message.from_user.full_name, "прайс-лист")
    await message.answer_document(types.InputFile(PRICE_PATH))

@dp.message_handler(lambda message: message.text == "❓ Ответы на вопросы")
async def send_answers(message: types.Message):
    log_user(message.from_user.id, message.from_user.username, message.from_user.full_name, "вопросы")
    text = (
        "🟦 В каких пределах действует доставка?
"
        "Доставка действует в Москве и в МО.

"
        "🟦 Сколько стоит доставка?
"
        "Доставка бесплатная.

"
        "🟦 Детали заказа?
"
        "Заказы на завтра принимаем до 16:00. Также доставка может быть запланирована на любой другой день, кроме субботы и воскресенья. "
        "В день доставки вам позвонит водитель и оповестит о примерном времени доставки (вы можете с ним договориться, если вам не подойдет время).

"
        "🟦 Как оплачивать?
"
        "Оплата строго наличными в руки водителю (лучше без сдачи)."
    )
    await message.answer(text)

@dp.message_handler(lambda message: message.text == "📞 Связь с менеджером")
async def contact(message: types.Message):
    log_user(message.from_user.id, message.from_user.username, message.from_user.full_name, "контакт")
    await message.answer("📞 Оскар
Тел: 8-925-178-77-09
Telegram: @oskar_0906")

@dp.message_handler(lambda message: message.text == "🌐 Сайт AST")
async def site(message: types.Message):
    log_user(message.from_user.id, message.from_user.username, message.from_user.full_name, "сайт AST")
    await message.answer("Тут вы можете посмотреть дополнительные данные о товаре с картинками:
https://www.ast-inter.ru/")

@dp.message_handler(lambda message: message.text == "💬 Предложения")
async def offer_request(message: types.Message):
    log_user(message.from_user.id, message.from_user.username, message.from_user.full_name, "вкладка предложения")
    await message.answer("Пишите свои предложения, чего вы еще хотели бы видеть в боте, какой ассортимент добавить:")

@dp.message_handler()
async def suggestions(message: types.Message):
    user = message.from_user
    log_user(user.id, user.username, user.full_name, f"предложение: {message.text}")
    df = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), user.id, user.username, user.full_name, message.text]],
                      columns=["Время", "ID", "Username", "Имя", "Предложение"])
    if os.path.exists(SUGGESTIONS_PATH):
        df.to_excel(SUGGESTIONS_PATH, index=False, header=False, startrow=len(pd.read_excel(SUGGESTIONS_PATH)))
    else:
        df.to_excel(SUGGESTIONS_PATH, index=False)
    await message.answer("Спасибо! Ваше предложение сохранено.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
