from nio.properties import VersionProperty
from nio.util.discovery import discoverable
from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@discoverable
class GreenGrassMQTTSubscribe(GreenGrassMQTTBase):
    """A subscriber block for the MQTT protocol that is used by greengrass.
    This block will grab messages from a certain topic and notify them."""

    version = VersionProperty('1.0.0')

    def configure(self):
        self.client.subscribe()
        super().configure()

    def watch_topic(self, topic):
        # grab incoming messages

        # notify messages to the service
        self.notify_signals([])
