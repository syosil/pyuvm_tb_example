""" SSDT-UVC sequence library

- The UVM Sequence is composed of several data items which can be put together in different ways to create different scenarios.
- They are executed by an assigned sequencer which then sends data items to the driver. Hence, sequences make up the core stimuli of any verification plan.
"""

from pyuvm import uvm_sequence, uvm_root
from .uvc_ssdt_seq_item import uvc_ssdt_seq_item


# ------------------------------------------------------------------------------
# Base sequence class.
# ------------------------------------------------------------------------------
class uvc_ssdt_base_seq(uvm_sequence):
    """ Base class for the SSDT sequence.
    """

    def __init__(self, name="ssdt_base_seq"):

        super().__init__(name)


        self.cfg = None                 # handle to configuration object
        self.seq_item = None            # sequence item
        self.rsp = None                 # sequence item reply
        self.seq_was_randomized = 0     # flag to check if sequence was already randomized

    async def body(self):
        """ This must be overwrite/updated by child.
        Note that the connection to the sequencer will be done on a 'uvm_test' class.
        """

        await super().body()

    def randomize(self):
        """ Randomize sequence.
        """

        if(self.seq_item == None):
            self.seq_item = uvc_ssdt_seq_item.create("uvc_ssdt_seq_item")

        self.seq_item.randomize()   # Randomize sequence item
        self.seq_was_randomized = 1

# ------------------------------------------------------------------------------
# Default sequence: creates and randomizes seq. item
# ------------------------------------------------------------------------------
class uvc_ssdt_default_seq(uvc_ssdt_base_seq):
    """ Default sequence for the SSDT-UVC.
        Sequence generating a single item: (data = rand(), valid = rand()).
    """

    def __init__(self, name="ssdt_default_seq"):

        super().__init__(name)

    async def body(self):

        await super().body()

        if not self.seq_was_randomized:
            self.seq_item = uvc_ssdt_seq_item.create("uvc_ssdt_seq_item")
            self.seq_item.randomize()   # Randomize sequence item

        uvm_root().logger.debug(f"Starting item ... {self.seq_item}")

        await self.start_item(self.seq_item)

        await self.finish_item(self.seq_item)

        uvm_root().logger.debug("Item finished...")

        uvm_root().logger.debug("Getting response...")
        self.rsp = await self.get_response()    # get response from driver of the seq. item

        uvm_root().logger.debug(f"Response got: {self.rsp}")