from nio.properties import VersionProperty
from nio.util.discovery import discoverable
from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@discoverable
class GreenGrassMQTTPublish(GreenGrassMQTTBase):
    """A publisher block for the MQTT protocol that is used by greengrass.
    This block will publish messages to a topic."""

    version = VersionProperty('1.0.0')

    def process_signals(self, signals):
        self.client.publish()
