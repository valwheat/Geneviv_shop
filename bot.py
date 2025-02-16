import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
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

# ✅ Properly Register the Start Command
async def start_handler(message: types.Message):
    await message.answer(
        "Привет-привет! Лови приложение для просмотра каталога и оформления заказа в Genaviv.\n"
        "[Открыть магазин](https://t.me/Genaviv_Bot/Genaviv_Shop)",
        parse_mode="MarkdownV2",
        reply_markup=main_keyboard
    )

dp.message.register(start_handler, Command("start"))  # ✅ Correct way to register handlers in aiogram v3

# ✅ Handle incoming orders from Tilda
async def order_handler(message: types.Message):
    if "Order #" in message.text:
        user_id = message.chat.id  # Get user ID
        await bot.send_message(user_id, "Спасибо за заказ! Мы скоро с вами свяжемся.")

dp.message.register(order_handler)  # ✅ Properly register the order handler

# ✅ Handle unknown messages (Optional)
async def unknown_message(message: types.Message):
    await message.answer("Я не понимаю это сообщение. Используйте команду /start.")

dp.message.register(unknown_message)  # ✅ Catch all other messages

# ✅ Fix Async Main Function
async def main():
    """Main function to start the bot."""
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
