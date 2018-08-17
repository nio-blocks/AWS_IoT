import json
from nio.properties import VersionProperty, StringProperty
from nio.signal.base import Signal
from nio import GeneratorBlock
from .aws_iot_mqtt_base_block import AWSIoTMQTTBase


# JSONDecodeError is raised in py3.5+
try:
    json_decode_error = json.JSONDecodeError
except:
    json_decode_error = ValueError

class AWSIoTMQTTSubscribe(AWSIoTMQTTBase, GeneratorBlock):
    """A subscriber block for the MQTT protocol that is used by AWS IoT.
    This block will grab messages from a certain topic and notify them."""

    version = VersionProperty("1.0.0")
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
            self.logger.error(
                "Could not unsubscribe from topic `{}`, returned {}".format(
                    self.topic(), response)
            )
        super().stop()

    def _handle_message(self, client, userdata, message):
        # client and userdata params are deprecated and passed None
        self.logger.debug("Received message on topic {}".format(message.topic))
        try:
            payload = json.loads(message.payload.decode())
        except json_decode_error:
            payload = message.payload.decode()
        self.notify_signals([Signal({"payload": payload,
                                     "topic": message.topic})])
