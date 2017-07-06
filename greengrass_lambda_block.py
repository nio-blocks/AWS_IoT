from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, Property
from aws_greengrass_core_sdk.sdk import greengrasssdk


class GreenGrassLambda(Block):

    version = VersionProperty('0.1.0')
    invocation_type = StringProperty(title='Invocation Type',
                                     default='RequestResponse')
    function_name = StringProperty(title='Function Name',
                                   allow_none=False)
    function_version = StringProperty(title='Function Version',
                                      allow_none=True)
    client_context = StringProperty(title='Client Context',
                                    default='1')
    payload = Property(title="Json Payload")

    def __init__(self):
        self.client = None
        super().__init__()

    def configure(self):
        self.client = greengrasssdk.client('lambda')

        # check that payload is json format


        super().configure()

    def process_signals(self, signals):
        for signal in signals:
            response = self.client.invoke(
                FunctionName=self.function_name(),
                InvocationType=self.invocation_type(),
                ClientContext=self.client_context(),
                Payload=self.payload(),
                Qualifier=self.client_context())

            

        self.notify_signals(signals)
