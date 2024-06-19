""" SSDT-UVC B2B virtual sequence library
"""

import cocotb
import vsc
from cocotb.triggers import Combine, ReadOnly, NextTimeStep, First
from pyuvm import uvm_sequence, uvm_root
from uvc.ssdt.src.uvc_ssdt_sequence_lib import uvc_ssdt_default_seq


# ------------------------------------------------------------------------------
# Base sequence class: Declaration of objects mainly.
# ------------------------------------------------------------------------------
class ssdt_b2b_base_seq(uvm_sequence):
    """ Base class for the SSDT B2B sequence.
    - Create a single sequence for the consumer and another for the producer.
    """

    def __init__(self, name="ssdt_b2b_base_seq"):

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

# ------------------------------------------------------------------------------------------
# Default virtual sequence for the SSDT B2B:
# - Launch a single default SSDT sequence on the producer and consumer.
# ------------------------------------------------------------------------------------------
class ssdt_b2b_default_seq(ssdt_b2b_base_seq):
    """ Default sequence for the SSDT-UVC B2B.
    - Start 2 default SSDT sequences in parallel.
    """

    def __init__(self, name="ssdt_b2b_default_seq"):

        super().__init__(name)

        # Create sequences
        self.producer_seq = uvc_ssdt_default_seq.create("ssdt_b2b_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("ssdt_b2b_cons_seq")

    async def body(self):

        # Launch sequences
        await super().body()

        prod_task = cocotb.start_soon(self.producer_seq.start(self.sequencer.ssdt_producer_sequencer))
        cons_task = cocotb.start_soon(self.consumer_seq.start(self.sequencer.ssdt_consumer_sequencer))

        # Finishes when the both tasks finishes
        await Combine(prod_task, cons_task)

# ------------------------------------------------------------------------------------------
# Sequence that launches a random number of sequences on each agent
# ------------------------------------------------------------------------------------------
@vsc.randobj
class ssdt_b2b_rand_size_seq(ssdt_b2b_base_seq):
    """ Launch a random number of sequences on each agent.
    """

    def __init__(self, name="ssdt_b2b_rand_size_seq"):

        super().__init__(name)

        # Create sequences
        self.producer_seq = uvc_ssdt_default_seq.create("ssdt_b2b_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("ssdt_b2b_cons_seq")

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


# ------------------------------------------------------------------------------------------
# Sequence that is always launching sequences on each agent, but finishes when
# the accumulated value 'data' of the consumer responses reaches a maximum defined.
# ------------------------------------------------------------------------------------------
@vsc.randobj
class ssdt_b2b_inf_accumulate_seq(ssdt_b2b_base_seq):
    """ Launch a random number of sequences for each agent.
    """

    def __init__(self, name="ssdt_b2b_rand_size_seq"):

        super().__init__(name)

        # Create sequences
        self.producer_seq = uvc_ssdt_default_seq.create("ssdt_b2b_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("ssdt_b2b_cons_seq")

        self.data_adder_max = vsc.rand_uint32_t()
        self.data_adder = 0

        # Controls the loop launching the tasks
        self.main_loop_flag = True

    async def body(self):

        # Launch sequences
        await super().body()

        uvm_root().logger.info(f"{'-'*30} Max. value of the accumulator = {self.data_adder_max} {'-'*30}")

        # Launch tasks
        prod_task = await cocotb.start(self.producer_seq.start(self.sequencer.ssdt_producer_sequencer))
        cons_task = await cocotb.start(self.consumer_seq.start(self.sequencer.ssdt_consumer_sequencer))
        cons_mon_task = await cocotb.start(self.monitor_consumer_rsp(cons_task))

        # Just for debug
        prod_task_cnt = 1
        cons_task_cnt = 1
        cons_mon_task_cnt = 1

        # Main loop
        while self.main_loop_flag:

            # Launch producer task if stopped
            if prod_task.done():
                prod_task_cnt += 1
                uvm_root().logger.debug(f"{'-'*30} Launch producer sequence task #{prod_task_cnt} {'-'*30}")
                prod_task = await cocotb.start(self.producer_seq.start(self.sequencer.ssdt_producer_sequencer))

            # Launch consumer task if stopped
            if cons_task.done():
                cons_task_cnt += 1
                uvm_root().logger.debug(f"{'-'*30} Launch consumer sequence task #{prod_task_cnt} {'-'*30}")
                cons_task = await cocotb.start(self.consumer_seq.start(self.sequencer.ssdt_consumer_sequencer))

            # Launch monitor task if stopped
            if cons_mon_task.done():
                cons_mon_task_cnt += 1
                uvm_root().logger.debug(f"{'-'*30} Launch consumer monitor task #{cons_mon_task_cnt} {'-'*30}")
                cons_mon_task = await cocotb.start(self.monitor_consumer_rsp(cons_task))

            # Await for any to finish
            await First(prod_task, cons_task)

    async def monitor_consumer_rsp(self, task):
        """ Method that updates de accumulated value whenever the consumer task finishes.
        Stops sequence when reaches to the maximum value.
        """

        # Wait for task to finish
        while not task.done():
            await ReadOnly()
            await NextTimeStep()

        uvm_root().logger.info(f"{self.get_full_name()} | Adder: {self.data_adder}, Resp: {self.consumer_seq.rsp}\n")
        self.data_adder += self.consumer_seq.rsp.data

        if self.data_adder >= self.data_adder_max:
            self.main_loop_flag = False

