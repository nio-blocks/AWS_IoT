from unittest.mock import patch

from nio.block.terminals import DEFAULT_TERMINAL
from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal

from ..aws_iot_mqtt_base_block import AWSIoTMQTTBase
from ..aws_iot_mqtt_subscribe_block import AWSIoTMQTTSubscribe
from ..aws_iot_mqtt_publish_block import AWSIoTMQTTPublish


class TestMQTTBase(NIOBlockTestCase):

    def test_configure(self):
        """Signals pass through block unmodified."""
        blk = AWSIoTMQTTBase()
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
                self._client_id = "test id"

        with patch.object(blk, "client") as patched_client:
            self.configure_block(blk, {"topic": "testtopic"})
            message = Message(payload="test message")
            blk.start()
            blk._handle_message(client=message, userdata="",
                                message=message)
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
            {"client": message,
             "userdata": "",
             "payload": "test message",
             "topic": blk.topic()})


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
