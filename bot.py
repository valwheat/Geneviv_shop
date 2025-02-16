import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # ID админа, можно взять из переменных окружения

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

# Обработчик данных из Web App
@dp.message(lambda message: message.web_app_data)
async def web_app_handler(message: types.Message):
    order_info = message.web_app_data.data  # Получаем данные заказа
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Отправляем пользователю подтверждение заказа
    await message.answer(f"Спасибо, {user_name}! Ваш заказ принят! 🎉")

    # Отправляем админу информацию о заказе
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"🛍 Новый заказ от {user_name} (ID: {user_id}):\n{order_info}")

async def main():
    """Основная функция запуска бота."""
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
