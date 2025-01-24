import asyncio
import json
import random

import websockets
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from settings import BOT_TOKEN, SUBSCRIBED_CHAT_ID


# Глобальные переменные
last_notified_price = None  # Цена последнего уведомления
current_price = None  # Текущая цена
subscribed_chat_id = SUBSCRIBED_CHAT_ID  # ID чата для уведомлений


async def on_message(websocket, bot):
    global last_notified_price, current_price
    async for message in websocket:
        data = json.loads(message)
        price_str = data.get("p")

        if not price_str:
            continue

        new_price = float(price_str)
        current_price = new_price  # Всегда обновляем текущую цену

        # Инициализация при первом запуске
        if last_notified_price is None:
            last_notified_price = new_price
            continue

        # Проверяем изменение цены относительно последнего уведомления
        price_diff = abs(new_price - last_notified_price)

        if price_diff >= 0.1 and subscribed_chat_id:
            direction = (
                "🟢 ВЗЛЕТЕЛА" if new_price > last_notified_price else "🔪 РУХНУЛА"
            )

            await bot.send_message(
                subscribed_chat_id,
                f"🚨 {direction} НА {price_diff:.2f}$!\n"
                f"👉 Текущая: ${new_price:.2f}\n"
                f"⏳ Предыдущий порог: ${last_notified_price:.2f}\n"
                f"#{'TO_THE_MOON' if direction == '🟢 ВЗЛЕТЕЛА' else 'DUMPSTER_FIRE'}",
            )

            last_notified_price = new_price


async def subscribe(bot):
    uri = "wss://fstream.binance.com/ws/trumpusdt@aggTrade"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(
                    json.dumps(
                        {
                            "method": "SUBSCRIBE",
                            "params": ["trumpusdt@aggTrade"],
                            "id": 1,
                        }
                    )
                )
                await on_message(websocket, bot)
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(5)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Команда /p - текущая цена
    @dp.message(Command("p"))
    async def price_cmd(message: Message):
        if current_price is not None:
            await message.answer(
                f"📊 Текущая цена TRUMP: ${current_price:.4f}\n"
                f"📈 Изменение от последнего уведомления: "
                f"{'🟢 +' if current_price >= last_notified_price else '🔴 '}"
                f"{(current_price - last_notified_price):.2f}$"
            )
        else:
            await message.answer("⏳ Данные о цене еще не получены...")

    await asyncio.gather(dp.start_polling(bot), subscribe(bot))


if __name__ == "__main__":
    asyncio.run(main())
