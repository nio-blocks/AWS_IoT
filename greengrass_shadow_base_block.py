from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

from nio.util.discovery import not_discoverable

from .greengrass_mqtt_base_block import GreenGrassMQTTBase


@not_discoverable
class GreenGrassMQTTShadowBase(GreenGrassMQTTBase):
    """The base block for Greengrass device shadows. This block is responsible
    for connecting to the local greengrass core via MQTT and interacting with
    device shadows for devices in the local greengrass core."""

    def configure(self, context):
        self.client = AWSIoTMQTTShadowClient(self.client_id(),
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

        self.client.configureConnectDisconnectTimeout(self.connect_timeout())
        self.client.configureMQTTOperationTimeout(5)
        self.client.configureAutoReconnectBackoffTime(1, 32, 20)

        self.connect()
