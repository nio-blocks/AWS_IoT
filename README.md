AWSIoTMQTTPublish
=================
Blocks to interact with AWS IoT's cloud broker.

Properties
----------
- **cert_path**: Path to file containing certifications.
- **connect_timeout**: How long to wait before considering a connection attempt invalid.
- **creds**: AWS access credentials.
- **data_to_publish**: Message to send over an MQTT topic.
- **mqtt_host**: Host location for the broker.
- **mqtt_port**: Port for the broker.
- **private_key_path**: Path to file containing AWS private key
- **root_ca_path**: File path to AWS IoT Root CA.
- **topic**: MQTT topic to publish to.
- **use_websocket**: Whether to use websockets. If this is set to `True`, the port used will likely be `443`.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
AWSIoTPythonSDK


AWSIoTMQTTSubscribe
===================


Properties
----------
- **cert_path**: Path to file containing certifications.
- **connect_timeout**: How long to wait before considering a connection attempt invalid.
- **creds**: 
- **mqtt_host**: Host location for the broker.
- **mqtt_port**: Port for the broker.
- **private_key_path**: Path to file containing AWS private key
- **root_ca_path**: File path to AWS IoT Root CA.
- **topic**: MQTT topic to subscribe to.
- **use_websocket**: Whether to use websockets. If this is set to `True`, the port used will likely be `443`.

Inputs
------
None

Outputs
-------
- **default**: Messages received from an MQTT topic.

Commands
--------
None

Dependencies
------------
AWSIoTPythonSDK
