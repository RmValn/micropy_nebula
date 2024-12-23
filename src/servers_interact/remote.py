import urequests
import ujson
import uasyncio as asyncio
class Remote:
    SERVER_URL = None

    @classmethod
    async def send_request(cls, path, server_url=None, data=None, method='POST'):
        if server_url:
            addr = server_url
        else:
            addr = cls.SERVER_URL
        url = f"http://{addr}/{path}"
        if not cls.SERVER_URL:
            raise ValueError("SERVER_URL не встановлено. Передайте server_url.")

        print(f"Використовується сервер: {addr}")
        headers = {"Content-Type": "application/json"}
        if data:
            data = ujson.dumps(data)
        if method == 'POST':
            response = urequests.post(url, headers=headers, data=data)
        elif method == 'GET':
            response = urequests.get(url, headers=headers)
        print("Відповідь сервера:", response.text)
        response.close()
        return response
                