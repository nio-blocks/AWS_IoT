from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from uuid import uuid4
from copy import deepcopy

from nio.properties import (StringProperty, PropertyHolder,
                            ObjectProperty, FileProperty, BoolProperty,
                            IntProperty)
from nio.util.discovery import not_discoverable


class AuthCreds(PropertyHolder):
    access_key_id = StringProperty(title="Access Key ID", default="",
                                   allow_none=True)
    secret_key = StringProperty(title="Secret Key", default="",
                                allow_none=True)


@not_discoverable
class AWSIoTMQTTBase(object):
    """The base block for AWS IoT. This block is responsible for connecting
    to the cloud broker via MQTT."""

    creds = ObjectProperty(AuthCreds, title="AWS Credentials",
                           default=AuthCreds())
    root_ca_path = FileProperty(title="IoT Root CA Location",
                                default="[[PROJECT_ROOT]]/etc/root_ca.pem")
    cert_path = FileProperty(title="Certificate Path",
                             default="[[PROJECT_ROOT]]/etc/cert.pem")
    private_key_path = FileProperty(
        title="Private Key Path",
        default="[[PROJECT_ROOT]]/etc/private_key.pem")
    use_websocket = BoolProperty(title="Use Websockets", default=False,
                                 visible=False)
    connect_timeout = IntProperty(title="Connect/Disconnect Timeout",
                                  default=10)
    mqtt_host = StringProperty(title="MQTT Host", default="127.0.0.1")
    mqtt_port = IntProperty(title="MQTT Port", default=8883)

    def __init__(self):
        self.client = deepcopy(AWSIoTMQTTClient)
        super().__init__()

    def configure(self, context):
        """set up MQTT client properties"""
        super().configure(context)

        self.client = self.client(str(uuid4()),
                                  useWebsocket=self.use_websocket())
        self.client.configureEndpoint(hostName=self.mqtt_host(),
                                      portNumber=self.mqtt_port())

        if self.use_websocket():
            # only need to configure the root CA and IAM credentials for
            # websockets
            self.client.configureIAMCredentials(self.creds().access_key_id(),
                                                self.creds().secret_key())
            self.client.configureCredentials(
                CAFilePath=self.root_ca_path().file)
        else:
            # don't need to configure IAM credentials for non-websocket use
            self.client.configureCredentials(
                CAFilePath=self.root_ca_path().file,
                KeyPath=self.private_key_path().file,
                CertificatePath=self.cert_path().file)

        self.client.configureOfflinePublishQueueing(queueSize=-1)
        self.client.configureConnectDisconnectTimeout(self.connect_timeout())
        self.client.configureDrainingFrequency(2)
        self.client.configureMQTTOperationTimeout(5)
        self.client.configureAutoReconnectBackoffTime(1, 32, 20)

        self.connect()

    def stop(self):
        self.disconnect()
        super().stop()

    def connect(self):
        self.logger.debug("Connecting...")
        self.client.connect()

    def disconnect(self):
        self.logger.debug("Disconnecting...")
        self.client.disconnect()
