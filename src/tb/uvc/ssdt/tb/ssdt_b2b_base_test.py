""" SSDT-UVC base test

- UVM testcase.
- Base test file to be used as parent.
"""

import os
import cocotb
import vsc
from pyuvm import uvm_test, uvm_report_object, uvm_root

from uvc.ssdt.src.uvc_ssdt_interface import ssdt_interface_wrapper
from uvc.ssdt.src.uvc_ssdt_interface_assertions import ssdt_interface_assert_check

from .ssdt_b2b_env import ssdt_b2b_env
from .ssdt_b2b_cfg import ssdt_b2b_cfg
from .ssdt_b2b_sequence_lib import ssdt_b2b_default_seq


class ssdt_b2b_base_test(uvm_test):
    """ Base test component for the SSDT-UVC.
    """

    def __init__(self, name="ssdt_b2b_base_test", parent=None):

        # -------------------------------------------------------------------------------------------------------
        # to set the default logging level before the build phase (https://github.com/pyuvm/pyuvm/discussions/39)
        _LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "NOTSET", "NullHandler"]
        if os.getenv("PYUVM_LOG_LEVEL") in _LOG_LEVELS:
            _PYUVM_LOG_LEVEL = os.getenv('PYUVM_LOG_LEVEL')
        else:
            _PYUVM_LOG_LEVEL = "INFO"
            if os.getenv("PYUVM_LOG_LEVEL") != None:
                uvm_root().logger.warning(f"{'='*50}\n   Wrong value for 'PYUVM_LOG_LEVEL' in Makefile. Changing to default value: 'INFO'.\n    {'='*50}")

        uvm_report_object.set_default_logging_level(_PYUVM_LOG_LEVEL)
        # -------------------------------------------------------------------------------------------------------

        super().__init__(name, parent)

        # Configuration object handler
        self.cfg = None

        # Declare Environment handler
        self.tb_env_ssdt_b2b = None

        # Declare DUT handler
        self.dut = None

        # Declare Virtual Sequence handler
        self.virt_sequence = None

    def build_phase(self):

        self.logger.debug(f"build_phase() Base Test")
        super().build_phase()

        # Create configuration objects
        self.cfg = ssdt_b2b_cfg('ssdt_b2b_cfg')
        self.cdb_set("cfg", self.cfg, "")

        # Access the DUT through the cocotb.top handle
        self.dut = cocotb.top

        # --------------------------------------------------------------------------

        # Instantiate interface
        self.ssdt_if  = ssdt_interface_wrapper("ssdt_prod_if")

        self.ssdt_prod_if = self.ssdt_if
        self.ssdt_cons_if = self.ssdt_if

        # Set interfaces in configs for each component
        self.cfg.ssdt_prod_cfg.vif = self.ssdt_prod_if
        self.cfg.ssdt_cons_cfg.vif = self.ssdt_cons_if

        # Assertions checker signals connections
        self.assert_check = ssdt_interface_assert_check(clk_signal   = self.dut.clk,
                                                        rst_signal   = self.dut.rst,
                                                        valid_signal = self.dut.in_valid,
                                                        data_signal  = self.dut.in_data)
        # --------------------------------------------------------------------------

        # Instantiate Environment
        self.tb_env_ssdt_b2b = ssdt_b2b_env.create("ssdt_b2b_env", self)
        self.tb_env_ssdt_b2b.cdb_set("cfg", self.cfg, "")

        # --------------------------------------------------------------------------

        # Get DUT parameters and pass to the agents
        self.cfg.ssdt_prod_cfg.DATA_WIDTH = self.dut.DATA_W.value
        self.cfg.ssdt_cons_cfg.DATA_WIDTH = self.dut.DATA_W.value

        # Pass the DUT parameters to the checkers class
        self.assert_check._set_width_values(self.cfg.ssdt_prod_cfg.DATA_WIDTH)
        # --------------------------------------------------------------------------

    def connect_phase(self):

        self.logger.debug(f"connect_phase() Base Test")
        super().connect_phase()

        self.ssdt_if.connect( clk_signal = self.dut.clk,
                              reset_signal = self.dut.rst,
                              valid_signal = self.dut.in_valid,
                              data_signal = self.dut.in_data
        )

    async def run_phase(self):

        self.logger.debug(f"run_phase() Base Test")
        await super().run_phase()

        # Start assertions check
        cocotb.start_soon(self.assert_check.check_assertions())

        # Instantiate (Virtual) Sequence
        self.virt_sequence = ssdt_b2b_default_seq.create("ssdt_b2b_top_seq")
        self.cdb_set("virt_sequence", self.virt_sequence, "")

        self.logger.debug(f"Sequence {self.virt_sequence}.")

    def report_phase(self):

        self.logger.debug(f"report_phase() Base Test")
        super().report_phase()

        # Creating coverage report with PyVSC

        # Writing coverage report in (.txt format)
        f = open(f'sim_build/{self.get_type_name()}_cov.txt', "w")
        f.write(f"Coverage report for {self.get_type_name()} \n")
        f.write("------------------------------------------------\n \n")
        vsc.report_coverage(fp=f, details=True)
        f.close()

        # writing coverage report in xml-format
        filename = f'sim_build/{self.get_type_name()}_cov.xml' # Destination for coverage data
        fmt = "xml" # Format of the coverage data. ‘xml’ and ‘libucis’ supported
        libucis = None # Path to a library implementing the UCIS C API (default=None)

        vsc.write_coverage_db(
            filename,
            fmt,
            libucis
        )

        # For each file only information regarding the test will show
        vsc.impl.coverage_registry.CoverageRegistry.clear()
