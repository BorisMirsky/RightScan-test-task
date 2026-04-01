import signal
import sys
import requests
from datetime import datetime, timedelta
from typing import List, Dict

# Отключаем прокси для localhost
session = requests.Session()
session.trust_env = False


def signal_handler(sig, frame):
    print("\n\nПрерывание мониторинга...")
    sys.exit(0)


class RobotMonitor:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", timeout_minutes: int = 10):
        self.base_url = base_url
        self.timeout_minutes = timeout_minutes
        self.session = session
    
    def get_all_tasks(self) -> List[Dict]:
        response = self.session.get(f"{self.base_url}/tasks", timeout=5)
        response.raise_for_status()
        return response.json()
    
    def is_task_stuck(self, task: Dict) -> bool:
        updated_at = datetime.fromisoformat(task["updated_at"])
        time_diff = datetime.now() - updated_at
        status = task.get("status", "")
        
        if status not in ["IN_PROGRESS", "PENDING"]:
            return False
        
        return time_diff > timedelta(minutes=self.timeout_minutes)
    
    def find_stuck_tasks(self) -> List[Dict]:
        tasks = self.get_all_tasks()
        return [task for task in tasks if self.is_task_stuck(task)]


def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("Поиск зависших задач...")
    print("Нажмите Ctrl+C для прерывания")
    print("=" * 60)
    
    try:
        monitor = RobotMonitor()
        stuck_tasks = monitor.find_stuck_tasks()
        
        print("\n" + "=" * 60)
        if stuck_tasks:
            print(f"НАЙДЕНО ЗАВИСШИХ ЗАДАЧ: {len(stuck_tasks)}")
            print("=" * 60)
            for task in stuck_tasks:
                print(f"\n  ID: {task['id']}")
                print(f"  Статус: {task['status']}")
                print(f"  Последнее обновление: {task['updated_at']}")
        else:
            print("ЗАВИСШИХ ЗАДАЧ НЕ ОБНАРУЖЕНО")
        print("=" * 60)
            
    except requests.exceptions.Timeout:
        print("\n ТАЙМАУТ: Сервер не отвечает")
    except requests.exceptions.ConnectionError as e:
        print(f"\n ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
    except Exception as e:
        print(f"\n ОШИБКА: {e}")


if __name__ == "__main__":
    main()
