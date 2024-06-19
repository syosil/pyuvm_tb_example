import cocotb
from cocotb.triggers import Combine

from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from uvc.ssdt.src.uvc_ssdt_sequence_lib import uvc_ssdt_default_seq

# ------------------------------------------------------------------------------------------
# Default virtual sequence for the Saturation Filter:
# - Launch a single default SSDT sequence on the producer and consumer.
# ------------------------------------------------------------------------------------------
class sat_filter_default_seq(sat_filter_tb_base_seq):
    """ Default sequence for the Saturation Filter TB.
    - Start 2 default SSDT sequences in parallel.
    """

    def __init__(self, name="sat_filter_default_seq"):

        super().__init__(name)

        # Create sequences
        self.producer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_cons_seq")

    async def body(self):

        # Launch sequences
        await super().body()

        prod_task = cocotb.start_soon(self.producer_seq.start(self.sequencer.ssdt_producer_sequencer))
        cons_task = cocotb.start_soon(self.consumer_seq.start(self.sequencer.ssdt_consumer_sequencer))

        # Finishes when the both tasks finishes
        await Combine(prod_task, cons_task)