import asyncio
import logging
from aiogram import Dispatcher, Bot
from config import BOT_TOKEN
from handlers import router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    # Создаем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутер
    dp.include_router(router)
    
    # Запускаем бота
    logger.info("🤖 Бот NoProk запущен!")
    logger.info("🎯 Доступны инлайн-кнопки и клавиатуры")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    # Проверяем токен
    if BOT_TOKEN == "DEMO_TOKEN":
        print("⚠️ Замени BOT_TOKEN в файле .env на свой токен от @BotFather!")
        print("Формат: BOT_TOKEN=ваш_токен_здесь")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен")