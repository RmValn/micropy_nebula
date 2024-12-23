import urequests
import ujson
import uasyncio as asyncio
class Remote:
    SERVER_URL = None

    @classmethod
    async def send_request(cls, path, server_url=None, data=None):
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
            if path == "logs":
                print(f"Невідформатовано - {data}")
                data = ujson.dumps({"log": data})
                print(f"JSON - {data}")
                print(url)
                response = urequests.post(url, headers=headers, data=data)
                print(f"Запит курва єбать - {data}")
            else:
                data = ujson.dumps(data)
                response = urequests.post(url, headers=headers, data=data)
                print(f"pin_status ------- {data}")
        else:
            print(f"ой курва, url = {url}")
            response = urequests.get(url, headers=headers)

        print("Відповідь сервера:", response.text)
        response.close()
                