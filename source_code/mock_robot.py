
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum


from models import Task, TaskStatus, TaskCreate, TaskResponse


logger = logging.getLogger(__name__)


class MockRobotAPI:
    """
    Мок-сервер, имитирующий API робота с возможностью:
    - задержек ответов
    - случайных ошибок
    - "зависания" задач
    """
    
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1
        self._init_test_tasks()
    
    def _init_test_tasks(self):
        """Создание тестовых задач, включая зависшие"""
        now = datetime.now()
        
        # Нормальная задача (обновлена 5 минут назад)
        self.tasks[1] = Task(
            id=1,
            description="Сортировка товаров A-123",
            status=TaskStatus.IN_PROGRESS,
            priority=5,
            created_at=now - timedelta(minutes=15),
            updated_at=now - timedelta(minutes=5)
        )
        
        # Зависшая задача (не обновлялась 12 минут)
        self.tasks[2] = Task(
            id=2,
            description="Сортировка товаров B-456",
            status=TaskStatus.IN_PROGRESS,
            priority=8,
            created_at=now - timedelta(minutes=30),
            updated_at=now - timedelta(minutes=12)
        )
        
        # Очень зависшая задача (не обновлялась 25 минут)
        self.tasks[3] = Task(
            id=3,
            description="Сортировка товаров C-789",
            status=TaskStatus.IN_PROGRESS,
            priority=3,
            created_at=now - timedelta(minutes=40),
            updated_at=now - timedelta(minutes=25)
        )
        
        # Задача в статусе PENDING (создана, но не начата)
        self.tasks[4] = Task(
            id=4,
            description="Сортировка товаров D-012",
            status=TaskStatus.PENDING,
            priority=1,
            created_at=now - timedelta(minutes=8),
            updated_at=now - timedelta(minutes=8)
        )
        
        # Завершенная задача
        self.tasks[5] = Task(
            id=5,
            description="Сортировка товаров E-345",
            status=TaskStatus.COMPLETED,
            priority=10,
            created_at=now - timedelta(hours=1),
            updated_at=now - timedelta(minutes=45)
        )
    
    def get_all_tasks(self) -> List[Task]:
        return list(self.tasks.values())
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def create_task(self, description: str, priority: int) -> Task:
        now = datetime.now()
        task = Task(
            id=self.next_id,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            created_at=now,
            updated_at=now
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        logger.info(f"Создана новая задача: {task.id}")
        return task
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        if task_id not in self.tasks:
            return None     
        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.now()
        logger.debug(f"Обновлен статус задачи {task_id}: {status}")
        return task







