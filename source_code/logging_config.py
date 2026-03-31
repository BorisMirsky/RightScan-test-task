import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('robot_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
