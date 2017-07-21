from unittest.mock import patch

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
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTSubscribe(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTSubscribe()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {"topic": "testtopic"})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTPublish(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTPublish()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {"topic": "testtopic"})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowBase(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTShadowBase()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowUpdate(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowUpdate()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowDelete(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowDelete()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)


class TestMQTTShadowDeltaListener(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowDeltaListener()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
        self.assert_num_signals_notified(0)
