import asyncio
import random
from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta

from config import *
from database import db

router = Router()

# Состояния FSM
class PomodoroStates(StatesGroup):
    waiting_for_task_name = State()
    waiting_for_custom_task = State()
    in_session = State()

# Команда /start с клавиатурой
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = """🎯 *Добро пожаловать в NoProk!*

Я помогу тебе победить прокрастинацию с помощью техники Pomodoro.

*Как это работает:*
1. Выбираешь задачу и время
2. Работаешь без отвлечений
3. Отдыхаешь 5 минут
4. Повторяешь цикл

*Используй кнопки ниже для управления:*"""
    
    await message.answer(
        welcome_text, 
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

# Обработка кнопки "🍅 Начать сессию"
@router.message(F.text == "🍅 Начать сессию")
async def start_session_button(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Проверяем активную сессию
    if db.get_session(user_id):
        await message.answer(
            "⚠️ У тебя уже есть активная сессия!\n\n"
            "Заверши ее или используй кнопки управления сессией.",
            reply_markup=get_session_keyboard()
        )
        return
    
    # Предлагаем выбрать тип задачи
    await message.answer(
        "🎯 *Выбери тип задачи:*",
        parse_mode="Markdown",
        reply_markup=get_task_type_keyboard()
    )

# Обработка кнопки "📊 Статистика"
@router.message(F.text == "📊 Статистика")
async def stats_button(message: types.Message):
    await message.answer(
        "📈 *Выбери тип статистики:*",
        parse_mode="Markdown",
        reply_markup=get_stats_keyboard()
    )

# Обработка кнопки "💡 Совет"
@router.message(F.text == "💡 Совет")
async def tips_button(message: types.Message):
    await message.answer(
        "💡 *Выбери категорию совета:*",
        parse_mode="Markdown", 
        reply_markup=get_tips_keyboard()
    )

# Обработка кнопки "❓ Помощь"
@router.message(F.text == "❓ Помощь")
async def help_button(message: types.Message):
    help_text = """*📚 Помощь по использованию бота*

*Основные функции:*
🍅 **Начать сессию** - начать работу по технике Pomodoro
📊 **Статистика** - посмотреть свою продуктивность
💡 **Совет** - получить полезный совет

*Во время сессии:*
⏸ **Пауза** - приостановить таймер
🛑 **Завершить** - досрочно закончить сессию
⏱ **Осталось времени** - узнать, сколько времени осталось
📝 **Сменить задачу** - изменить задачу во время сессии

*Техника Pomodoro:*
• 25 минут фокусированной работы
• 5 минут перерыва
• После 4 сессий - длинный перерыв (15-30 минут)

*Советы для эффективности:*
• Убери телефон подальше
• Закрой лишние вкладки в браузере
• Сообщи окружающим, что ты занят"""
    
    await message.answer(help_text, parse_mode="Markdown")

# Обработка кнопки "ℹ️ О проекте"
@router.message(F.text == "ℹ️ О проекте")
async def about_button(message: types.Message):
    about_text = """*🤖 О проекте NoProk*

Этот бот создан в рамках школьного индивидуального проекта для борьбы с прокрастинацией у старшеклассников.

*Цель проекта:*
Помочь учащимся эффективно управлять своим временем и повысить продуктивность с помощью цифровых инструментов.

*Технологии:*
• Python 3.11+
• Aiogram 3.x (Telegram Bot API)
• Асинхронное программирование
• JSON база данных

*Особенности:*
✅ Интуитивный интерфейс с кнопками
✅ Подробная статистика продуктивности
✅ Советы по тайм-менеджменту
✅ Система мотивации

*Автор:* Мерзлякова Валерия
*Цель проекта:* Исследовать эффективность цифровых инструментов в борьбе с прокрастинацией."""
    
    await message.answer(about_text, parse_mode="Markdown")

# Обработка инлайн-кнопок выбора типа задачи
@router.callback_query(F.data.startswith("task_"))
async def process_task_type(callback: types.CallbackQuery, state: FSMContext):
    task_type = callback.data.split("_")[1]
    
    task_names = {
        "study": "📚 Учебная сессия",
        "work": "💼 Работа над проектом", 
        "sport": "🏋️ Тренировка",
        "creative": "🎨 Творческая работа",
        "cleaning": "🧹 Уборка",
        "reading": "📖 Чтение"
    }
    
    task_name = task_names.get(task_type, "Работа")
    
    # Сохраняем выбранную задачу
    await state.update_data(task_name=task_name)
    
    # Предлагаем выбрать длительность
    await callback.message.edit_text(
        f"✅ Задача: *{task_name}*\n\n"
        f"⏱ *Выбери длительность сессии:*",
        parse_mode="Markdown",
        reply_markup=get_task_duration_keyboard()
    )
    
    await callback.answer()

# Обработка кнопки "✏️ Своя задача"
@router.callback_query(F.data == "custom_task")
async def process_custom_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ *Введи название своей задачи:*\n\n"
        "Например: 'Подготовка к контрольной по математике', 'Написание сочинения'",
        parse_mode="Markdown"
    )
    
    await state.set_state(PomodoroStates.waiting_for_custom_task)
    await callback.answer()

# Обработка ввода своей задачи
@router.message(PomodoroStates.waiting_for_custom_task)
async def process_custom_task_name(message: types.Message, state: FSMContext):
    task_name = message.text
    
    if len(task_name) > 100:
        await message.answer("Слишком длинное название. Попробуй короче (до 100 символов).")
        return
    
    await state.update_data(task_name=task_name)
    
    await message.answer(
        f"✅ Задача: *{task_name}*\n\n"
        f"⏱ *Выбери длительность сессии:*",
        parse_mode="Markdown",
        reply_markup=get_task_duration_keyboard()
    )
    
    await state.clear()

# Обработка выбора длительности сессии
@router.callback_query(F.data.startswith("duration_"))
async def process_duration(callback: types.CallbackQuery, state: FSMContext):
    duration = int(callback.data.split("_")[1])
    
    # Получаем сохраненную задачу
    state_data = await state.get_data()
    task_name = state_data.get("task_name", "Работа")
    
    # Запускаем сессию
    user_id = callback.from_user.id
    session_id = db.start_session(user_id, task_name, duration * 60)
    
    # Отправляем сообщение о начале сессии
    await callback.message.edit_text(
        f"🍅 *Сессия началась!*\n\n"
        f"*Задача:* {task_name}\n"
        f"*Время:* {duration} минут\n"
        f"*Старт:* {datetime.now().strftime('%H:%M')}\n\n"
        f"💪 Сосредоточься на задаче!\n"
        f"Я напомню об окончании сессии.",
        parse_mode="Markdown"
    )
    
    # Запускаем таймер
    asyncio.create_task(run_timer(user_id, callback.message.chat.id, duration, task_name))
    
    await callback.answer(f"Сессия началась! {duration} минут фокуса.")

# Обработка отмены
@router.callback_query(F.data == "cancel")
async def process_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Действие отменено.")
    await state.clear()
    await callback.answer()

# Функция таймера
async def run_timer(user_id: int, chat_id: int, duration: int, task_name: str):
    from aiogram import Bot
    from config import BOT_TOKEN
    
    bot = Bot(token=BOT_TOKEN)
    total_seconds = duration * 60
    
    try:
        while total_seconds > 0:
            # Проверяем, активна ли еще сессия
            if not db.get_session(user_id):
                break
            
            # Обновляем каждые 30 секунд
            if total_seconds % 30 == 0:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f"⏱ *Осталось времени:* {minutes:02d}:{seconds:02d}\n"
                             f"Задача: {task_name}",
                        parse_mode="Markdown"
                    )
                except:
                    pass
            
            await asyncio.sleep(1)
            total_seconds -= 1
        
        # Завершаем сессию
        actual_duration = db.end_session(user_id)
        
        if actual_duration:
            minutes = actual_duration // 60
            
            await bot.send_message(
                chat_id=chat_id,
                text=f"✅ *Сессия завершена!*\n\n"
                     f"*Задача:* {task_name}\n"
                     f"*Время работы:* {minutes} минут\n"
                     f"*Завершено:* {datetime.now().strftime('%H:%M')}\n\n"
                     f"🏖️ *Время перерыва!*\n"
                     f"Отдохни 5 минут, затем начни новую сессию.",
                parse_mode="Markdown",
                reply_markup=get_main_keyboard()
            )
            
    except Exception as e:
        print(f"Ошибка таймера: {e}")
    finally:
        await bot.close()

