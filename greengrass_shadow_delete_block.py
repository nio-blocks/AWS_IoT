import json

from nio.properties import (VersionProperty, Property)
from nio.signal.base import Signal
from nio.util.discovery import discoverable

from .greengrass_shadow_base_block import GreenGrassMQTTShadowBase


@discoverable
class GreenGrassShadowDelete(GreenGrassMQTTShadowBase):
    """Delete device shadow properties on the local MQTT system"""

    version = VersionProperty('0.1.0')
    data_to_delete = Property(title="Data to delete",
                              default="{{ $.to_dict() }}",
                              allow_none=False)

    def _delete_callback(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            self.logger.debug("Delete request {} timed out".format(token))
        if responseStatus == "accepted":
            payload_dict = json.loads(payload)
            self.logger.debug("Delete request {} was accepted".format(token))
            return payload_dict
        if responseStatus == "rejected":
            self.logger.debug("Delete request {} was rejected".format(token))

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:
            result = self.shadow_handler.shadowDelete(
                self.data_to_delete(signal),
                self._delete_callback,
                srcTimeout=5
            )
            new_signals.append(Signal(result))
        self.notify_signals(new_signals)
