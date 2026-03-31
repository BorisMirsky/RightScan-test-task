import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

import logging_config, monitoring, mock_robot, mock_robot_fastapi, models




async def main():
    """
    Основная функция для запуска мониторинга
    """
    monitor = RobotMonitor(timeout_minutes=10)
    
    try:
        logger.info("Запуск мониторинга зависших задач...")
        stuck_tasks = await monitor.find_stuck_tasks()
        
        # Вывод результатов
        if stuck_tasks:
            print("\n" + "="*60)
            print(f"⚠️  НАЙДЕНО ЗАВИСШИХ ЗАДАЧ: {len(stuck_tasks)}")
            print("="*60)
            for task in stuck_tasks:
                print(f"  • Задача ID: {task['id']}")
                print(f"    Статус: {task['status']}")
                print(f"    Последнее обновление: {task['updated_at']}")
                print()
        else:
            print("\n" + "="*60)
            print("✅ ЗАВИСШИХ ЗАДАЧ НЕ ОБНАРУЖЕНО")
            print("="*60)
        
        return stuck_tasks
        
    except Exception as e:
        logger.critical(f"Критическая ошибка при выполнении мониторинга: {e}")
        print(f"\n❌ Ошибка: {e}")
        return []
    finally:
        await monitor.close()


# ==================== ТОЧКА ВХОДА ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        # Запуск мок-сервера
        print("Запуск мок-сервера робота на http://localhost:8000")
        print("Документация API: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    else:
        # Запуск мониторинга
        print("Запуск мониторинга зависших задач...\n")
        asyncio.run(main())



        
