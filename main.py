import aiohttp
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from settings import API_TOKEN, BOT_TOKEN


async def get_trump_info():
    """
    Асинхронная функция для получения информации о цене TRUMP.
    """

    headers = {"X-CMC_PRO_API_KEY": API_TOKEN}
    params = {"id": 35336, "convert": "USD"}
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            response.raise_for_status()  # Проверка на ошибки
            data = await response.json()  # Асинхронно получаем JSON-ответ
            price = data["data"]["35336"]["quote"]["USD"]["price"]
            last_updated = data["data"]["35336"]["quote"]["USD"]["last_updated"]
            return price, datetime.strptime(
                last_updated, "%Y-%m-%dT%H:%M:%S.%fZ"
            ).strftime("%H:%M:%S %d-%m-%Y")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("price"))
async def send_price(message: Message):
    try:
        price, last_updated = (
            await get_trump_info()
        )  # Используем await для асинхронного вызова
        msg = f"Price: ${price:.3f}\nLast updated: {last_updated}"
    except Exception as e:
        msg = f"Error: {e}"
    await message.reply(msg)


async def main():
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
