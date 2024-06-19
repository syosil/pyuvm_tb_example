""" Saturation Filter Scoreboard
- Verification component that contains checkers and verifies the functionality of the design.
- Receives transaction level objects captured from the interfaces of a DUT via TLM Analysis Ports.
- Includes the Reference Model.
"""

import cocotb
from pyuvm import uvm_scoreboard, uvm_analysis_port, uvm_tlm_analysis_fifo
from cocotb.queue import Queue


class sat_filter_scoreboard(uvm_scoreboard):
    """ Scoreboard for Saturation Filter. """

    def __init__(self, name="sat_filter_scoreboard", parent=None):

        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None

        self.analysis_port = None   # Analysis Port handler

        # FIFO for connecting to UVC's ap
        self.uvc_ssdt_consumer_fifo = None
        self.ref_model_fifo = None

        # recording number of successes and failures
        self.succes = 0
        self.failure = 0

    def build_phase(self):

        super().build_phase()

        # Instantiate configuration object
        self.cfg = self.cdb_get("cfg", "")
        self.logger.debug(f" Config of < {self.get_name()} > is {(self.cfg.__getattribute__)}")

        # Instantiate the analysis port
        self.analysis_port = uvm_analysis_port(f"{self.get_name()}_analysis_port", self)

        # Create the analysis FIFOs
        self.uvc_ssdt_consumer_fifo = uvm_tlm_analysis_fifo("uvc_ssdt_consumer_fifo", self)
        self.ref_model_fifo = uvm_tlm_analysis_fifo("ref_model_fifo", self)

        # Queues to store output of Ref. Model
        self.uvc_ssdt_consumer_queue = Queue(maxsize=1)
        self.ref_model_queue = Queue(maxsize=1)

    async def run_phase(self):
        """
        - Get the item from the FIFOs
        - Compare the samples received
        """

        await super().run_phase()

        cocotb.start_soon(self.sample_ap_uvc(self.uvc_ssdt_consumer_fifo, self.uvc_ssdt_consumer_queue))
        cocotb.start_soon(self.sample_ap_uvc(self.ref_model_fifo, self.ref_model_queue))

        while True:

            # Get items from queues
            self.uvc_ssdt_consumer_item = await self.uvc_ssdt_consumer_queue.get()
            self.ref_model_item = await self.ref_model_queue.get()

            # Print items as they arrive (only in DEBUG level)
            self.print_scb()

            # compare items and update result
            if (self.uvc_ssdt_consumer_item == self.ref_model_item):
                self.succes += 1
                self.logger.info(f"Items are identical: {self.uvc_ssdt_consumer_item}")
            else:
                self.logger.error(f"Items not identical: \n \
                    {self.uvc_ssdt_consumer_item}, \n \
                    {self.ref_model_item}")
                self.failure += 1

    # Report the results of the comparisons
    def check_phase(self):

        super().check_phase()

        self.logger.info(f"Scoreboard found {self.succes} successes and {self.failure} failures")
        assert self.failure == 0, f"the test found {self.failure} failed comparisons"

    async def sample_ap_uvc(self, fifo, queue):
        """ Copy FIFO content to internal queues.
        """
        while True:
            item = await fifo.get()
            item.set_name(fifo.get_name())

            await queue.put(item)
            self.logger.debug(f"sample_ap_uvc : {item} |")

    def print_scb(self):
        """ Print queue items.
        """
        self.logger.debug(f"{'-'*35}")
        self.logger.debug(" | Consumer |   Ref    |")
        self.logger.debug(f" |   {self.uvc_ssdt_consumer_item.data:4d}   |   {self.ref_model_item.data:4d}")
        self.logger.debug(f"{'-'*35}")
        self.logger.debug(f" \n \
                            | {self.uvc_ssdt_consumer_item}  |\n \
                            |         {self.ref_model_item}  |")
        self.logger.debug(f"{'-'*35}")

