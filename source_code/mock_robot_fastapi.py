import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn


import sys
#sys.path.append('C:\Users\Борис\source\WriteScan-test-task\src')
import logging_config, models # mock_robot
from mock_robot import MockRobotAPI
from models import Task, TaskStatus, TaskCreate, TaskResponse



app = FastAPI(title="Robot API Mock", description="Мок-сервер API робота-сортировщика")
robot_api = MockRobotAPI()


@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks():
    """
    Получить список всех задач
    """
    try:
        # Имитация задержки API
        await asyncio.sleep(0.1)
        
        tasks = robot_api.get_all_tasks()
        return [
            TaskResponse(
                id=task.id,
                status=task.status.value,
                updated_at=task.updated_at.isoformat()
            )
            for task in tasks
        ]
    except Exception as e:
        logger.error(f"Ошибка при получении списка задач: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """
    Получить статус конкретной задачи
    """
    try:
        await asyncio.sleep(0.05)  # Имитация задержки
        
        task = robot_api.get_task(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        return TaskResponse(
            id=task.id,
            status=task.status.value,
            updated_at=task.updated_at.isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении задачи {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate):
    """
    Создать новую задачу
    """
    try:
        await asyncio.sleep(0.1)
        
        task = robot_api.create_task(task_data.description, task_data.priority)
        return TaskResponse(
            id=task.id,
            status=task.status.value,
            updated_at=task.updated_at.isoformat()
        )
    except Exception as e:
        logger.error(f"Ошибка при создании задачи: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )



def main():
    """Точка входа для запуска мок-сервера"""
    print("=" * 60)
    print("Запуск мок-сервера робота-сортировщика")
    print("Сервер доступен по адресу: http://localhost:8000")
    print("Документация API: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()

