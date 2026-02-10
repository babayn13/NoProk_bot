import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Токен из переменных окружения Railway
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN не найден в переменных окружения!")
    logger.error("Добавь BOT_TOKEN в настройки Railway")
    exit(1)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Клавиатура
def get_main_keyboard():
    keyboard = [
        [KeyboardButton(text="🍅 Начать сессию")],
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="💡 Совет")],
        [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О проекте")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Обработчики
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    logger.info(f"Получен /start от {message.from_user.id}")
    
    welcome_text = """🎯 *PROкрай - бот для борьбы с прокрастинацией*

🤖 *Развернут на Railway 24/7*
📊 *Автоматическое обновление из GitHub*
🚀 *Высокая доступность*

*Используй кнопки ниже:*"""
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

@dp.message(lambda message: message.text == "🍅 Начать сессию")
async def start_session(message: types.Message):
    await message.answer(
        "✅ *Сессия начата!*\n25 минут фокусированной работы.",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "📊 Статистика")
async def show_stats(message: types.Message):
    await message.answer(
        "📊 *Статистика системы:*\n"
        "🟢 Бот работает на Railway\n"
        "⏱ Время работы: 24/7\n"
        "🚀 Авторазвертывание: Да",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "💡 Совет")
async def send_tip(message: types.Message):
    await message.answer(
        "💡 *Совет от Railway:*\n"
        "Используй облачные платформы для 24/7 работы ботов!",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "❓ Помощь")
async def show_help(message: types.Message):
    await message.answer(
        "❓ *Помощь:*\nБот развернут на Railway.app\n"
        "Обновления автоматически из GitHub",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "ℹ️ О проекте")
async def about_project(message: types.Message):
    await message.answer(
        "ℹ️ *О проекте:*\n"
        "🤖 Бот развернут на Railway\n"
        "🎓 Школьный проект 10 класс\n"
        "🚀 Технологии: Python, Aiogram, Railway",
        parse_mode="Markdown"
    )

# Запуск бота
async def main():
    # Проверка подключения
    bot_info = await bot.get_me()
    logger.info(f"✅ Бот запущен: @{bot_info.username}")
    logger.info(f"🚀 Запущено на Railway")
    logger.info(f"⏱ Время: {__import__('datetime').datetime.now()}")
    
    # Сбрасываем вебхуки
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("=" * 50)
    print("🚂 PROкрай Бот на Railway")
    print("=" * 50)
    print(f"Python: {__import__('sys').version}")
    print(f"Токен: {BOT_TOKEN[:15]}...")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка: {e}")