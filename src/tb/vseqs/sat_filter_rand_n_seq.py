import vsc
import cocotb

from cocotb.triggers import Combine
from pyuvm import uvm_root

from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from uvc.ssdt.src.uvc_ssdt_sequence_lib import uvc_ssdt_default_seq

# ------------------------------------------------------------------------------------------
# Sequence that launches a random number of sequences on each agent
# ------------------------------------------------------------------------------------------
@vsc.randobj
class sat_filter_rand_n_seq(sat_filter_tb_base_seq):
    """ Launch a random number of sequences on each agent.
    """

    def __init__(self, name="ssdt_b2b_rand_n_seq"):

        super().__init__(name)

        # Create sequences
        self.producer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_cons_seq")

        self.number_of_seqs = vsc.rand_uint32_t()

    async def body(self):

        # Launch sequences
        await super().body()

        uvm_root().logger.info(f"{'-'*30} Launching {self.number_of_seqs} sequences. {'-'*30}")

        prod_task = cocotb.start_soon(self.prod_transactions())
        cons_task = cocotb.start_soon(self.cons_transactions())

        # Finishes when all tasks finishes
        await Combine(prod_task, cons_task)

    async def prod_transactions(self):

        for _ in range(0, self.number_of_seqs):
            await self.producer_seq.start(self.sequencer.ssdt_producer_sequencer)

    async def cons_transactions(self):

        for _ in range(0, self.number_of_seqs):
            await self.consumer_seq.start(self.sequencer.ssdt_consumer_sequencer)

    @vsc.constraint
    def number_of_seqs_pos(self):
        self.number_of_seqs > 0
