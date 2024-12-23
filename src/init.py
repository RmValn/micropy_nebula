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
        asyncio.run(Init.main(server_ip))

    @staticmethod
    async def main(server_ip):
        Remote.SERVER_URL = server_ip
        await Log.clear_logs()
        await asyncio.gather(Server.restart(),OTA.check_for_update(),send_inputs())
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