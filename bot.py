import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHANNEL_ID = os.getenv("ADMIN_CHANNEL_ID")

if not BOT_TOKEN:
    raise ValueError("Ошибка: Не найден BOT_TOKEN! Добавь его в переменные окружения.")
if not ADMIN_CHANNEL_ID:
    raise ValueError("Ошибка: Не найден ADMIN_CHANNEL_ID! Добавь его в переменные окружения.")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=["start"])
async def start_command(message: Message):
    await message.answer("Привет! Добро пожаловать в магазин.")

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def handle_web_app_data(message: Message):
    try:
        data = message.web_app_data.data
        await bot.send_message(ADMIN_CHANNEL_ID, f"🛍 Новый заказ: {data}")
        await message.answer("Спасибо за заказ! Мы скоро с вами свяжемся.")
    except Exception as e:
        logging.error(f"Ошибка обработки заказа: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
