""" Saturation Filter base UVM Test.
"""

import os, warnings
import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
import vsc

from pyuvm import uvm_test, uvm_report_object, uvm_root

from sat_filter_tb_config import sat_filter_tb_config
from sat_filter_tb_env import sat_filter_tb_env
from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from sat_filter_coverage import sat_filter_coverage

from uvc.ssdt.src.uvc_ssdt_interface import ssdt_interface_wrapper
from uvc.ssdt.src.uvc_ssdt_interface_assertions import ssdt_interface_assert_check

# to set the default logging level before the build phase (https://github.com/pyuvm/pyuvm/discussions/39)
_LOG_LEVELS = ["DEBUG", "CRITICAL", "ERROR", "WARNING", "INFO", "NOTSET", "NullHandler"]

class sat_filter_tb_base_test(uvm_test):
    """ Base test component for the Saturation Filter TB.
    """

    def __init__(self, name="sat_filter_base_test", parent=None):

        # ----------------------------------------------------------------------
        if os.getenv("PYUVM_LOG_LEVEL") in _LOG_LEVELS:
            _PYUVM_LOG_LEVEL = os.getenv('PYUVM_LOG_LEVEL')
        else:
            _PYUVM_LOG_LEVEL = "INFO"
            if os.getenv("PYUVM_LOG_LEVEL") != None:
                uvm_root().logger.warning(f"{'='*50}\n   Wrong value for 'PYUVM_LOG_LEVEL' in Makefile. Changing to default value: 'INFO'.\n    {'='*50}")

        uvm_report_object.set_default_logging_level(_PYUVM_LOG_LEVEL)
        # ----------------------------------------------------------------------

        super().__init__(name, parent)

        # Configuration object handler
        self.cfg = None

        # Declare Environment handler
        self.tb_env = None

        # Declare DUT handler
        self.dut = None

        # Declare Virtual Sequence handler
        self.virt_sequence = None

        # Agent's interfaces
        self.ssdt_prod_if = None
        self.ssdt_cons_if = None

        # Saturation filter coverage - OVF
        self.sat_filter_cov = None

        # Quick fix because of warnings og PYVSC
        warnings.simplefilter("ignore")

    def build_phase(self):

        self.logger.debug("build_phase() Base Test")
        super().build_phase()

        # Create configuration objects
        self.cfg = sat_filter_tb_config.create('sat_filter_base_cfg')
        self.cdb_set("cfg", self.cfg, "")

        # Access the DUT through the cocotb.top handle
        self.dut = cocotb.top

        # Instantiate Environment
        self.tb_env = sat_filter_tb_env.create("sat_filter_tb_env", self)
        self.tb_env.cdb_set("cfg", self.cfg, "")

        # Create the saturation filter coverage
        self.sat_filter_cov = sat_filter_coverage.create("coverage", self)

        # Instantiate interface
        self.ssdt_prod_if = ssdt_interface_wrapper("ssdt_prod_if")
        self.ssdt_cons_if = ssdt_interface_wrapper("ssdt_cons_if")

        # Set interfaces in configs for each component
        self.cfg.ssdt_prod_cfg.vif = self.ssdt_prod_if
        self.cfg.ssdt_cons_cfg.vif = self.ssdt_cons_if

        # Assertions checker connections
        self.assert_check = ssdt_interface_assert_check(clk_signal   = self.dut.clk,
                                                        rst_signal   = self.dut.rst,
                                                        valid_signal = self.dut.in_valid,
                                                        data_signal  = self.dut.in_data)
        # --------------------------------------------------------------------------

        # Get DUT parameters and pass to the agents
        self.cfg.ssdt_prod_cfg.DATA_WIDTH = self.dut.DATA_W.value
        self.cfg.ssdt_cons_cfg.DATA_WIDTH = self.dut.DATA_W.value

        self.cfg.data_width = self.dut.DATA_W.value
        self.cfg.threshold = self.dut.THRESHOLD.value

        # Pass the required parameters to the sSDT checker class
        self.assert_check._set_width_values(self.cfg.ssdt_prod_cfg.DATA_WIDTH)
        # --------------------------------------------------------------------------

    def connect_phase(self):

        self.logger.debug("connect_phase() Base Test")
        super().connect_phase()

        self.ssdt_prod_if.connect(clk_signal=self.dut.clk,
                                  reset_signal=self.dut.rst,
                                  valid_signal=self.dut.in_valid,
                                  data_signal=self.dut.in_data
                                  )

        self.ssdt_cons_if.connect(clk_signal=self.dut.clk,
                                  reset_signal=self.dut.rst,
                                  valid_signal=self.dut.out_valid,
                                  data_signal=self.dut.out_data
                                  )

    # Monitor loop to trigger the sample mechanism of the ovf signal
    async def monitor_loop_ovf(self):
        """ Monitor loop for overflow signal"""
        while True:
            await RisingEdge(self.dut.clk)
            await ReadOnly()

            # Sample whenever 'valid' == 1
            if (self.dut.out_valid.value.binstr == "1"):
                self.sat_filter_cov.write(self.dut.ovf)

    async def run_phase(self):

        self.logger.debug(f"run_phase() Base Test")
        await super().run_phase()

        # Start assertions check and overflow coverage
        cocotb.start_soon(self.assert_check.check_assertions())
        cocotb.start_soon(self.monitor_loop_ovf())

        # Instantiate (Virtual) Sequence
        self.virt_sequence = sat_filter_tb_base_seq.create("sat_filter_tb_seq")
        self.cdb_set("virt_sequence", self.virt_sequence, "")
        self.logger.debug(f"Sequence {self.virt_sequence}.")

        # Clean inputs
        self.dut.in_data.value = 0
        self.dut.in_valid.value = 0

        # Trigger reset
        await self.trigger_reset()

    def report_phase(self):

        self.logger.debug("report_phase() Base Test")
        super().report_phase()

        # Check if the assertions failed
        assert self.assert_check.passed, "assertions failed"

        # Creating coverage report with PyVSC
        self.setup_pyvsc_coverage_report()

    # --------------------------------------------------

    async def trigger_reset(self):
        """Reset operation"""

        self.logger.debug(f"Resetting DUT...")

        await RisingEdge(self.dut.clk)
        self.dut.rst.value = 1

        await RisingEdge(self.dut.clk)
        await RisingEdge(self.dut.clk)
        self.dut.rst.value = 0

        self.logger.debug(f"Resetting DONE.")

    def setup_pyvsc_coverage_report(self):

        # Writing coverage report in (.txt format)
        f = open(f'sim_build/{self.get_type_name()}_cov.txt', "w")
        f.write(f"Coverage report for {self.get_type_name()} \n")
        f.write("------------------------------------------------\n \n")
        vsc.report_coverage(fp=f, details=True)
        f.close()

        # writing coverage report in xml-format
        # Destination for coverage data
        _SIM_BUILD_FOLDER_ = os.getenv("SIM_BUILD", default="sim_build")
        uvm_root().logger.debug(f"{'='*50}\n 'SIM_BUILD' is '{_SIM_BUILD_FOLDER_}'.\n    {'='*50}")

        filename = f'{_SIM_BUILD_FOLDER_}/{self.get_type_name()}_cov.xml'
        fmt = "xml"  # Format of the coverage data. ‘xml’ and ‘libucis’ supported
        # Path to a library implementing the UCIS C API (default=None)
        libucis = None

        vsc.write_coverage_db(
            filename,
            fmt,
            libucis
        )

        # For each file only information regarding the test will show
        vsc.impl.coverage_registry.CoverageRegistry.clear()
