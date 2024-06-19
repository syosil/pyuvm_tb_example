import vsc
import cocotb

from cocotb.triggers import ReadOnly, NextTimeStep, First
from pyuvm import uvm_root

from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from uvc.ssdt.src.uvc_ssdt_sequence_lib import uvc_ssdt_default_seq

# ------------------------------------------------------------------------------------------
# Sequence that is always launching sequences on each agent, but finishes when
# the accumulated value 'data' of the consumer responses reaches a maximum defined.
# ------------------------------------------------------------------------------------------
@vsc.randobj
class sat_filter_inf_accumulate_seq(sat_filter_tb_base_seq):
    """ Launch a random number of sequences for each agent.
    """

    def __init__(self, name="sat_filter_inf_accumulate_seq"):

        super().__init__(name)

        # Create sequences
        self.producer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_cons_seq")

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
