from machine import Pin
import urequests
import uasyncio as asyncio
from servers_interact.remote import Remote
# Входи
inputs = {
    "D0": Pin(16, Pin.IN),
    "D1": Pin(5, Pin.IN),
    "D2": Pin(4, Pin.IN),
    "D4": Pin(2, Pin.OUT),

}

SERVER_URL = "http://your-flask-server-ip/inputs_status"


async def send_inputs():
    while True:
        print('Надсилання інпутів')
        # Зчитуємо всі входи
        data = {pin: inputs[pin].value() for pin in inputs}
        # try:
        await Remote.send_request('pin_status', data)
        # except Exception as e:
        #     print("Failed to send data:", e)
        await asyncio.sleep(5)  # Інтервал між відправками
