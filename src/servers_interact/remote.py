import usocket
import ujson
import uasyncio as asyncio
class Remote:
    SERVER_URL = "192.168.0.20"
    PORT = 5000

    @classmethod
    async def send_request(cls, path, data=None):
        if data:
            if path == 'logs':
                print(f'Невідформатовано - {data}')
                data = ujson.dumps({'log': data})
                print(f'JSON - {data}')
                request = (
                f"POST /{path} HTTP/1.1\r\n"
                f"Host: {cls.SERVER_URL}\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: {len(data)}\r\n"
                f"Connection: close\r\n\r\n"
                f"{data}" )
                print(f'Запит курва єбать - {request}')
            if path == 'pin_status':
                data = ujson.dumps(data)
                request = (
                f"POST /{path} HTTP/1.1\r\n"
                f"Host: {cls.SERVER_URL}\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: {len(data)}\r\n"
                f"Connection: close\r\n\r\n"
                f"{data}" )
                print(f'pin_status -------{request}')
        else:
            print('ой курва')
            request = (
            f"POST /{path} HTTP/1.1\r\n"
            f"Host: {cls.SERVER_URL}\r\n"
            "Content-Type: application/json\r\n"
            "Content-Length: 0\r\n"
            "Connection: close\r\n\r\n"
            )
        addr = usocket.getaddrinfo(cls.SERVER_URL, cls.PORT)[0][-1]
        reader, writer = await asyncio.open_connection(addr[0], addr[1])

        writer.write(request.encode('utf-8'))
        await writer.drain()

        response = await reader.read(1024)
        print("Відповідь сервера:", response.decode('utf-8'))

        writer.close()
        await writer.wait_closed()
                