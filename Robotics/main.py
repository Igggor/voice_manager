import requests
import serial
from time import sleep
from dotenv import dotenv_values


conf = dotenv_values(".env")
TABLE = 'Devices'  # имя таблицы
URL = f"https://test.igreeda.keenetic.pro/API/{TABLE}"
API_KEY = conf["KEY"]


def get(url: str, key: str):
    getparams = {
        "key": key,
        'title': "AnLamp",
    }
    response = requests.get(url=url, params=getparams)
    data = response.json()
    return data


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS1')
    try:
        while True:
            data = get(URL, API_KEY)[0]["settings"]["type"]
            ser.write(data.encode('utf-8'))
            sleep(1)
    except Exception as ex:
        print(ex)
    finally:
        ser.close()
