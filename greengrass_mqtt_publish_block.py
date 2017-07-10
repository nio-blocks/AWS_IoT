from nio.properties import VersionProperty, StringProperty
from nio.util.discovery import discoverable
from greengrass_mqtt_base_block import GreenGrassMQTTBase


@discoverable
class GreenGrassMQTTPublish(GreenGrassMQTTBase):
    """A publisher block for the MQTT protocol that is used by greengrass.
    This block will publish messages to a topic."""

    version = VersionProperty('1.0.0')
    topic = StringProperty(title="Topic", allow_none=False)

    def process_signals(self, signals):
        for signal in signals:
            self.logger.debug("Publishing signal to topic '{}': {}"
                              .format(self.topic(), signal.to_dict()))
            self.client.publish(self.topic(), signal.to_dict(), 0)
