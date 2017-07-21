import json

from nio.util.discovery import discoverable
from nio.properties import (VersionProperty, StringProperty, BoolProperty,
                            Property)
from nio.signal.base import Signal

from .greengrass_shadow_base_block import GreenGrassMQTTShadowBase


@discoverable
class GreenGrassShadowDelete(GreenGrassMQTTShadowBase):
    """Delete device shadow properties on the local MQTT system"""

    version = VersionProperty('1.0.0')
    thing_name = StringProperty(title="Thing name", default="",
                                allow_none=False)
    persistent_subscribe = BoolProperty(title="Persistent Subscription",
                                        default=True)
    data_to_delete = Property(title="Data to delete",
                              default="{{ $.to_dict() }}",
                              allow_none=False)

    def __init__(self):
        super().__init__()
        self.shadow_handler = None

    def configure(self, context):
        super().configure(context)
        self.shadow_handler = self.client.createShadowHandlerWithName(
            self.thing_name(),
            isPersistentSubscribe=self.persistent_subscribe())

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
            result = self.shadow_handler.shadowDelete(self.data_to_update(signal),
                                                      self._update_callback,
                                                      srcTimeout=5)
            new_signals.append(Signal(result))
        self.notify_signals(new_signals)
