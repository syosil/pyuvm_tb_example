import pyuvm

from pyuvm import uvm_factory

from sat_filter_tb_base_test import sat_filter_tb_base_test
from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from vseqs.sat_filter_rand_n_seq import sat_filter_rand_n_seq

# Default values
_TIMEOUT_TIME = 1000
_TIMEOUT_UNIT = 'ns'

_MAX_SEQS_NUMBER_ = 105   # You can change this value

# ---------------------------------------------------------------------------------------------
# Test launching the 'sat_filter_rand_n_seq' sequence
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_sat_filter_rand_n_seq(sat_filter_tb_base_test):
    """ Test that launches the 'sat_filter_rand_n_seq' sequence:
    - Randomize the sequence to set the number of tierations
    - Start the virtual sequence to generate the data traffic.
    """

    def __init__(self, name="test_sat_filter_sat_filter_rand_n_seq", parent=None):

        super().__init__(name, parent)

    def start_of_simulation_phase(self):

        super().start_of_simulation_phase()
        uvm_factory().set_type_override_by_type(sat_filter_tb_base_seq, sat_filter_rand_n_seq)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.__class__.__name__}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        # Randomize the maximum value of the accumulator
        with self.virt_sequence.randomize_with() as seq:
            seq.number_of_seqs == _MAX_SEQS_NUMBER_

        # Start sequence
        await (self.virt_sequence.start(self.tb_env.virtual_sequencer))

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")
