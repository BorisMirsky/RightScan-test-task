import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskCreate(BaseModel):
    """Модель для создания задачи"""
    description: str = Field(..., min_length=1, max_length=500)
    priority: int = Field(1, ge=1, le=10)


class Task(BaseModel):
    """Модель задачи"""
    id: int
    description: str
    status: TaskStatus
    priority: int
    created_at: datetime
    updated_at: datetime


class TaskResponse(BaseModel):
    """Модель для API ответа"""
    id: int
    status: str  # Строка, а не Enum
    updated_at: str  # Строка ISO формата, а не datetime
