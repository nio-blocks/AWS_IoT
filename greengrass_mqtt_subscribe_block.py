from nio.properties import VersionProperty, StringProperty
from nio.util.discovery import discoverable
from nio.signal.base import Signal
from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@discoverable
class GreenGrassMQTTSubscribe(GreenGrassMQTTBase):
    """A subscriber block for the MQTT protocol that is used by greengrass.
    This block will grab messages from a certain topic and notify them."""

    version = VersionProperty('1.0.0')
    topic = StringProperty(title="Topic", allow_none=False)

    def configure(self):
        self.client.subscribe(self.topic(), 1, self.handle_message)
        super().configure()

    def stop(self):
        self.client.unsubscribe(self.topic())
        super().stop()

    def handle_message(self, message):
        self.notify_signals([Signal({})])
