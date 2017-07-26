from nio.properties import VersionProperty, StringProperty, Property
from nio.util.discovery import discoverable
from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@discoverable
class GreenGrassMQTTPublish(GreenGrassMQTTBase):
    """A publisher block for the MQTT protocol that is used by greengrass.
    This block will publish messages to a topic."""

    version = VersionProperty('1.0.0')
    topic = StringProperty(title="Topic", allow_none=False)
    data_to_publish = Property(title="Data to Publish", default="{{ $text }}")

    def process_signals(self, signals):
        for signal in signals:
            self.logger.debug("Publishing signal to topic '{}': {}"
                              .format(self.topic(),
                                      self.data_to_publish(signal)))
            response = self.client.publish(topic=self.topic(),
                                           payload=self.data_to_publish(signal),
                                           QoS=0)
            self.logger.debug("Got response {0}, success: {0}".format(response))
