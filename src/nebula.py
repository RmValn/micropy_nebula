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
        print(Nebula.connectWiFi(ssid, password))
        super().__init__()
        asyncio.create_task(self.start_async_tasks(server_ip))
        self.ensure_event_loop_running()

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
    def connectWiFi(ssid, password):
        print('Підключення до Wi-Fi...')
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(ssid, password)

        # Чекаємо на підключення
        while not wifi.isconnected():
            pass
        print('Wi-Fi підключено:', wifi.ifconfig())
        return wifi.ifconfig()

    @staticmethod
    def ensure_event_loop_running():
        """Запускає цикл подій, якщо він ще не запущений."""
        try:
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            print(f"Помилка під час запуску циклу подій: {e}")