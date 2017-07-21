from nio.testing.block_test_case import NIOBlockTestCase
from ..greengrass_mqtt_base_block import GreenGrassMQTTBase
from ..greengrass_mqtt_subscribe_block import GreenGrassMQTTSubscribe
from ..greengrass_mqtt_publish_block import GreenGrassMQTTPublish
from ..greengrass_shadow_base_block import GreenGrassMQTTShadowBase
from ..greengrass_shadow_update_block import GreenGrassShadowUpdate
from ..greengrass_shadow_delete_block import GreenGrassShadowDelete
from ..greengrass_shadow_delta_listener_block import GreenGrassShadowDeltaListener


class TestMQTTBase(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTBase()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTSubscribe(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTSubscribe()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTPublish(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTPublish()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowBase(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTShadowBase()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowUpdate(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowUpdate()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowDelete(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowDelete()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowDeltaListener(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowDeltaListener()
        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assert_num_signals_notified(0)
