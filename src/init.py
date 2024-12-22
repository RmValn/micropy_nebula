import uasyncio as asyncio
from .wifi import connectWiFi
from .servers_interact.local import Server
from .servers_interact.remote import Remote
from .logs import Log
from .pin_state import send_inputs
from .ota import OTA
class Init:
    def __init__(self,ssid,password,server_ip):
        connectWiFi(ssid, password)
        asyncio.run(Init.main(server_ip))

    @staticmethod
    async def main(server_ip):
        await Log.clear_logs()
        await asyncio.gather(Server.restart(),OTA.check_for_update(server_ip),send_inputs())
        print("Програма готова до роботи.")