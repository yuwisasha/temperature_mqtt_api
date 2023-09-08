import logging
from typing import Any

from gmqtt import Client

logging.basicConfig(level=logging.INFO)


def on_connect(client: Client, flags, rc, propeties) -> None:
    logging.info("[CONNECTED {}]".format(client._client_id))


def on_disconnect(client: Client, packet, exc=None) -> None:
    logging.info("[DISCONNECTED {}]".format(client._client_id))


def on_subscribe(client: Client, mid, qos: int, properties) -> None:
    logging.info("[SUBSCRIBED {}] QOS: {}".format(client._client_id, qos))


async def on_message(
    client: Client, topic: str, payload: Any, qos: int, properties
) -> None:
    logging.info(
        "[RECV MSG {}] TOPIC: {} PAYLOAD: {} QOS: {} PROPERTIES: {}".format(
            client._client_id, topic, payload, qos, properties
        )
    )

    return 0


def assign_callbacks_to_client(client: Client) -> None:
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
