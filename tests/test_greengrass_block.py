from unittest.mock import patch

from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal

from ..greengrass_mqtt_base_block import GreenGrassMQTTBase
from ..greengrass_mqtt_subscribe_block import GreenGrassMQTTSubscribe
from ..greengrass_mqtt_publish_block import GreenGrassMQTTPublish
from ..greengrass_shadow_base_block import GreenGrassMQTTShadowBase
from ..greengrass_shadow_update_block import GreenGrassShadowUpdate
from ..greengrass_shadow_delete_block import GreenGrassShadowDelete
from ..greengrass_shadow_delta_listener_block import GreenGrassShadowDeltaListener


class TestMQTTBase(NIOBlockTestCase):

    def test_configure(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTBase()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
            self.assertEqual(patched_client.return_value.connect.call_count, 1)

        self.assert_num_signals_notified(0)


class TestMQTTSubscribe(NIOBlockTestCase):

    def test_subscribe(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTSubscribe()

        class Message:
            def __init__(self, payload):
                self.payload = payload
                self.topic = blk.topic()

        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {"topic": "testtopic"})
            blk.start()
            blk._handle_message(client="", userdata="",
                               message=Message(payload="test message"))
            blk.stop()
            patched_client.return_value.subscribe.assert_called_with(
                topic=blk.topic(),
                QoS=0,
                callback=blk._handle_message
            )
            patched_client.return_value.unsubscribe.assert_called_with(
                blk.topic()
            )
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"client": "",
             "userdata": "",
             "payload": "test message",
             "topic": blk.topic()})


class TestMQTTPublish(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTPublish()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {"topic": "testtopic"})
            blk.start()
            blk.process_signals([Signal({"text": "hello"})])
            blk.stop()
            patched_client.return_value.publish.assert_called_with(
                topic=blk.topic(),
                QoS=0,
                payload=blk.data_to_publish(Signal({"text": "hello"}))
            )

        self.assert_num_signals_notified(0)


class TestMQTTShadowBase(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassMQTTShadowBase()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
            patched_client.return_value.createShadowHandlerWithName.\
                assert_called_with(blk.thing_name(),
                                   isPersistentSubscribe=blk.persistent_subscribe())
        self.assert_num_signals_notified(0)


class TestMQTTShadowUpdate(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowUpdate()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            patched_client.return_value.createShadowHandlerWithName.\
                return_value.shadowUpdate.return_value = {
                "response": "success"
            }
            blk.process_signals([Signal({"test": 1})])
            blk.stop()
            patched_client.return_value.createShadowHandlerWithName. \
                return_value.shadowUpdate.assert_called_with(
                    blk.data_to_update(Signal({"test": 1})),
                    blk._update_callback,
                    srcTimeout=5
            )

        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"response": "success"})


class TestMQTTShadowDelete(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = GreenGrassShadowDelete()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            patched_client.return_value.createShadowHandlerWithName.\
                return_value.shadowDelete.return_value = {
                "response": "success"
            }
            blk.process_signals([Signal({"test": 1})])
            blk.stop()
            patched_client.return_value.createShadowHandlerWithName. \
                return_value.shadowDelete.assert_called_with(
                    blk.data_to_delete(Signal({"test": 1})),
                    blk._delete_callback,
                    srcTimeout=5
            )

        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"response": "success"})


class TestMQTTShadowDeltaListener(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        import json
        blk = GreenGrassShadowDeltaListener()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk._delta_callback(
                payload=json.dumps({"state": {"property": "test_property"},
                                    "version": 1}),
                responseStatus=200,
                token="")
            blk.stop()
            patched_client.return_value.createShadowHandlerWithName. \
                return_value.shadowRegisterDeltaCallback.assert_called_with(
                blk._delta_callback
            )
            patched_client.return_value.createShadowHandlerWithName. \
                return_value.shadowUnregisterDeltaCallback.assert_called_with(
                blk._delta_callback
            )
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'state': {'property': 'test_property'}, 'version': 1})
