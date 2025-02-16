import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import WebAppData

# Загружаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHANNEL_ID = os.getenv("ADMIN_CHANNEL_ID")  # ID админского канала

# Проверка наличия переменных окружения
if not BOT_TOKEN:
    raise ValueError("Ошибка: Не найден BOT_TOKEN! Добавь его в переменные окружения.")

if not ADMIN_CHANNEL_ID:
    raise ValueError("Ошибка: Не найден ADMIN_CHANNEL_ID! Добавь его в переменные окружения.")

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Открыть магазин", web_app=types.WebAppInfo(url="https://genaviv.tilda.ws/")))
    
    await message.answer(
        "Добро пожаловать в магазин ювелирных украшений! 🛍\n"
        "Выберите товар и оформите заказ прямо в Telegram.",
        reply_markup=keyboard
    )

# Обработчик данных из Web App
@dp.message()
async def web_app_data_handler(message: Message):
    if message.web_app_data:
        try:
            data = message.web_app_data.data  # JSON-данные от Web App
            await bot.send_message(
                ADMIN_CHANNEL_ID,
                f"📦 Новый заказ!\n\n"
                f"🛍 Товар: {data}"
            )
            await message.answer("✅ Заказ отправлен! Мы скоро свяжемся с вами. 😊")
        except Exception as e:
            logging.error(f"Ошибка обработки WebAppData: {e}")
            await message.answer("❌ Ошибка при обработке заказа. Попробуйте ещё раз.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
