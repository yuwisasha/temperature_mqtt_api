import secrets
import asyncio
import string
import signal

import uvloop
from gmqtt import Client, Subscription
from httpx import URL

from utils import get_random_string
from api import get_temperature, get_stations_temperature, get_api_info
from callbacks import assign_callbacks_to_client

TEMPERATURE_API = "https://api.data.gov.sg/v1/environment/air-temperature"
STATION_IDS = ("S50", "S107", "S60")

BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = "1883"  # "8885"

API_STR = "/api"

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

STOP = asyncio.Event()


def ask_exit(*args):
    STOP.set()


async def main(broker_host: URL, broker_port: str, token: str):
    # Client which publicate messages
    sub_client = Client(
        await get_random_string(6, string.ascii_letters + string.digits)
    )
    assign_callbacks_to_client(sub_client)
    # sub_client.set_auth_credentials(token, None)
    await sub_client.connect(broker_host, broker_port, ssl=False)
    sub_client.subscribe(
        [
            Subscription(f"{API_STR}/status"),
            Subscription(f"{API_STR}/temperature/#"),
        ]
    )

    # Client which recieve messages
    pub_client = Client(
        await get_random_string(6, string.ascii_letters + string.digits)
    )
    assign_callbacks_to_client(pub_client)
    # pub_client.set_auth_credentials(token, None)
    await pub_client.connect(broker_host, broker_port, ssl=False)

    temperature_data = await get_temperature(TEMPERATURE_API)
    stations_temerature = await get_stations_temperature(
        STATION_IDS, temperature_data
    )
    api_status = await get_api_info(temperature_data)

    pub_client.publish(f"{API_STR}/status", api_status, qos=1)

    for station in stations_temerature:
        pub_client.publish(
            f"{API_STR}/temperature/{station['station_id']}", station, qos=1
        )

    await STOP.wait()
    await pub_client.disconnect()
    await sub_client.disconnect(session_expiry_interval=0)


if __name__ == "__main__":
    token = secrets.token_urlsafe(16)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)
    loop.run_until_complete(main(BROKER_HOST, BROKER_PORT, token))
