import urequests
import ujson
import uasyncio as asyncio
class Remote:


    @classmethod
    async def send_request(cls, server_url, path, data=None):
        url = f"http://{server_url}/{path}"
        headers = {"Content-Type": "application/json"}

        if data:
            if path == "logs":
                print(f"Невідформатовано - {data}")
                data = ujson.dumps({"log": data})
                print(f"JSON - {data}")
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
                