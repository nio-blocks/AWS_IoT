import json

from nio.properties import VersionProperty, Property
from nio.signal.base import Signal
from nio.util.discovery import discoverable

from .greengrass_shadow_base_block import GreenGrassMQTTShadowBase


@discoverable
class GreenGrassShadowUpdate(GreenGrassMQTTShadowBase):
    """Update device shadows on the local MQTT system"""

    version = VersionProperty('0.1.0')
    data_to_update = Property(title="Data to update",
                              default="{{ $.to_dict() }}",
                              allow_none=False)

    def _update_callback(self, payload, responseStatus, token):
        if responseStatus == "timeout":
            self.logger.debug("Update request {} timed out".format(token))
        if responseStatus == "accepted":
            payload_dict = json.loads(payload)
            self.logger.debug("Update request {} was accepted".format(token))
            return payload_dict
        if responseStatus == "rejected":
            self.logger.debug("Update request {} was rejected".format(token))

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:
            result = self.shadow_handler.shadowUpdate(self.data_to_update(signal),
                                                      self._update_callback,
                                                      srcTimeout=5)
            new_signals.append(Signal(result))
        self.notify_signals(new_signals)
