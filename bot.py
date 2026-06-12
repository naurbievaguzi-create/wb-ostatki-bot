import requests
import telegram
import asyncio

BOT_TOKEN = "СЮДА_ТОКЕН_БОТА"
WB_TOKEN = "СЮДА_API_WB"
CHAT_ID = "-5576132963"

bot = telegram.Bot(token=BOT_TOKEN)

def get_stocks():
    headers = {
        "Authorization": WB_TOKEN
    }

    url = "https://statistics-api.wildberries.ru/api/v1/supplier/stocks?dateFrom=2025-01-01"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Ошибка WB: {response.status_code}"

    data = response.json()

    message = "📦 Остатки WB\n\n"

    low_stock = []

    for item in data[:50]:
        qty = item.get("quantity", 0)
        nm_id = item.get("nmId")

        message += f"Артикул {nm_id}: {qty} шт.\n"

        if qty < 10:
            low_stock.append(f"⚠️ {nm_id}: {qty} шт.")

    if low_stock:
        message += "\n\nЗаканчиваются:\n"
        message += "\n".join(low_stock)

    return message


async def send_report():
    text = get_stocks()
    await bot.send_message(chat_id=CHAT_ID, text=text)


asyncio.run(send_report())
