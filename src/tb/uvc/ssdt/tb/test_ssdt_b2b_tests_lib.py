""" Test library for the SSDT-UVC B2B.
"""


import pyuvm
from pyuvm import uvm_factory
from cocotb.triggers import RisingEdge
from uvc.ssdt.tb.ssdt_b2b_base_test import ssdt_b2b_base_test
from uvc.ssdt.tb.ssdt_b2b_sequence_lib import *


# Default values
_TIMEOUT_TIME = 1000
_TIMEOUT_UNIT = 'ns'


# ---------------------------------------------------------------------------------------------
# Base test setup.
# ---------------------------------------------------------------------------------------------
class test_ssdt_b2b_base_setup(ssdt_b2b_base_test):
    """ Base test class.
    0. Reset all input signals.
    1. Wait 1clk cycle.
    2. Reset for 2clk cycles.
    3. Wait 1clk cycle.
    4. Start 10 sequences.
    """

    def __init__(self, name="test_ssdt_b2b_base_test", parent=None):

        super().__init__(name, parent)

    async def run_phase(self):

        await super().run_phase()

        # Clean inputs
        self.dut.in_data.value = 0
        self.dut.in_valid.value = 0

        self.logger.debug(f"Resetting DUT...")

        await RisingEdge(self.dut.clk)
        self.dut.rst.value = 1

        await RisingEdge(self.dut.clk)
        await RisingEdge(self.dut.clk)
        self.dut.rst.value = 0

        self.logger.debug(f"Resetting DONE.")


# ---------------------------------------------------------------------------------------------
# Test running default sequence. (bringup_test)
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_ssdt_b2b_default_seq(test_ssdt_b2b_base_setup):
    """ Test running default sequence for the SSDT-UVC.
    """

    def __init__(self, name="test_ssdt_b2b_default_seq", parent=None):

        super().__init__(name, parent)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.get_name()}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        # Start sequences
        for _ in range(0,5):

            # Start sequence
            await (self.virt_sequence.start(self.tb_env_ssdt_b2b.virtual_sequencer))

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")

# ---------------------------------------------------------------------------------------------
# Launch sequences until the sum of the response 'data' is higher than 'data_adder_max'.
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_ssdt_b2b_default_accumulate_seq(test_ssdt_b2b_base_setup):
    """ Test that launches sequences until the sum of the response 'data' is higher than 'data_adder_max'.
    """

    def __init__(self, name="test_ssdt_b2b_data_accumulate_seq", parent=None):

        super().__init__(name, parent)

        self.data_adder_max = 100
        self.data_adder = 0

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.__class__.__name__}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        while (self.data_adder <= self.data_adder_max):

            # Start sequence
            await (self.virt_sequence.start(self.tb_env_ssdt_b2b.virtual_sequencer))

            # Add 'rsp.data' to the previous value
            self.data_adder += self.virt_sequence.consumer_seq.rsp.data

            self.logger.info(f"Adder: {self.data_adder}, rsp: {self.virt_sequence.consumer_seq.rsp}")

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")


# ---------------------------------------------------------------------------------------------
# Launch 'N' number of sequences w/ inline constraint
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_ssdt_b2b_rand_n_seq(test_ssdt_b2b_base_setup):
    """ Test that launches 'N' number of random sequences using inline constraint.
    """

    def __init__(self, name="test_ssdt_b2b_accumulate2_seq", parent=None):

        super().__init__(name, parent)

    def start_of_simulation_phase(self):

        super().start_of_simulation_phase()
        uvm_factory().set_type_override_by_type(ssdt_b2b_default_seq, ssdt_b2b_rand_size_seq)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.__class__.__name__}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        # Randomize number of seq. items
        with self.virt_sequence.randomize_with() as seq:
            seq.number_of_seqs < 200

        self.logger.info(f"Number of sequences = {self.virt_sequence.number_of_seqs}")

        # Start virtual sequence
        await (self.virt_sequence.start(self.tb_env_ssdt_b2b.virtual_sequencer))

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")


# ---------------------------------------------------------------------------------------------
# Test launching the 'ssdt_b2b_inf_accumulate_seq' sequence
# ---------------------------------------------------------------------------------------------
@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_sssdt_b2b_inf_accum_seq(test_ssdt_b2b_base_setup):
    """ Test that launches sequences until the sum of the response 'data' is higher than 'data_adder_max'.
    """

    def __init__(self, name="test_ssdt_b2b_rand_size_accum_seq", parent=None):

        super().__init__(name, parent)

    def start_of_simulation_phase(self):

        super().start_of_simulation_phase()
        uvm_factory().set_type_override_by_type(ssdt_b2b_default_seq, ssdt_b2b_inf_accumulate_seq)

    async def run_phase(self):

        self.logger.info(f"{'-'*30} Running test <{self.__class__.__name__}> {'-'*30}")

        self.raise_objection()

        await super().run_phase()

        # Randomize the maximum value of the accumulator
        with self.virt_sequence.randomize_with() as seq:
            seq.data_adder_max == 105

        # Start sequence
        await (self.virt_sequence.start(self.tb_env_ssdt_b2b.virtual_sequencer))

        self.drop_objection()

        self.logger.info(f"{'-'*30} END 'run_phase' of <{self.__class__.__name__}> {'-'*30}")

