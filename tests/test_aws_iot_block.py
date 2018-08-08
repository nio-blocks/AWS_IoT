import json
from unittest.mock import patch, MagicMock

from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal
from nio import Block

from ..aws_iot_mqtt_base_block import AWSIoTMQTTBase
from ..aws_iot_mqtt_subscribe_block import AWSIoTMQTTSubscribe
from ..aws_iot_mqtt_publish_block import AWSIoTMQTTPublish
from ..aws_iot_update_shadow_block import AWSIoTUpdateShadow


class TestMQTTBase(NIOBlockTestCase):

    def test_configure(self):
        """Signals pass through block unmodified."""

        class AWSIoTMQTT(AWSIoTMQTTBase, Block):
            pass

        blk = AWSIoTMQTT()
        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {})
            blk.start()
            blk.stop()
            self.assertEqual(patched_client.return_value.connect.call_count, 1)

        self.assert_num_signals_notified(0)


class TestMQTTSubscribe(NIOBlockTestCase):

    def test_subscribe(self):
        """Signals pass through block unmodified."""
        blk = AWSIoTMQTTSubscribe()

        class Message:
            def __init__(self, payload):
                self.payload = payload
                self.topic = blk.topic()

        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {"topic": "testtopic"})
            message = Message(payload="test message")
            blk.start()
            # first two args to callback are deprecated and passed None
            blk._handle_message(client=None, userdata=None, message=message)
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
            {"payload": "test message", "topic": blk.topic()})


class TestMQTTPublish(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = AWSIoTMQTTPublish()
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

class TestUpdateShadow(NIOBlockTestCase):

    thing_name = "SomeNeatThing"
    data = {"text": "hello"}

    def test_update(self):
        """ The device's shadow is updated with the reported state"""
        blk = AWSIoTUpdateShadow()
        with patch.object(blk, "client") as patched_client:
            test_client = patched_client.return_value
            test_shadow = test_client.createShadowHandlerWithName.return_value
            self.configure_block(blk, {"thing_name": self.thing_name})
            blk.start()
            blk.process_signals([Signal(self.data)])
            blk.stop()
            test_client.createShadowHandlerWithName.assert_called_once_with(
                self.thing_name, isPersistentSubscribe=True)
            test_client.configureOfflinePublishQueueing.assert_not_called()
            test_client.configureDrainingFrequency.assert_not_called()
            test_shadow.shadowUpdate.assert_called_once_with(
                json.dumps({'state': {'reported': self.data}}),
                blk._callback,
                5)

    def test_rejected_update(self):
        """ An update has been rejected and an error is logged"""
        status = 'rejected'
        token = 'abc-123'
        def dummy_update(payload, cb, to):
            blk._callback(payload, status, token)

        blk = AWSIoTUpdateShadow()
        with patch.object(blk, "client") as patched_client:
            test_client = patched_client.return_value
            test_shadow = test_client.createShadowHandlerWithName.return_value
            test_shadow.shadowUpdate.side_effect = dummy_update
            self.configure_block(blk, {"thing_name": self.thing_name})
            blk.logger = MagicMock()
            blk.start()
            blk.process_signals([Signal(self.data)])
            expected_payload = json.dumps(
                {'state': {'reported': self.data}})
            blk.logger.error.assert_called_once_with(
                '{} Update returned status \'{}\', payload: {}'.format(
                    token, status, expected_payload))
