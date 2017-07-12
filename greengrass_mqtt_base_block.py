from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

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
    root_ca_path = FileProperty(title="IoT Root CA Location",
                                default="/etc/root_ca.pem")
    cert_path = FileProperty(title="Certificate Path",
                             default="/etc/cert.pem")
    private_key_path = FileProperty(title="Private Key Path",
                                    default="/etc/private_key.pem")
    client_id = StringProperty(title="Client ID", default="")
    use_websocket = BoolProperty(title="Use Websockets", default=False,
                                 visible=False)
    connect_timeout = IntProperty(title="Connect/Disconnect Timeout",
                                  default=60)
    mqtt_host = StringProperty(title="MQTT Host", default="127.0.0.1")
    mqtt_port = IntProperty(title="MQTT Port", default=8883)

    def __init__(self):
        self.client = AWSIoTMQTTClient
        super().__init__()

    def configure(self, context):
        """set up MQTT client properties"""
        self.client(self.client_id(), useWebsocket=self.use_websocket())
        self.client.configureEndpoint(self.mqtt_host(), self.mqtt_port())
        self.client.configureOfflinePublishQueueing(queueSize=-1)
        self.client.configureConnectDisconnectTimeout(self.connect_timeout())
        self.client.configureCredentials(CAFilePath=self.root_ca_path(),
                                         KeyPath=self.private_key_path(),
                                         CertificatePath=self.cert_path())
        self.connect()
        super().configure(context)

    def stop(self):
        self.disconnect()
        super().stop()

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()
