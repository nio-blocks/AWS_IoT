import json
from nio.properties import VersionProperty, StringProperty, Property
from nio import TerminatorBlock
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from AWSIoTPythonSDK.exception import AWSIoTExceptions
from .aws_iot_mqtt_base_block import AWSIoTMQTTBase


class AWSIoTUpdateShadow(AWSIoTMQTTBase, TerminatorBlock):
    """Update a device's shadow document with a reported state."""

    version = VersionProperty("1.0.1")
    thing_name = StringProperty(title='Thing Name')
    reported_state = Property(
        title='Reported State', default='{{ $.to_dict() }}')

    def __init__(self):
        super().__init__()
        self.client = AWSIoTMQTTShadowClient
        self.shadow = None

    def configure(self, context):
        super().configure(context)
        self.shadow = self.client.createShadowHandlerWithName(
            self.thing_name(), isPersistentSubscribe=True)

    def process_signals(self, signals):
        for signal in signals:
            payload = json.dumps(
                {'state': {'reported': self.reported_state(signal)}})
            try:
                token = self.shadow.shadowUpdate(payload, self._callback, 5)
                self.logger.debug(
                    'Updating shadow, token {}, payload: {}'.format(
                        token, payload))
            except AWSIoTExceptions.publishQueueDisabledException:
                self.logger.exception(
                    'Client is disconnected, '
                    'dropping signal with payload {}'.format(payload))

    def configure_connection(self):
        # override inhereted method, contains invalid config calls
        # for this client
        self.client.configureConnectDisconnectTimeout(self.connect_timeout())
        self.client.configureMQTTOperationTimeout(5)
        self.client.configureAutoReconnectBackoffTime(1, 32, 20)

    def _callback(self, payload, responseStatus, token):
        if responseStatus == 'accepted':
            self.logger.debug('{} Update accepted'.format(token))
        else:
            self.logger.error(
                '{} Update returned status \'{}\', payload: {}'.format(
                    token, responseStatus, payload))
