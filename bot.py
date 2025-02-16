import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Ошибка: Не найден BOT_TOKEN! Добавь его в переменные окружения.")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message()
async def start_handler(message: Message):
    if message.text == "/start":
        await message.answer("Привет! Добро пожаловать в магазин.")

# Обработчик данных из WebApp (нажатие кнопки "Купить" на сайте)
@dp.message()
async def web_app_data_handler(message: Message):
    if message.web_app_data:
        await message.answer("Спасибо за заказ! Мы скоро с вами свяжемся.")

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
