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
        response = self.client.subscribe(topic=self.topic(),
                                         QoS=0,
                                         callback=self._handle_message)
        if response:
            self.logger.info("Subscribed to topic `{}`, success: {}"
                             .format(self.topic(), response))
        else:
            self.logger.error("Could not subscribe to topic `{}`, success: "
                              "{}".format(self.topic(), response))

    def stop(self):
        response = self.client.unsubscribe(self.topic())
        if response:
            self.logger.info("Unsubscribed from topic `{}`"
                             .format(self.topic()))
        else:
            self.logger.error("Could not unsubscribe from topic `{}`, returned "
                              "{}".format(self.topic(), response))
        super().stop()

    def _handle_message(self, client, userdata, message):
        self.logger.debug("Received message from client '{}' on topic '{}': "
                          "{}".format(client, message.topic, message.payload))
        self.notify_signals([Signal({"client": client,
                                     "userdata": userdata,
                                     "payload": message.payload,
                                     "topic": message.topic})])
