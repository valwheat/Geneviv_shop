import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.utils import executor

# 🔹 Укажи свой токен от BotFather
API_TOKEN = "7796901148:AAG813tStp-auy4Vteec5rVTICp5-JvRwH8"

# 🔹 ID твоего админского канала
ADMIN_CHANNEL_ID = -1002250580910

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# 🔹 Список товаров (можно добавлять новые)
PRODUCTS = {
    "buy_ring_elegance": {"name": "Кольцо 'Элегантность'", "price": 5000},
    "buy_ring_luxury": {"name": "Кольцо 'Роскошь'", "price": 7000},
}

# ✅ Команда /start - Открывает магазин
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    args = message.get_args()  # Получаем параметр после ?start=

    # 🔹 Если параметра нет – показываем кнопку "Открыть магазин"
    if not args:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        web_app_button = KeyboardButton(
            "🛍 Открыть магазин", web_app=WebAppInfo(url="https://genaviv.tilda.ws")
        )
        keyboard.add(web_app_button)

        await message.answer(
            "Добро пожаловать в магазин! Нажмите кнопку ниже, чтобы открыть каталог.",
            reply_markup=keyboard,
        )
        return

    # 🔹 Если параметр передан – это заказ товара
    if args in PRODUCTS:
        product = PRODUCTS[args]
        product_name = product["name"]
        price = product["price"]

        response_text = f"🛍 Вы выбрали: <b>{product_name}</b>\n💰 Цена: {price} ₽\n\nМы свяжемся с вами!"
        await message.answer(response_text, parse_mode="HTML")

        # 🔹 Отправляем заказ в админский канал
        admin_text = (
            f"📢 <b>Новый заказ!</b>\n"
            f"👤 Клиент: <b>{message.from_user.full_name}</b>\n"
            f"🛍 Товар: <b>{product_name}</b>\n"
            f"💰 Цена: {price} ₽"
        )
        await bot.send_message(ADMIN_CHANNEL_ID, admin_text, parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
