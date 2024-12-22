import urequests
import ujson
import uasyncio as asyncio
class Remote:
    SERVER_URL = None

    @classmethod
    async def send_request(cls, path, server_url=None, data=None):
        cls.SERVER_URL = server_url
        url = f"http://{cls.SERVER_URL}/{path}"
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
            print("ой курва")
            response = urequests.post(url, headers=headers)

        print("Відповідь сервера:", response.text)
        response.close()
                