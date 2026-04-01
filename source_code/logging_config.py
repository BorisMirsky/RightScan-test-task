
import logging


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
