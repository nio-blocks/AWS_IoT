from nio.properties import VersionProperty, StringProperty
from nio.util.discovery import discoverable
from nio.signal.base import Signal
from .aws_iot_mqtt_base_block import AWSIoTMQTTBase


@discoverable
class AWSIoTMQTTSubscribe(AWSIoTMQTTBase):
    """A subscriber block for the MQTT protocol that is used by AWS IoT.
    This block will grab messages from a certain topic and notify them."""

    version = VersionProperty('1.0.0')
    topic = StringProperty(title="Topic", allow_none=False)

    def start(self):
        super().start()
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
        self.logger.debug("Received message for client '{}' on topic '{}': "
                          "{}".format(client._client_id, message.topic,
                                      message.payload))

        if self.client._mqttCore.getClientID() != client._client_id:
            self.logger.warning("Received message intended for different "
                                "client({}).".format(client._client_id))

        self.notify_signals([Signal({"client": client,
                                     "userdata": userdata,
                                     "payload": message.payload,
                                     "topic": message.topic})])
