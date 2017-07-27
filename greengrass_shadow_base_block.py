from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from copy import deepcopy

from nio.util.discovery import not_discoverable
from nio.properties import StringProperty, BoolProperty

from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@not_discoverable
class GreenGrassMQTTShadowBase(GreenGrassMQTTBase):
    """The base block for Greengrass device shadows. This block is responsible
    for connecting to the local greengrass core via MQTT and setting up a 
    handler with which to interact with the device shadows."""

    thing_name = StringProperty(title="Thing name", default="",
                                allow_none=False)
    persistent_subscribe = BoolProperty(title="Persistent Subscription",
                                        default=True)

    def __init__(self):
        super().__init__()
        self.client = deepcopy(AWSIoTMQTTShadowClient)
        self.shadow_handler = None

    def configure(self, context):
        super().configure(context)
        self.shadow_handler = self.client.createShadowHandlerWithName(
            self.thing_name(),
            isPersistentSubscribe=self.persistent_subscribe())
