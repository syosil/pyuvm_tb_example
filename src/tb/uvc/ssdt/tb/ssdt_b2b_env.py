""" SSDT-UVC Environment UVM component.

- A UVM environment contains several, reusable verification components, such as, agents, scoreboard, coverage collector, ...
- Here is defined their default configuration required by the test case.
"""

from pyuvm import uvm_env, uvm_active_passive_enum
from uvc.ssdt.src.uvc_ssdt_config import uvc_ssdt_type_enum
from uvc.ssdt.src.uvc_ssdt_agent import uvc_ssdt_agent
from .ssdt_b2b_virt_sequencer import ssdt_b2b_virt_sequencer


class ssdt_b2b_env(uvm_env):
    """ UVM Environment component for SSDT-UVC B2B.
    """

    def __init__(self, name, parent):

        super().__init__(name, parent)

        # Declare configuration object
        self.cfg = None

        # Declare Virtual Sequencer
        self.virtual_sequencer = None

        # Declare Agents
        self.uvc_ssdt_producer = None
        self.uvc_ssdt_consumer = None

    def build_phase(self):

        self.logger.debug("build_phase Environment")
        super().build_phase()

        # Instantiate configuration object
        self.cfg = self.cdb_get("cfg")
        self.logger.debug(f"config  {self.cfg}")

        # Instantiate Virtual Sequencer
        self.logger.debug(f"Creating Virtual Sequencer...")
        self.virtual_sequencer = ssdt_b2b_virt_sequencer.create("uvc_ssdt_b2b_top_seqr", self)
        self.virtual_sequencer.cdb_set("cfg", self.cfg, "")
        self.logger.debug(f"Virtual Sequencer < {self.virtual_sequencer} > created")

        # Instantiate Agents
        self.logger.debug("Creating Agents...")

        # ----- Producer ------
        self.uvc_ssdt_producer = uvc_ssdt_agent.create("uvc_ssdt_producer", self)

        self.uvc_ssdt_producer.cdb_set("cfg", self.cfg.ssdt_prod_cfg, "")
        self.cfg.ssdt_prod_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.cfg.ssdt_prod_cfg.driver_type = uvc_ssdt_type_enum.PRODUCER

        self.logger.debug(f"\nAgent < {self.uvc_ssdt_producer} > created with the following configs {self.uvc_ssdt_producer.cfg}\n")

        # ----- Consumer ------
        self.uvc_ssdt_consumer = uvc_ssdt_agent.create("uvc_ssdt_consumer", self)

        self.uvc_ssdt_consumer.cdb_set("cfg", self.cfg.ssdt_cons_cfg, "")
        self.cfg.ssdt_cons_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.cfg.ssdt_cons_cfg.driver_type = uvc_ssdt_type_enum.CONSUMER

        self.logger.debug(f"\nAgent < {self.uvc_ssdt_consumer} > created with the following configs {self.uvc_ssdt_consumer.cfg}\n")


        # -----------------

    def connect_phase(self):

        self.logger.debug(f"connect_phase() Environment")
        super().connect_phase()

        # Connect agents' sequencer to virtual sequencer
        self.logger.debug(f"Connecting virtual sequencer: {self.virtual_sequencer}")

        self.virtual_sequencer.ssdt_producer_sequencer = self.uvc_ssdt_producer.sequencer
        self.virtual_sequencer.ssdt_consumer_sequencer = self.uvc_ssdt_consumer.sequencer

        self.logger.debug(f"Virtual sequencer connected: {self.virtual_sequencer}")
