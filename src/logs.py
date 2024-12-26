import uasyncio as asyncio
import json
from .servers_interact.remote import Remote

class Log:

    @classmethod
    async def send_log(cls, log_message):
        """відправляє лог-повідомлення на сервер Flask."""
        await Remote.send_request('logs', data=log_message)

    @classmethod
    async def clear_logs(cls):
        """Надсилає запит на очищення логів."""
        try:
            await Remote.send_request('clear_logs')
        except Exception as e:
            print(f"Error cleaning logs: {e}")
            await cls.send_log(f"Error cleaning logs: {e}")