# Обработка статистики
@router.callback_query(F.data.startswith("stats_"))
async def process_stats(callback: types.CallbackQuery):
    stat_type = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    stats = db.get_user_stats(user_id)
    
    if stat_type == "today":
        text = f"📊 *Статистика за сегодня*\n\n"
        text += f"🍅 Сессий: {stats['today_sessions']}\n"
        text += f"⏱ Время: {stats['today_time'] // 60} минут\n"
        text += f"🎯 Цель: 4 сессии в день\n"
        
        if stats['today_sessions'] >= 4:
            text += "\n✅ Отличный результат! Ты выполнил дневную норму!"
        elif stats['today_sessions'] > 0:
            text += f"\n💪 Осталось до цели: {4 - stats['today_sessions']} сессий"
        else:
            text += "\n🎯 Начни первую сессию прямо сейчас!"
    
    elif stat_type == "week":
        text = f"📊 *Статистика за неделю*\n\n"
        text += f"🍅 Всего сессий: {stats['total_sessions']}\n"
        text += f"⏱ Общее время: {stats['total_time'] // 3600} ч {stats['total_time'] % 3600 // 60} мин\n"
        text += f"🎯 Любимая задача: {stats['favorite_task'] or 'Нет данных'}\n"
        text += f"🕐 Последняя активность: {stats['last_active'][:16] if stats['last_active'] != 'Никогда' else 'Никогда'}"
    
    elif stat_type == "all":
        global_stats = db.get_global_stats()
        text = f"🏆 *Общая статистика*\n\n"
        text += f"👥 Всего пользователей: {global_stats['total_users']}\n"
        text += f"🍅 Всего сессий: {global_stats['total_sessions']}\n"
        text += f"⏱ Всего часов фокуса: {global_stats['total_time_hours']:.1f}\n"
        text += f"🔥 Активных сегодня: {global_stats['active_today']}"
    
    elif stat_type == "rating":
        leaderboard = db.get_leaderboard(10)
        text = "👑 *Топ-10 по продуктивности*\n\n"
        
        for i, user in enumerate(leaderboard, 1):
            hours = user['total_time'] // 3600
            minutes = (user['total_time'] % 3600) // 60
            
            if str(user_id) == user['user_id']:
                text += f"*{i}. Ты* - {hours}ч {minutes}мин ({user['total_sessions']} сессий)\n"
            else:
                text += f"{i}. Участник {user['user_id'][:4]}... - {hours}ч {minutes}мин\n"
        
        if not leaderboard:
            text += "Пока нет данных. Будь первым!"
    
    else:
        text = "📤 *Экспорт статистики*\n\n"
        text += "Эта функция в разработке. Скоро ты сможешь экспортировать статистику в CSV или PDF!"
    
    await callback.message.edit_text(text, parse_mode="Markdown")
    await callback.answer()

