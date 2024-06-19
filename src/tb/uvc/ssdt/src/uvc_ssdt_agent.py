""" SSDT Agent.

- Provides protocol specific tasks to generate transactions, check the results and perform coverage.
- UVM agent encapsulates the Sequencer, Driver and Monitor into a single entity.
- The components here are instatiated and connected via TLM interfaces.
- Can also have configuration options like:
    - the type of UVM agent (active/passive),
    - knobs to turn on features such as functional coverage, and other similar parameters.
"""

from pyuvm import uvm_agent, uvm_active_passive_enum, uvm_analysis_port, uvm_sequencer, uvm_factory
from .uvc_ssdt_driver import uvc_ssdt_driver
from .uvc_ssdt_monitor import uvc_ssdt_monitor
from .uvc_ssdt_coverage import uvc_ssdt_coverage

from .uvc_ssdt_seq_item import uvc_ssdt_seq_item
from .ssdt_common import ssdt_seq_item_override


class uvc_ssdt_agent(uvm_agent):
    """ UVM agent for SSDT.
    """

    def __init__(self, name="ssdt_agent", parent=None):

        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None         # Configuration object
        self.sequencer = None   # Sequencer handler
        self.monitor = None     # Monitor handler
        self.driver = None      # Driver handler

        self.analysis_port = None   # Analysis Port handler

        # Define the coverage handle
        self.coverage = None        # Coverage handler

        self.logger.debug("Agent initialized.")

    def build_phase(self):

        self.logger.info(f"Building Agent {self.get_name()}...")
        super().build_phase()

        # Instantiate configuration object
        self.cfg = self.cdb_get("cfg", "")

        # Build based on the type of the agent (active/passive)

        # If ACTIVE build driver and sequencer, and passes handles to 'cfg'
        self.logger.debug(f" Agent < {self.get_name()} > will be configured as {self.get_is_active().name}.")
        if self.get_is_active() == uvm_active_passive_enum.UVM_ACTIVE:

            # Instantiate Driver and pass handler to ConfigDB
            self.logger.debug(f"Creating Driver...")
            self.driver = uvc_ssdt_driver.create(f"{self.get_name()}_driver", self)
            self.driver.cdb_set("cfg", self.cfg, "")
            self.logger.debug(f"Driver created.")

            # Instantiate Sequencer and pass handler to ConfigDB
            self.logger.debug(f"Creating Sequencer...")
            self.sequencer = uvm_sequencer.create(f"{self.get_name()}_sequencer", self)
            self.logger.debug(f"Sequencer created.")

        # This will apply the agent configurations needed to the sequence item
        uvm_factory().set_type_override_by_type(uvc_ssdt_seq_item, ssdt_seq_item_override(self.cfg.DATA_WIDTH))

        # Create instance of Monitor and pass handle to ConfigDB
        self.logger.debug(f"Creating Monitor...")
        self.monitor = uvc_ssdt_monitor.create(f"{self.get_name()}_monitor", self)
        self.monitor.cdb_set("cfg", self.cfg, "")
        self.logger.debug(f"Monitor created.")

        # Create instance of coverage collector and pass handle to ConfigDB
        self.coverage = uvc_ssdt_coverage.create(f"{self.get_name()}_coverage", self)
        self.coverage.cdb_set("cfg", self.cfg, "")

        # Create instance of Analysis Port
        self.analysis_port = uvm_analysis_port(f"{self.get_name()}_analysis_port", self)

        self.logger.debug(f"Agent {self.get_name()} built!!")

    def connect_phase(self):

        self.logger.debug(f"connect_phase() Agent")
        super().connect_phase()

        # Connects driver to sequencer if UVM_ACTIVE (sequence item port)
        if self.get_is_active() == uvm_active_passive_enum.UVM_ACTIVE:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)

        # Connect monitor analysis port to the agent analysis port
        self.monitor.mon_analysis_port.connect(self.analysis_port)

        # Connect Coverage collector
        self.monitor.mon_analysis_port.connect(self.coverage.analysis_export)
