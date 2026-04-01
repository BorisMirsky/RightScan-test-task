Проект состоит из файлов:

mock_robot.py      # бизнес-логика и данные
mock_server.py     # HTTP сервер (запускается в терминале 1)
monitoring.py      # мониторинг (запускается в терминале 2)
logging_config.py  # логирование
robot_monitor.log  # текстовый файл с логами.


Как пользоваться:

1) Перейти в WriteScan-test-task\source_code.

2) Поставить зависимости из requirements.txt.

3) Перейти в WriteScan-test-task\source_code\venv_src\Scripts. 
Открыть два окна терминала, активировать в каждом виртуальное окружение.

4) Запуск
   # Терминал 1
   python mock_server.py

   # Терминал 2
   python monitoring.py