# Обработка советов
@router.callback_query(F.data.startswith("tip_"))
async def process_tips(callback: types.CallbackQuery):
    tip_type = callback.data.split("_")[1]
    
    tips_by_category = {
        "focus": [
            "🎯 *Техника 'Помидора':* Работай 25 минут, отдыхай 5. После 4 циклов — длинный перерыв.",
            "🎯 *Правило 2 минут:* Если задача занимает меньше 2 минут — сделай ее сразу.",
            "🎯 *Метод 'Съешь лягушку':* Начни день с самой неприятной задачи.",
            "🎯 *Техника 'Временных блоков':* Планируй день по 30-минутным блокам."
        ],
        "time": [
            "⏰ *Матрица Эйзенхауэра:* Раздели задачи на: срочные/важные, несрочные/важные и т.д.",
            "⏰ *Правило 52/17:* Работай 52 минуты, отдыхай 17. Исследования показывают максимальную эффективность.",
            "⏰ *Метод '90 минут':* Человек может максимально концентрироваться 90 минут, затем нужен перерыв.",
            "⏰ *Техника 'Альп':* Планируй задачи на день с учетом приоритетов и времени."
        ],
        "mental": [
            "🧘 *Медитация осознанности:* 10 минут в день улучшают концентрацию на 20%.",
            "🧘 *Техника '5-4-3-2-1':* Для борьбы с тревогой: найди 5 вещей, которые видишь, 4 — которые чувствуешь и т.д.",
            "🧘 *Дневник благодарности:* Каждый день записывай 3 вещи, за которые благодарен.",
            "🧘 *Дыхание 4-7-8:* Вдох на 4, задержка на 7, выдох на 8. Успокаивает нервную систему."
        ],
        "health": [
            "🍎 *Правило 20-20-20:* Каждые 20 минут смотри на объект в 20 футах (6 метрах) в течение 20 секунд.",
            "🍎 *Вода и продуктивность:* Обезвоживание на 2% снижает концентрацию на 10%. Пей воду!",
            "🍎 *Сон и память:* Каждый час недосыпа снижает IQ на 1 пункт. Спи 7-9 часов.",
            "🍎 *Физическая активность:* 30 минут упражнений в день улучшают когнитивные функции на 15%."
        ],
        "tools": [
            "🔧 *Используй блокаторы сайтов:* Freedom, Cold Turkey для блокировки отвлекающих сайтов.",
            "🔧 *Приложения для фокуса:* Forest, Focus To-Do, Be Focused помогут с таймерами.",
            "🔧 *Шум для концентрации:* Белый шум, звуки дождя или coffitivity.com улучшают фокус.",
            "🔧 *Метод 'Помодоро':* Используй наш бота для регулярных сессий фокуса!"
        ]
    }
    
    if tip_type == "random":
        all_tips = []
        for category_tips in tips_by_category.values():
            all_tips.extend(category_tips)
        tip = random.choice(all_tips)
    else:
        tips = tips_by_category.get(tip_type, ["💡 Хороший совет — начать прямо сейчас!"])
        tip = random.choice(tips)
    
    await callback.message.edit_text(tip, parse_mode="Markdown")
    await callback.answer()

