import pyuvm

from pyuvm import uvm_factory

from sat_filter_tb_base_test import sat_filter_tb_base_test
from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from vseqs.sat_filter_default_seq import sat_filter_default_seq

# Default values
_TIMEOUT_TIME = 1000
_TIMEOUT_UNIT = 'ns'

# ---------------------------------------------------------------------------------------------
# Test running default sequence. (bringup_test)
# - Start 5 default_sequences
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_sat_filter_default_seq(sat_filter_tb_base_test):
    """ Test running default sequence for the SSDT-UVC.
    """

    def __init__(self, name="test_ssdt_b2b_default_seq", parent=None):

        super().__init__(name, parent)

    def start_of_simulation_phase(self):

        super().start_of_simulation_phase()
        uvm_factory().set_type_override_by_type(sat_filter_tb_base_seq, sat_filter_default_seq)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.get_name()}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        # Start sequences
        for _ in range(0,5):

            # Start sequence
            await (self.virt_sequence.start(self.tb_env.virtual_sequencer))

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")