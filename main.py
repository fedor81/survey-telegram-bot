import os
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv


async def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не задан")

    # Поддержка двух форматов: JSON-массив или строка через запятую
    chats_raw = os.getenv("CHAT_IDS", "")
    if not chats_raw:
        raise ValueError("CHAT_IDS не задан")

    if chats_raw.strip().startswith("["):
        chat_ids = json.loads(chats_raw)
    else:
        chat_ids = [c.strip() for c in chats_raw.split(",") if c.strip()]

    question = os.getenv("POLL_QUESTION", "Кто сегодня придет?")
    options_raw = os.getenv("POLL_OPTIONS", '["да", "нет"]')
    try:
        options = json.loads(options_raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Невалидный JSON в POLL_OPTIONS: {e}")

    async with Bot(token=token) as bot:
        for chat_id in chat_ids:
            try:
                await bot.send_poll(
                    chat_id=chat_id,
                    question=question,
                    options=options,
                    is_anonymous=False,  # видно, кто проголосовал
                    open_period=86400,  # 24 часа
                )
                print(f"✅ Успешно отправлено в {chat_id}")
            except TelegramError as e:
                print(f"⚠️ Ошибка в чате: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        raise SystemExit(1)
