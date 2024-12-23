import uasyncio as asyncio
import gc

class Router:
    _instance = None

    def __new__(cls, *args, **kwargs):
        print(f"Router.__new__ called. Current _instance: {cls._instance}")
        if not cls._instance:
            print("Creating a new Router instance.")
            cls._instance = super().__new__(cls)
            cls._instance.routes = {}
        print(f"New _instance: {cls._instance}")
        return cls._instance
    
    # def __init__(self):
    #     self.routes = {}  # Глобальний словник маршрутів
    #     self.restart_task = None
    #     self.route_called = False
    #     print("Router initialized")

    @classmethod
    def get_instance(cls):
        return cls._instance

    def route(self, path):
        """Декоратор для реєстрації маршруту."""
        self.route_called = True
        def decorator(func):
            self.routes[path] = func
            print(f"Route registered: {path} -> {func}")
            print('хто тут')
            return func
        return decorator
    
    async def schedule_restart(self):
        """Відкладений перезапуск сервера."""
        try:
            print('а тут хтось є?')
            await asyncio.sleep(0.5)  # Час для реєстрації всіх маршрутів
            await Server.restart(self)
        except asyncio.CancelledError:
            print("Restart task was cancelled.")

    @classmethod
    async def __handle_request(cls, reader, writer):
        """Обробка HTTP-запиту."""
        try:
            request = await reader.read(1024)
            request = request.decode("utf-8")
            print(f"Request: {request}")

            # Парсинг шляху
            path = request.split(" ")[1]
            if "POST /update_signal" in request:
                print("Сигнал оновлення отримано!")
                response = "HTTP/1.1 200 OK\r\n\r\nОновлення запущено"
                writer.write(response.encode('utf-8'))
                await writer.drain()
                # await check_for_update()
                await writer.aclose()
                return
            # Виклик обробника маршруту
            print(cls._instance)
            print(f"Registered routes: {cls.get_instance().routes}")
            print(f"Requested path: {path}")
            if path in cls.get_instance().routes:
                await cls.get_instance().routes[path](writer)
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nNot found"
                writer.write(response.encode("utf-8"))
                await writer.drain()
        finally:
            await writer.aclose()


class Server:
    server = None

    @classmethod
    async def restart(cls):
        if cls.server:
            cls.server.close()
            await cls.server.wait_closed()
            gc.collect()
            print('Server stoped')
        cls.server = await asyncio.start_server(Router.__handle_request, "0.0.0.0", 80)
        print(f"OTA-server started on http://0.0.0.0:80 {cls.server}")
        while True:
            await asyncio.sleep(1) 
        # except Exception as e:
        #     print(f"Error starting OTA-server: {e}")

