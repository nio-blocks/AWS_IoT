from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

from nio.util.discovery import not_discoverable

from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@not_discoverable
class GreenGrassMQTTShadowBase(GreenGrassMQTTBase):
    """The base block for Greengrass device shadows. This block is responsible
    for connecting to the local greengrass core via MQTT and managing device
    shadows for devices in the local greengrass core."""

    def __init__(self):
        self.client = AWSIoTMQTTShadowClient
        super().__init__()
