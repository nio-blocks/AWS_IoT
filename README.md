Current state: this block is still a WIP. Further research into greengrass
or further development of the greengrass platform is needed. In the current
state, the subscribe block and the publish block work when pointed to
the AWS IoT cloud MQTT broker, but no connection can be established/authenticated
for the local broker running on the greengrass core.

Instructions for setting up greengrass can be found [here.](http://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html)
And a blog post about using lambda with it can be found [here.](https://aws.amazon.com/blogs/aws/aws-greengrass-run-aws-lambda-functions-on-connected-devices/)


Greengrass
==========

Blocks to interact with a greengrass core.

Dependencies
----------------
AWSIoTPythonSDK

GreengrassSubscribe
===================
Subscribe to topics in greengrass's MQTT pub/sub system and notify them.

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
- **mqtt_host**(string): Host location for the greengrass core
- **mqtt_port**(integer): Port for the greengrass core

Commands
----------------
None

Input
-------
Messages from an MQTT topic.

Output
---------
The same message and any associated info


GreengrassPublish
=================
Publish signals to greengrass's MQTT pub/sub system.

Properties
--------------
Same as GreenGrassSubscribe, except the `topic` property is a publisher topic

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Same list of signals as input, but published to MQTT.


GreengrassShadowDelete
======================
Delete a property from a devices shadow.

Properties
--------------
Same as GreengrassSubscribe, with the following additional properties:
- **data_to_delete**(expression): A dictionary structure that defines
the property on the shadow you wish to delete.
- **thing_name**(string): The thing ARN of the device you which to change
- **persistent_subscribe**(boolean): whether to persistently subscribe to the device in question

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Results of the shadow deletions.


GreengrassShadowUpdate
======================
Update a property of a devices shadow.

Properties
--------------
Same as GreengrassShadowDelete, replacing data_to_delete with:
- **data_to_update**(expression): A dictionary structure that defines the property
on the shadow you wish to update

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Results of the shadow updates.


GreengrassShadowDeltaListener
=============================
Listens to a device shadow for deltas/changes.

Properties
--------------
Same as GreengrassShadowDelete, minus the data_to_delete property.

Commands
----------------
None

Input
-------
Any list of signals.

Output
---------
Any deltas to the given device's shadow.
