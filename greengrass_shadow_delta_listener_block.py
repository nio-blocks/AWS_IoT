import json

from nio.properties import VersionProperty
from nio.signal.base import Signal
from nio.util.discovery import discoverable

from .greengrass_shadow_base_block import GreenGrassMQTTShadowBase


@discoverable
class GreenGrassShadowDeltaListener(GreenGrassMQTTShadowBase):
    """Listens for changes to device shadows in the local greengrass"""

    version = VersionProperty('0.1.0')

    def configure(self, context):
        super().configure(context)
        self.shadow_handler.shadowRegisterDeltaCallback(self._delta_callback)

    def stop(self):
        self.shadow_handler.shadowUnregisterDeltaCallback(self._delta_callback)
        super().stop()

    def _delta_callback(self, payload, responseStatus, token):
        self.logger.debug("Got responseStatus `{}` from token `{}`"
                          .format(responseStatus, token))
        payloadDict = json.loads(payload)
        self.logger.debug("property: " + str(payloadDict["state"]["property"]))
        self.logger.debug("version: " + str(payloadDict["version"]))

        self.notify_signals([Signal(payloadDict)])
