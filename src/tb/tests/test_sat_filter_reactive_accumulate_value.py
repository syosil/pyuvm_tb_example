import pyuvm
import vsc

from pyuvm import uvm_factory

from sat_filter_tb_base_test import sat_filter_tb_base_test
from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from vseqs.sat_filter_default_seq import sat_filter_default_seq

# Default values
_TIMEOUT_TIME = 1000
_TIMEOUT_UNIT = 'ns'

_MAX_ACC_VALUE_ = 100

# ---------------------------------------------------------------------------------------------
# Launch default sequences until the sum of the response 'data' is higher than 'data_adder_max'.
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_sat_filter_default_accumulate_seq(sat_filter_tb_base_test):
    """ Test that launches sequences until the sum of the response 'data' is higher than 'data_adder_max'.
    """

    def __init__(self, name="test_sat_filter_default_accumulate_seq", parent=None):

        super().__init__(name, parent)

        self.data_adder_max = _MAX_ACC_VALUE_ #vsc.rand_uint32_t()
        self.data_adder = 0

    def start_of_simulation_phase(self):

        super().start_of_simulation_phase()
        uvm_factory().set_type_override_by_type(sat_filter_tb_base_seq, sat_filter_default_seq)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.__class__.__name__}>")

        self.raise_objection()

        await super().run_phase()

        # TODO: Randomize the maximum value of the accumulator

        self.logger.info(f"{'-'*30} Running test until accumulated value is <{self.data_adder_max}>")

        while True:

            # Start sequence
            await (self.virt_sequence.start(self.tb_env.virtual_sequencer))

            # Add 'rsp.data' to the previous value
            self.data_adder += self.virt_sequence.consumer_seq.rsp.data

            self.logger.debug(f"Adder: {self.data_adder}, rsp: {self.virt_sequence.consumer_seq.rsp}")

            if (self.data_adder >= self.data_adder_max):
                break

        self.drop_objection()

        self.logger.info(f"{'-'*30} Accumulated value was <{self.data_adder}>")
        self.logger.info(f"{'-'*30} END of 'run_phase' of <{self.__class__.__name__}>")
