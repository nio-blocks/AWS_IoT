from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, AWSIoTMQTTShadowClient

from nio.block.base import Block
from nio.properties import (VersionProperty, StringProperty, PropertyHolder,
                            ObjectProperty, FileProperty, BoolProperty,
                            IntProperty)
from nio.util.discovery import not_discoverable


class AuthCreds(PropertyHolder):
    username = StringProperty(title="Access Key ID", default="", allow_none=True)
    password = StringProperty(title="Secret Key", default="", allow_none=True)


@not_discoverable
class GreenGrassMQTTBase(Block):
    """The base block for Greengrass. This block is responsible for connecting
    to the local greengrass core via MQTT."""

    version = VersionProperty('1.0.0')
    creds = ObjectProperty(AuthCreds, title="AWS Credentials", default=AuthCreds())
    certificate = FileProperty(title="IoT Root CA Location",
                               default="/etc/root_ca.pem")
    client_id = StringProperty(title="Client ID", default="")
    use_websocket = BoolProperty(title="Use Websockets", default=True,
                                 visible=False)
    connect_timeout = IntProperty(title="Connect/Disconnect Timeout",
                                  default=60)

    def __init__(self):
        self.client = None
        super().__init__()

    def configure(self):
        """set up MQTT client properties"""
        self.client = AWSIoTMQTTClient(self.client_id(),
                                       useWebsocket=self.use_websocket())
        self.client.configureOfflinePublishQueueing(-1)
        self.client.configureConnectDisconnectTimeout(self.connect_timeout())

        self.connect()
        super().configure()

    def stop(self):
        self.disconnect()

    def process_signals(self, signals):
        for signal in signals:
            pass
        self.notify_signals(signals)

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()
