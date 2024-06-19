import vsc
import pyuvm

from pyuvm import uvm_factory

from sat_filter_tb_base_test import sat_filter_tb_base_test
from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from vseqs.sat_filter_default_seq import sat_filter_default_seq

# Default values
_TIMEOUT_TIME = 5000
_TIMEOUT_UNIT = 'ns'

_SEQS_N_NUMBER_ = 50     # Change this value

# ---------------------------------------------------------------------------------------------
# Test launching 'N' number of sequences w/ inline constraint.
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_sat_filter_rand_n_seq(sat_filter_tb_base_test):
    """ Test that launches 'N' number of random sequences using inline constraint.
    """

    def __init__(self, name="test_sat_filter_rand_n_seq", parent=None):

        super().__init__(name, parent)

        self.number_of_seqs = _SEQS_N_NUMBER_ #vsc.rand_uint32_t()
        self.seq_counter = 0

    def start_of_simulation_phase(self):

        super().start_of_simulation_phase()
        uvm_factory().set_type_override_by_type(sat_filter_tb_base_seq, sat_filter_default_seq)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.__class__.__name__}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        # TODO: Randomize number of seq. items

        while True:

            # Start sequence
            await (self.virt_sequence.start(self.tb_env.virtual_sequencer))

            # Count sequences
            self.seq_counter += 1

            self.logger.debug(f"Seq nr. {self.seq_counter}, rsp: {self.virt_sequence.consumer_seq.rsp}")

            if (self.seq_counter >= self.number_of_seqs):
                break

        self.logger.info(f"Number of sequences = {self.number_of_seqs}")

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")
