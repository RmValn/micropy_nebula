import uasyncio as asyncio
import machine
from .servers_interact.remote import Remote
import gc
from .config import version as CURRENT_VERSION 
from .logs import Log
# from servers_interact.remote import Remote

class OTA:

    @classmethod
    async def check_for_update(cls, server_url):
        """Періодично перевіряє наявність оновлень."""
        try:
            print("Checking update...")
            await Log.send_log("Checking update...")
            response = Remote.send_request('version', server_url)
            if response.status_code == 200:
                server_version = response.json().get("version")
                if server_version != CURRENT_VERSION:
                    print(f"Server version: {server_version}, Current: {CURRENT_VERSION}. Updating...")
                    await Log.send_log(f"Server version: {server_version}, Current: {CURRENT_VERSION}. Updating...")
                    await cls.perform_update(server_version)
                else:
                    print("Same version. No need to update")
                    await Log.send_log("Same version. No need to update")
            else:
                await Log.send_log(response.content)
            response.close()
        except Exception as e:
            print(f"Checking update error: {e}")
            await Log.send_log(f"Checking update error: {e}")
        finally:
            gc.collect()

    @classmethod
    async def update_config_version(cls, new_version):
        """Оновлює версію програми в config.py."""
        try:
            with open("config.py", "w") as f:
                f.write(f'version = "{new_version}"\n')
            await Log.send_log("Unpated versioawaitn in config.py!")
        except Exception as e:
            await Log.send_log(f"Update error in config.py: {e}")
            pass


# Викликайте цю функцію після підключення до Wi-Fi:

    @classmethod
    async def perform_update(cls, server_version):
        """Завантажує нову версію програми та оновлює main.py."""
        try:
            await Log.send_log("Dowloading file...")
            response = Remote.send_request('main.py')
            new_version = server_version
            if response.status_code == 200:
                with open("main.py", "w") as f:
                    f.write(response.text)
                response.close()
                await Log.send_log("Flie main.py updated!")
                await cls.update_config_version(new_version) 
                await Log.send_log("Rebooting for apply...")
                asyncio.sleep(2)
                machine.reset()  # Перезавантаження контролера
            else:
                print(f"Download error: HTTP {response.status_code}")
                await Log.send_log(f"Download error: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error OTA: {e}")
            await Log.send_log(f"Error OTA: {e}")
        finally:
            gc.collect()
