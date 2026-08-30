from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import json
from datetime import datetime


class ContactHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET-запросов"""
        try:
            # Читаем содержимое HTML-файла с помощью контекстного менеджера
            with open('work.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Возвращаем HTML-страницу
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        except FileNotFoundError:
            # Обработка ошибки 404 - файл не найден
            self.send_error_response(404, "Страница не найдена")
        except Exception as e:
            # Обработка ошибки 500 - внутренняя ошибка сервера
            print(f"❌ Ошибка сервера: {e}")
            self.send_error_response(500, "Внутренняя ошибка сервера")

    def do_POST(self):
        """Обработка POST-запросов"""
        try:
            if self.path == '/submit':
                # Получаем длину содержимого
                content_length = int(self.headers.get('Content-Length', 0))

                if content_length == 0:
                    # Обработка пустого запроса
                    self.send_error_response(400, "Пустой запрос")
                    return

                # Читаем данные POST-запроса
                post_data = self.rfile.read(content_length).decode('utf-8')

                # Парсим данные формы
                parsed_data = urllib.parse.parse_qs(post_data)

                # Извлекаем значения полей с проверкой
                name = parsed_data.get('name', [''])[0].strip()
                email = parsed_data.get('email', [''])[0].strip()
                message = parsed_data.get('message', [''])[0].strip()

                # Валидация данных
                if not name or not email or not message:
                    self.send_error_response(400, "Все поля обязательны для заполнения")
                    return

                # Выводим данные в консоль в красивом формате
                self.print_form_data(name, email, message)

                # Отправляем страницу с подтверждением
                self.send_success_response(name, email, message)

            else:
                # Если путь не "/submit", возвращаем 404
                self.send_error_response(404, "Страница не найдена")

        except ValueError as e:
            # Ошибка при парсинге данных
            print(f"❌ Ошибка парсинга: {e}")
            self.send_error_response(400, "Некорректные данные")
        except Exception as e:
            # Ошибка 500 - внутренняя ошибка сервера
            print(f"❌ Ошибка сервера: {e}")
            self.send_error_response(500, "Внутренняя ошибка сервера")

    def print_form_data(self, name, email, message):
        """Вывод данных формы в консоль"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "=" * 60)
        print(f"📨 ПОЛУЧЕНО НОВОЕ СООБЩЕНИЕ [{timestamp}]")
        print("=" * 60)
        print(f"👤 Имя: {name}")
        print(f"📧 Email: {email}")
        print(f"💬 Сообщение: {message}")
        print("=" * 60 + "\n")

        # Опционально: сохраняем в файл лога
        with open('messages.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{timestamp}] Имя: {name}, Email: {email}, Сообщение: {message}\n")

    def send_success_response(self, name, email, message):
        """Отправка страницы с подтверждением"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        response_html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Сообщение отправлено</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                }}
                .success-card {{
                    border-radius: 20px;
                    border: none;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }}
                .success-icon {{
                    font-size: 80px;
                    animation: bounce 1s ease infinite;
                }}
                @keyframes bounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                .data-section {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                }}
                .btn-back {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    padding: 12px 40px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }}
                .btn-back:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="card success-card p-4">
                            <div class="card-body text-center p-5">
                                <div class="success-icon">✅</div>
                                <h1 class="card-title mt-3 mb-4">Сообщение успешно отправлено!</h1>
                                <p class="card-text text-muted mb-4">Спасибо за ваше сообщение. Мы свяжемся с вами в ближайшее время.</p>

                                <div class="data-section text-start">
                                    <h6 class="mb-3">📋 Данные из формы:</h6>
                                    <p><strong>👤 Имя:</strong> {name}</p>
                                    <p><strong>📧 Email:</strong> {email}</p>
                                    <p><strong>💬 Сообщение:</strong><br>{message}</p>
                                </div>

                                <a href="/" class="btn btn-primary btn-back mt-4">🏠 Вернуться на главную</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
        self.wfile.write(response_html.encode('utf-8'))

    def send_error_response(self, status_code, message):
        """Отправка страницы с ошибкой"""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        error_pages = {
            404: {
                'title': '404 - Страница не найдена',
                'icon': '🔍',
                'description': 'Извините, запрашиваемая страница не существует.',
                'color': '#ff6b6b'
            },
            400: {
                'title': '400 - Плохой запрос',
                'icon': '⚠️',
                'description': 'Извините, запрос содержит некорректные данные.',
                'color': '#feca57'
            },
            500: {
                'title': '500 - Внутренняя ошибка сервера',
                'icon': '💥',
                'description': 'Извините, на сервере произошла ошибка. Попробуйте позже.',
                'color': '#ff4757'
            }
        }

        error_info = error_pages.get(status_code, {
            'title': f'{status_code} - Ошибка',
            'icon': '❌',
            'description': 'Произошла ошибка.',
            'color': '#2f3542'
        })

        error_html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{error_info['title']}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    color: white;
                }}
                .error-card {{
                    background: rgba(255,255,255,0.05);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    border: 1px solid rgba(255,255,255,0.1);
                    padding: 60px 40px;
                }}
                .error-icon {{
                    font-size: 100px;
                    display: block;
                    margin-bottom: 30px;
                }}
                .error-title {{
                    font-size: 48px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
                .error-description {{
                    font-size: 18px;
                    color: rgba(255,255,255,0.7);
                    margin-bottom: 30px;
                }}
                .btn-home {{
                    background: {error_info['color']};
                    border: none;
                    padding: 12px 40px;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }}
                .btn-home:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="error-card text-center">
                            <span class="error-icon">{error_info['icon']}</span>
                            <h1 class="error-title">{error_info['title']}</h1>
                            <p class="error-description">{error_info['description']}</p>
                            <a href="/" class="btn btn-primary btn-home">🏠 Вернуться на главную</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode('utf-8'))


def run_server(port=8000):
    """Запуск сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ContactHandler)

    print("=" * 60)
    print("🚀 СЕРВЕР ЗАПУЩЕН")
    print("=" * 60)
    print(f"📍 Адрес: http://localhost:{port}")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    print(f"📄 Файл: work.html")
    print(f"📋 Статус: {'✅ Найден' if os.path.exists('work.html') else '❌ Не найден'}")
    print("=" * 60)
    print("📝 Нажмите Ctrl+C для остановки сервера")
    print("=" * 60 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
        httpd.server_close()


if __name__ == '__main__':
    run_server()