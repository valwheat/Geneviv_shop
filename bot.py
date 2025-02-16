import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

# Включаем логирование (удобно для отладки)
logging.basicConfig(level=logging.INFO)

# Берём токен бота из переменных окружения (безопасно)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, есть ли токен
if not BOT_TOKEN:
    raise ValueError("Ошибка: Не найден BOT_TOKEN! Добавь его в переменные окружения.")

# Создаём экземпляр бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Добро пожаловать в магазин украшений. Выбирайте товары в нашем мини-приложении!")

# Обработчик входящих данных из WebApp (когда жмут кнопку "Купить")
@dp.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: Message):
    try:
        data = message.web_app_data.data
        await message.answer(f"🛍 Вы заказали: {data}\nМы свяжемся с вами для подтверждения заказа.")
        
        # Отправка заказа в админский канал (замени на свой ID)
        ADMIN_CHANNEL_ID = -1002250580910
        await bot.send_message(ADMIN_CHANNEL_ID, f"Новый заказ:\n{data}")
    
    except Exception as e:
        logging.error(f"Ошибка при обработке данных из WebApp: {e}")
        await message.answer("Произошла ошибка. Попробуйте ещё раз.")

# Основная асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
