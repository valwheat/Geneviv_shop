import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Ошибка: Не найден BOT_TOKEN! Добавь его в переменные окружения.")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Create Web App button in chat
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Открыть магазин", web_app=WebAppInfo(url="https://genaviv.tilda.ws/"))]
    ],
    resize_keyboard=True
)

# Command /start
async def start_handler(message: types.Message):
    await message.answer(
        "Привет-привет! Лови приложение для просмотра каталога и оформления заказа в Genaviv. "
        "[Открыть магазин](https://t.me/Genaviv_Bot/Genaviv_Shop)",
        parse_mode="Markdown"
    )

# Handle incoming orders from Tilda
@dp.message(lambda message: "Order #" in message.text)
async def order_handler(message: types.Message):
    user_id = message.chat.id  # Get user ID
    await bot.send_message(user_id, "Спасибо за заказ! Мы скоро с вами свяжемся.")

async def main():
    """Main function to start the bot."""
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
