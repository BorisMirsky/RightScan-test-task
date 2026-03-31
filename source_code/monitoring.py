import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

import logging_config, mock_robot, mock_robot_fastapi, models
from logging_config import logger




class RobotMonitor:
    """
    Монитор для отслеживания зависших задач
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout_minutes: int = 10):
        self.base_url = base_url
        self.timeout_minutes = timeout_minutes
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_all_tasks(self) -> List[Dict]:
        """
        Получить все задачи через API с обработкой ошибок
        """
        try:
            logger.info(f"Запрос списка задач с {self.base_url}/tasks")
            response = await self.client.get(f"{self.base_url}/tasks")
            response.raise_for_status()
            
            tasks = response.json()
            logger.info(f"Получено {len(tasks)} задач")
            return tasks
            
        except httpx.TimeoutException:
            logger.error("Таймаут при запросе к API робота")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка {e.response.status_code}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Ошибка соединения с API: {e}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении задач: {e}")
            raise
    
    def is_task_stuck(self, task: Dict) -> bool:
        """
        Проверить, зависла ли задача
        
        Args:
            task: Словарь с данными задачи
            
        Returns:
            True если задача зависла, False в противном случае
        """
        try:
            updated_at_str = task.get("updated_at")
            if not updated_at_str:
                logger.warning(f"Задача {task.get('id')} не содержит поля updated_at")
                return False
            
            # Парсим время последнего обновления
            updated_at = datetime.fromisoformat(updated_at_str)
            now = datetime.now()
            time_diff = now - updated_at
            
            # Проверяем только задачи в статусе IN_PROGRESS или PENDING
            status = task.get("status", "")
            if status not in ["IN_PROGRESS", "PENDING"]:
                return False
            
            is_stuck = time_diff > timedelta(minutes=self.timeout_minutes)
            
            if is_stuck:
                logger.warning(
                    f"Обнаружена зависшая задача {task.get('id')}: "
                    f"статус={status}, не обновлялась {time_diff.total_seconds() / 60:.1f} минут"
                )
            
            return is_stuck
            
        except ValueError as e:
            logger.error(f"Ошибка парсинга даты для задачи {task.get('id')}: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при проверке задачи {task.get('id')}: {e}")
            return False
    
    async def find_stuck_tasks(self) -> List[Dict]:
        """
        Найти все зависшие задачи
        
        Returns:
            Список зависших задач
        """
        try:
            # Получаем все задачи
            tasks = await self.get_all_tasks()
            
            # Фильтруем зависшие
            stuck_tasks = [task for task in tasks if self.is_task_stuck(task)]
            
            logger.info(f"Найдено зависших задач: {len(stuck_tasks)} из {len(tasks)}")
            
            # Выводим детальную информацию о зависших задачах
            if stuck_tasks:
                logger.info("=== СПИСОК ЗАВИСШИХ ЗАДАЧ ===")
                for task in stuck_tasks:
                    updated_at = task.get("updated_at", "unknown")
                    logger.info(
                        f"ID: {task.get('id')}, "
                        f"Статус: {task.get('status')}, "
                        f"Последнее обновление: {updated_at}"
                    )
                logger.info("================================")
            
            return stuck_tasks
            
        except Exception as e:
            logger.error(f"Ошибка при поиске зависших задач: {e}")
            raise
    
    async def close(self):
        """Закрыть HTTP клиент"""
        await self.client.aclose()




async def main():
    """Основная асинхронная функция мониторинга"""
    monitor = RobotMonitor(timeout_minutes=10)
    
    try:
        logger.info("Запуск мониторинга зависших задач...")
        stuck_tasks = await monitor.find_stuck_tasks()
        
        # Вывод результатов
        print("\n" + "=" * 60)
        if stuck_tasks:
            print(f"⚠️  НАЙДЕНО ЗАВИСШИХ ЗАДАЧ: {len(stuck_tasks)}")
            print("=" * 60)
            for task in stuck_tasks:
                print(f"  • Задача ID: {task['id']}")
                print(f"    Статус: {task['status']}")
                print(f"    Последнее обновление: {task['updated_at']}")
                print()
        else:
            print("✅ ЗАВИСШИХ ЗАДАЧ НЕ ОБНАРУЖЕНО")
            print("=" * 60)
        
        return stuck_tasks
        
    except Exception as e:
        logger.critical(f"Критическая ошибка при выполнении мониторинга: {e}")
        print(f"\n❌ Ошибка: {e}")
        return []
    finally:
        await monitor.close()


if __name__ == "__main__":
    # Точка входа для запуска мониторинга
    asyncio.run(main())
