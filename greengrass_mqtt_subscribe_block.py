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

    def configure(self, context):
        super().configure(context)
        self.client.subscribe(topic=self.topic(),
                              QoS=0,
                              callback=self.handle_message)

    def stop(self):
        self.client.unsubscribe(self.topic())
        super().stop()

    def handle_message(self, client, userdata, message):
        self.logger.debug("Received message from client '{}' on topic '{}'. "
                          "{}".format(client, message.topic, message.payload))
        self.notify_signals([Signal({"client": client,
                                     "userdata": userdata,
                                     "payload": message.payload,
                                     "topic": message.topic})])
