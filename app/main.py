import asyncio
import signal
import ssl

import uvloop
from gmqtt import Subscription
from httpx import URL

from utils import get_client
from api import get_temperature, get_stations_temperature, get_api_info

TEMPERATURE_API = "https://api.data.gov.sg/v1/environment/air-temperature"
STATION_IDS = ("S50", "S107", "S60")

BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = "8885"

API_STR = "/api"

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

STOP = asyncio.Event()


def ask_exit(*args):
    STOP.set()


async def main(broker_host: URL, broker_port: str):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain("client.crt", "client.key")
    ssl_context.check_hostname = False

    # Client which recive messages
    sub_client = await get_client(
        username="ro",
        password="readonly",
        broker_host=broker_host,
        broker_port=broker_port,
        ssl_cntxt=ssl_context,
    )
    sub_client.subscribe(
        [
            Subscription(f"{API_STR}/status"),
            Subscription(f"{API_STR}/temperature/#"),
        ]
    )

    # Client which publicate messages
    pub_client = await get_client(
        username="wo",
        password="writeonly",
        broker_host=broker_host,
        broker_port=broker_port,
        ssl_cntxt=ssl_context,
    )

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
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)
    loop.run_until_complete(main(BROKER_HOST, BROKER_PORT))
