import uasyncio as asyncio
from .wifi import connectWiFi
from .servers_interact.local import Server
from .servers_interact.remote import Remote
from .logs import Log
from .pin_state import send_inputs
from .ota import OTA
import network
class Init:
    def __init__(self,ssid,password,server_ip):
        print(Init.connectWiFi(ssid, password))
        asyncio.run(self.start_async_tasks(server_ip))

    async def start_async_tasks(self, server_ip):
        """Запуск асинхронних завдань."""
        print("Програма почала роботу.")
        Remote.SERVER_URL = server_ip
        await Log.clear_logs()
        await asyncio.gather(
            Server.restart(), 
            OTA.check_for_update(),
            send_inputs()
        )
        print("Програма готова до роботи.")
        
    @staticmethod
    def connectWiFi(ssid,password):
        print('прейом')
        # Підключення до Wi-Fi
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(ssid, password)

        # Чекати на підключення
        while not wifi.isconnected():
            pass
        return wifi.ifconfig()