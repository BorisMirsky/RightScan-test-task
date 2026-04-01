mock_robot.py      # бизнес-логика и данные
mock_server.py     # HTTP сервер (запускается в терминале 1)
monitoring.py      # мониторинг (запускается в терминале 2)
logging_config.py  # логирование

Как запускать:
# Терминал 1
python mock_server.py

# Терминал 2
python monitoring.py