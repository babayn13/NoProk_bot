import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

print("=" * 50)
print("🔍 ТЕСТИРОВАНИЕ ТОКЕНА БОТА")
print("=" * 50)

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не найден в .env файле")
    print("\nПроверь файл .env, он должен содержать:")
    print("BOT_TOKEN=твой_токен_здесь")
    exit(1)

print(f"Токен (первые 20 символов): {BOT_TOKEN[:20]}...")
print(f"Длина токена: {len(BOT_TOKEN)} символов")

if BOT_TOKEN == "ваш_токен_здесь" or BOT_TOKEN == "DEMO_TOKEN":
    print("❌ ОШИБКА: Ты используешь демо-токен!")
    print("Замени его на настоящий токен от @BotFather")
    exit(1)

if len(BOT_TOKEN) < 40:
    print("❌ ОШИБКА: Токен слишком короткий!")
    print("Настоящий токен должен быть ~50 символов")
    exit(1)

print("\n🔗 Пробуем подключиться к Telegram API...")

try:
    bot = Bot(token=BOT_TOKEN)
    
    # Получаем информацию о боте
    bot_info = bot.session.get(bot.session.api.base.make_request("getMe"))
    
    if bot_info and bot_info.get("ok"):
        username = bot_info["result"]["username"]
        first_name = bot_info["result"]["first_name"]
        
        print(f"✅ УСПЕХ! Бот найден!")
        print(f"👤 Имя бота: {first_name}")
        print(f"🔗 Username: @{username}")
        print(f"🆔 ID бота: {bot_info['result']['id']}")
        
        print("\n🎉 Токен работает правильно!")
        print("Теперь ты можешь:")
        print("1. Найти бота в Telegram по имени @{}".format(username))
        print("2. Запустить main.py: python main.py")
        print("3. Написать боту /start")
        
    else:
        print("❌ ОШИБКА: Не удалось получить информацию о боте")
        
except Exception as e:
    print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
    print("\nВозможные причины:")
    print("1. Неверный токен")
    print("2. Проблемы с интернет-соединением")
    print("3. Токен был отозван в @BotFather")

print("=" * 50)