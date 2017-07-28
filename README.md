AWS IoT
=======

Blocks to interact with AWS IoT's cloud broker.

Dependencies
----------------
AWSIoTPythonSDK

AWSIoTSubscribe
===============
Subscribe to topics in AWS IoT's MQTT pub/sub system and notify them.

Properties
--------------
- **topic**(string): MQTT topic to subscribe to
- **AWS Access Key ID**(string): AWS access key ID for your AWS account
- **AWS Secret Key**(string): AWS secret key for your AWS account
- **root_ca_path**(string): Path to AWS IoT Root CA
- **cert_path**(string):
- **private_key_path**(string):
- **use_websocket**(bool, hidden): Whether to use websockets. If this is set to `True`, the port used will likely be `443`
- **connect_timeout**(integer): How long to wait before considering a connection attempt invalid
- **mqtt_host**(string): Host location for the broker
- **mqtt_port**(integer): Port for the broker

Commands
----------------
None

Input
-------
Messages from an MQTT topic.

Output
---------
The same message and any associated info


AWSIoTPublish
=============
Publish signals to AWS IoT's MQTT pub/sub system.

Properties
--------------
Same as AWSIoTSubscribe, except the `topic` property is a publisher topic

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Same list of signals as input, but published to MQTT.
