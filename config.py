import os
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Загружаем переменные из .env
load_dotenv()

# Получаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("⚠️ Внимание: BOT_TOKEN не найден в .env файле")
    BOT_TOKEN = "DEMO_TOKEN"

# Константы Pomodoro
WORK_TIME = 25 * 60  # 25 минут в секундах
BREAK_TIME = 5 * 60   # 5 минут в секундах

# Для демо-режима уменьшим время
DEMO_MODE = True
if DEMO_MODE:
    WORK_TIME = 30  # 30 секунд для теста
    BREAK_TIME = 10  # 10 секунд для теста

# Клавиатуры
def get_main_keyboard():
    """Основная клавиатура с главными кнопками"""
    keyboard = [
        [KeyboardButton(text="🍅 Начать сессию")],
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="💡 Совет")],
        [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О проекте")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_session_keyboard():
    """Клавиатура во время сессии"""
    keyboard = [
        [KeyboardButton(text="⏸ Пауза"), KeyboardButton(text="🛑 Завершить")],
        [KeyboardButton(text="⏱ Осталось времени"), KeyboardButton(text="📝 Сменить задачу")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_task_duration_keyboard():
    """Инлайн-клавиатура для выбора длительности сессии"""
    builder = InlineKeyboardBuilder()
    
    durations = [
        ("🍅 25 мин", "25"),
        ("⚡ 15 мин", "15"), 
        ("🐢 50 мин", "50"),
        ("🔥 90 мин", "90")
    ]
    
    for text, minutes in durations:
        builder.button(text=text, callback_data=f"duration_{minutes}")
    
    builder.button(text="❌ Отмена", callback_data="cancel")
    builder.adjust(2, 2, 1)
    return builder.as_markup()

def get_task_type_keyboard():
    """Инлайн-клавиатура для выбора типа задачи"""
    builder = InlineKeyboardBuilder()
    
    tasks = [
        ("📚 Учеба", "study"),
        ("💼 Работа", "work"),
        ("🏋️ Тренировка", "sport"),
        ("🎨 Творчество", "creative"),
        ("🧹 Уборка", "cleaning"),
        ("📖 Чтение", "reading")
    ]
    
    for text, task_type in tasks:
        builder.button(text=text, callback_data=f"task_{task_type}")
    
    builder.button(text="✏️ Своя задача", callback_data="custom_task")
    builder.button(text="❌ Отмена", callback_data="cancel")
    builder.adjust(2, 2, 2, 1, 1)
    return builder.as_markup()

def get_stats_keyboard():
    """Инлайн-клавиатура для статистики"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📈 За сегодня", callback_data="stats_today")
    builder.button(text="📊 За неделю", callback_data="stats_week")
    builder.button(text="🏆 За все время", callback_data="stats_all")
    builder.button(text="👑 Рейтинг", callback_data="stats_rating")
    builder.button(text="📤 Экспорт", callback_data="stats_export")
    
    builder.adjust(2, 2, 1)
    return builder.as_markup()

def get_tips_keyboard():
    """Инлайн-клавиатура для советов"""
    builder = InlineKeyboardBuilder()
    
    categories = [
        ("🎯 Фокус", "tip_focus"),
        ("⏰ Тайм-менеджмент", "tip_time"),
        ("🧘 Ментальное здоровье", "tip_mental"),
        ("🍎 Здоровье", "tip_health"),
        ("🔧 Инструменты", "tip_tools"),
        ("🎲 Случайный совет", "tip_random")
    ]
    
    for text, callback in categories:
        builder.button(text=text, callback_data=callback)
    
    builder.adjust(2, 2, 2)
    return builder.as_markup()