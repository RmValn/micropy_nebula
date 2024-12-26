import uasyncio as asyncio
import gc
from ..logs import Log
from ..ota import OTA

class Router:
    _instance = None
    def __init__(self):
        Router._instance = self
        Router._instance.routes = {}
        
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            raise ValueError("Router instance not initialized!")
        return cls._instance

    def route(self, path):
        """Декоратор для реєстрації маршруту."""
        self.route_called = True
        def decorator(func):
            self.routes[path] = func
            print(f"Route registered: {path} -> {func}")
            Log.send_log(f"Route registered: {path} -> {func}")
            return func
        return decorator
    
    async def __handle_request(self, reader, writer):
        """Обробка HTTP-запиту."""
        try:
            request = await reader.read(1024)
            request = request.decode("utf-8")
            print(f"Request: {request}")
            Log.send_log(f"Request: {request}")

            # Парсинг шляху
            path = request.split(" ")[1]
            if "POST /update_signal" in request:
                print("Сигнал оновлення отримано!")
                Log.send_log("Сигнал оновлення отримано!")
                response = "HTTP/1.1 200 OK\r\n\r\nОновлення запущено"
                writer.write(response.encode('utf-8'))
                await writer.drain()
                await OTA.check_for_update()
                await writer.aclose()
                return
            # Виклик обробника маршруту
            print(f"Registered routes: {self.routes}")
            print(f"Requested path: {path}")
            Log.send_log(f"Registered routes: {self.routes}")
            Log.send_log(f"Requested path: {path}")
            if path in self.routes:
                await self.routes[path](writer)
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nNot found"
                writer.write(response.encode("utf-8"))
            await writer.drain()
        finally:
            await writer.aclose()
    
    async def restart(self):
        print(f"Restart called. Router._instance: {self}")
        await asyncio.start_server(self.__handle_request, "0.0.0.0", 80)
        print(f"OTA-server started on http://0.0.0.0:80")
        Log.send_log(f"OTA-server started on http://0.0.0.0:80")
        while True:
            await asyncio.sleep(1) 

    @classmethod
    async def restart_server(cls):
        await cls.get_instance().restart()


class Server:
    server = None

    @classmethod
    async def restart(cls):
        print(f"Restart called. Router._instance: {Router.get_instance()}")
        if cls.server:
            cls.server.close()
            await cls.server.wait_closed()
            gc.collect()
            print('Server stoped')
        cls.server = await asyncio.start_server(Router.get_instance().__handle_request, "0.0.0.0", 80)
        print(f"OTA-server started on http://0.0.0.0:80 {cls.server}")
        Log.send_log(f"OTA-server started on http://0.0.0.0:80")
        while True:
            await asyncio.sleep(1) 

