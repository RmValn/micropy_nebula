import uasyncio as asyncio
from .wifi import connectWiFi
from .servers_interact.local import Router
from .servers_interact.remote import Remote
from .logs import Log
from .pin_state import send_inputs
from .ota import OTA
import network

class Nebula(Router):
    def __init__(self, ssid, password, server_ip):
        super().__init__()
        asyncio.run(self.initialize(ssid, password, server_ip))

    async def initialize(self, ssid, password, server_ip):
        """Ініціалізація Wi-Fi та запуск асинхронних завдань."""
        print("Підключення до Wi-Fi...")
        wifi_config = await self.connectWiFi(ssid, password)
        print(f"Wi-Fi підключено: {wifi_config}")

        # Запуск серверів та інших задач
        await self.start_async_tasks(server_ip)

        # Запуск циклу подій
        self.run_event_loop()

    @staticmethod
    async def connectWiFi(ssid, password):
        """Асинхронне підключення до Wi-Fi."""
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(ssid, password)

        while not wifi.isconnected():
            await asyncio.sleep(0.1)  # Замість блокуючого `pass`

        return wifi.ifconfig()

    async def start_async_tasks(self, server_ip):
        """Запуск асинхронних завдань."""
        try:
            print("Програма почала роботу.")
            Remote.SERVER_URL = server_ip
            await Log.clear_logs()
            await asyncio.gather(
                Router.restart_server(),
                OTA.check_for_update(),
                send_inputs()
            )
            print("Програма готова до роботи.")
        except Exception as e:
            print(f"Помилка під час виконання завдань: {e}")

    @staticmethod
    def run_event_loop():
        """Запускає цикл подій."""
        print("Запуск циклу подій...")
        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except Exception as e:
            print(f"Помилка у циклі подій: {e}")
