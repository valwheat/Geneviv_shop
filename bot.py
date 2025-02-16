import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Ошибка: Не найден BOT_TOKEN! Добавь его в переменные окружения.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Добро пожаловать в магазин.")

# Обработчик входящих сообщений от Тильды
@dp.message(lambda message: "Order #" in message.text)
async def order_handler(message: types.Message):
    user_id = message.chat.id  # ID клиента, который оформил заказ
    await bot.send_message(user_id, "Спасибо за заказ! Мы скоро с вами свяжемся.")

async def main():
    """Основная функция запуска бота."""
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
