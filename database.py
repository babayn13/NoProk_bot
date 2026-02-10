import json
import os
from datetime import datetime, date, timedelta
from collections import defaultdict

class SimpleDatabase:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = self._load_data()
        self.active_sessions = {}  # В памяти для быстрого доступа
    
    def _load_data(self):
        """Загрузить данные из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"users": {}, "daily_stats": {}}
        return {"users": {}, "daily_stats": {}}
    
    def _save_data(self):
        """Сохранить данные в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    # Методы для сессий
    def start_session(self, user_id: int, task_name: str, duration: int):
        """Начать новую сессию"""
        session_id = f"{user_id}_{datetime.now().timestamp()}"
        
        self.active_sessions[user_id] = {
            "id": session_id,
            "task": task_name,
            "duration": duration,
            "start_time": datetime.now().isoformat(),
            "paused": False,
            "paused_time": 0
        }
        
        return session_id
    
    def get_session(self, user_id: int):
        """Получить активную сессию пользователя"""
        return self.active_sessions.get(user_id)
    
    def end_session(self, user_id: int):
        """Завершить сессию и сохранить статистику"""
        session = self.active_sessions.pop(user_id, None)
        if not session:
            return None
        
        # Рассчитываем фактическое время
        start_time = datetime.fromisoformat(session["start_time"])
        actual_duration = (datetime.now() - start_time).seconds - session["paused_time"]
        
        # Сохраняем статистику
        self._save_session_stats(user_id, session, actual_duration)
        
        return actual_duration
    
    def _save_session_stats(self, user_id: int, session: dict, actual_duration: int):
        """Сохранить статистику сессии"""
        user_key = str(user_id)
        today = date.today().isoformat()
        
        # Инициализируем структуру данных
        if "users" not in self.data:
            self.data["users"] = {}
        if user_key not in self.data["users"]:
            self.data["users"][user_key] = {
                "total_sessions": 0,
                "total_time": 0,
                "last_active": None,
                "tasks": {}
            }
        
        # Обновляем статистику пользователя
        user_data = self.data["users"][user_key]
        user_data["total_sessions"] += 1
        user_data["total_time"] += actual_duration
        user_data["last_active"] = datetime.now().isoformat()
        
        # Статистика по задачам
        task_name = session["task"]
        if task_name not in user_data["tasks"]:
            user_data["tasks"][task_name] = {"sessions": 0, "time": 0}
        user_data["tasks"][task_name]["sessions"] += 1
        user_data["tasks"][task_name]["time"] += actual_duration
        
        # Ежедневная статистика
        if "daily_stats" not in self.data:
            self.data["daily_stats"] = {}
        if today not in self.data["daily_stats"]:
            self.data["daily_stats"][today] = {"sessions": 0, "time": 0, "users": set()}
        
        self.data["daily_stats"][today]["sessions"] += 1
        self.data["daily_stats"][today]["time"] += actual_duration
        self.data["daily_stats"][today]["users"].add(user_key)
        
        self._save_data()
    
    # Методы для статистики
    def get_user_stats(self, user_id: int, period: str = "today"):
        """Получить статистику пользователя за период"""
        user_key = str(user_id)
        user_data = self.data["users"].get(user_key, {})
        
        stats = {
            "total_sessions": user_data.get("total_sessions", 0),
            "total_time": user_data.get("total_time", 0),
            "today_sessions": 0,
            "today_time": 0,
            "week_sessions": 0,
            "week_time": 0,
            "favorite_task": None,
            "last_active": user_data.get("last_active", "Никогда")
        }
        
        # Статистика за сегодня
        today = date.today().isoformat()
        if today in self.data.get("daily_stats", {}):
            daily = self.data["daily_stats"][today]
            if user_key in daily["users"]:
                # Здесь нужно более сложное вычисление для конкретного пользователя
                # Для простоты считаем пропорционально
                stats["today_sessions"] = len([u for u in daily["users"] if u == user_key])
                stats["today_time"] = daily["time"] / len(daily["users"]) if daily["users"] else 0
        
        # Любимая задача
        if user_data.get("tasks"):
            favorite = max(user_data["tasks"].items(), key=lambda x: x[1]["time"])
            stats["favorite_task"] = favorite[0]
        
        return stats
    
    def get_global_stats(self):
        """Получить глобальную статистику"""
        today = date.today().isoformat()
        
        return {
            "total_users": len(self.data.get("users", {})),
            "total_sessions": sum(u["total_sessions"] for u in self.data.get("users", {}).values()),
            "total_time_hours": sum(u["total_time"] for u in self.data.get("users", {}).values()) / 3600,
            "active_today": len(self.data.get("daily_stats", {}).get(today, {}).get("users", [])),
            "today_sessions": self.data.get("daily_stats", {}).get(today, {}).get("sessions", 0)
        }
    
    def get_leaderboard(self, limit: int = 10):
        """Получить таблицу лидеров"""
        users = []
        for user_id, data in self.data.get("users", {}).items():
            users.append({
                "user_id": user_id,
                "total_time": data.get("total_time", 0),
                "total_sessions": data.get("total_sessions", 0)
            })
        
        # Сортируем по общему времени
        users.sort(key=lambda x: x["total_time"], reverse=True)
        return users[:limit]

# Глобальный экземпляр
db = SimpleDatabase()