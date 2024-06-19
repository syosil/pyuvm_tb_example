from pyuvm import uvm_sequence, uvm_root

class sat_filter_tb_base_seq(uvm_sequence):
    """ Base sequence for the Saturation Filter's TB.
    - Create a single sequence for the consumer and another for the producer.
    """

    def __init__(self, name="sat_filter_base_seq"):

        super().__init__(name)

        self.cfg = None         # Declaration of configuration object handler
        self.sequencer = None   # Declaration of sequencer

        # Declaration of sequences for each agent
        self.producer_seq = None
        self.consumer_seq = None

    async def pre_body(self):

        if(self.sequencer is not None):
            uvm_root().logger.debug("Getting 'sequencer' from configDB")
            self.cfg = self.sequencer.cfg

    async def body(self):
        """ This must be overwrite/updated by the children class.
        Note that the connection to the sequencer will be done on a 'uvm_test' class.
        """

        await self.pre_body()