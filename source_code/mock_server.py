import json
import signal
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

from mock_robot import MockRobotAPI

robot_api = MockRobotAPI()
server = None


def signal_handler(sig, frame):
    print("\n\nОстановка сервера...")
    if server:
        server.shutdown()
    sys.exit(0)


class RobotRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/tasks":
            tasks = robot_api.get_all_tasks()
            response = [
                {
                    "id": task.id,
                    "status": task.status.value,
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]
            self._send_response(200, response)
        else:
            self._send_response(404, {"error": "Not found"})
    
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        pass


def main():
    global server
    signal.signal(signal.SIGINT, signal_handler)
    
    server = HTTPServer(('127.0.0.1', 8000), RobotRequestHandler)
    print("=" * 60)
    print("Сервер запущен на http://127.0.0.1:8000")
    print("Проверьте: http://127.0.0.1:8000/tasks")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
