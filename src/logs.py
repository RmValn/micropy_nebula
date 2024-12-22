import uasyncio as asyncio
import json
from .servers_interact.remote import Remote

class Log:

    @classmethod
    async def send_log(cls, log_message):
        """Асинхронно відправляє лог-повідомлення на сервер Flask."""
        # try:
            # Генеруємо JSON
            # log_data = json.dumps({"log": log_message})

            # Формуємо HTTP-запит
        print('тут блять')
        await Remote.send_request('logs', data=log_message)
        # except Exception as e:
        #     print(f"Error: {e}")

    @classmethod
    async def clear_logs(cls,server_url):
        """Надсилає запит на очищення логів."""
        try:
            await Remote.send_request('clear_logs',server_url=server_url)
        except Exception as e:
            print(f"Error cleaning logs: {e}")
            await cls.send_log(f"Error cleaning logs: {e}")
