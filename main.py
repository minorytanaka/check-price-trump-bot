import asyncio
import json
import websockets
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from settings import BOT_TOKEN


# Переменная для хранения последней полученной цены
last_price = None


# Функция для обработки сообщений WebSocket
async def on_message(websocket):
    global last_price
    async for message in websocket:
        data = json.loads(message)
        price = data.get("p")
        if price:
            last_price = price  # Обновляем последнюю цену


# Функция для подписки на WebSocket
async def subscribe():
    uri = "wss://fstream.binance.com/ws/trumpusdt@aggTrade"
    async with websockets.connect(uri) as websocket:
        # Подписка на стрим
        subscription_message = {
            "method": "SUBSCRIBE",
            "params": ["trumpusdt@aggTrade"],
            "id": 1,
        }
        await websocket.send(json.dumps(subscription_message))

        # Обработка сообщений
        await on_message(websocket)


# Функция бота для получения цены
async def send_price(message: Message):
    if last_price:
        msg = f"${last_price}"
    else:
        msg = "Price data is not available yet."
    await message.reply(msg)


# Основная асинхронная функция
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Обработчик команды /price
    @dp.message(Command("price"))
    async def handle_price(message: Message):
        await send_price(message)

    # Запуск бота в фоновом режиме
    asyncio.create_task(dp.start_polling(bot))

    # Подключение к WebSocket для получения цен
    await subscribe()


if __name__ == "__main__":
    asyncio.run(main())