# Обработка команд управления сессией
@router.message(F.text == "⏸ Пауза")
async def pause_session(message: types.Message):
    user_id = message.from_user.id
    session = db.get_session(user_id)
    
    if not session:
        await message.answer("У тебя нет активной сессии.")
        return
    
    if session.get("paused"):
        await message.answer("Сессия уже на паузе.")
    else:
        session["paused"] = True
        session["paused_at"] = datetime.now().isoformat()
        await message.answer("⏸ Сессия поставлена на паузу. Используй кнопки для продолжения.")

@router.message(F.text == "🛑 Завершить")
async def stop_session(message: types.Message):
    user_id = message.from_user.id
    
    if not db.get_session(user_id):
        await message.answer("У тебя нет активной сессии.")
        return
    
    actual_duration = db.end_session(user_id)
    minutes = actual_duration // 60 if actual_duration else 0
    
    await message.answer(
        f"🛑 *Сессия завершена досрочно*\n\n"
        f"Ты проработал: *{minutes} минут*\n\n"
        f"Хорошая попытка! Начни новую сессию, когда будешь готов.",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "⏱ Осталось времени")
async def time_left(message: types.Message):
    user_id = message.from_user.id
    session = db.get_session(user_id)
    
    if not session:
        await message.answer("У тебя нет активной сессии.")
        return
    
    start_time = datetime.fromisoformat(session["start_time"])
    elapsed = (datetime.now() - start_time).seconds - session.get("paused_time", 0)
    remaining = session["duration"] - elapsed
    
    if remaining > 0:
        minutes = remaining // 60
        seconds = remaining % 60
        await message.answer(f"⏱ *Осталось:* {minutes:02d}:{seconds:02d}", parse_mode="Markdown")
    else:
        await message.answer("⏰ Время сессии истекло! Заверши сессию.")

@router.message(F.text == "📝 Сменить задачу")
async def change_task(message: types.Message):
    await message.answer(
        "📝 *Введи новое название задачи:*",
        parse_mode="Markdown"
    )
    # Здесь можно добавить логику смены задачи

# Сохраняем поддержку старых команд
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await help_button(message)

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    await stats_button(message)