""" SSDT-UVC Driver

- The UVM Driver is an active entity that converts abstract transaction to design pin toggles and vice-versa.
- Transaction level objects are obtained from the Sequencer and the UVM Driver drives them to the design via an interface handler, and vice-versa.
"""

from pyuvm import uvm_driver
from cocotb.triggers import RisingEdge, ReadOnly
from .uvc_ssdt_config import uvc_ssdt_type_enum

class uvc_ssdt_driver(uvm_driver):
    """ Driver for the SSDT-UVC.
        - translates transactions to pin level activity.
        - transactions pulled from sequencer by the seq_item_port.
    """
    def __init__(self, name="uvc_driver", parent=None):

        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None         # Configuration object
        self.vif = None         # Virtual interface object

    def build_phase(self):

        self.logger.debug("build_phase() Driver")
        super().build_phase()

        # Create an instance of configuration object
        self.cfg = self.cdb_get("cfg", "")

        # Create an instance of Virtual interface (obtained from the ConfigDB)
        self.vif = self.cfg.vif

    async def run_phase(self):
        """ Run task of the Driver.
        """
        await super().run_phase()

        self.logger.info("Running driver...")

        while True:
            self.logger.debug(f"{'='*50}")

            # 1. Get(Wait for) next item
            self.logger.debug("Waiting for next seq_item...")
            self.req = await self.seq_item_port.get_next_item()
            self.logger.debug(f"Seq. item got: {self.req}")
            self.logger.debug(f"{'-'*50}")

            # 2. Once it get the transaction from the sequencer, clones it
            self.rsp = self.req.clone()     # creates clone of seq item
            self.rsp.set_context(self.req)  # Set response_id. Link a new response transaction to the request transaction.
            self.rsp.set_id_info(self.req)
            # TODO: Explain this... Why context is not enought?

            # 3. Drive transaction
            self.logger.debug("...Driving pins...")
            await self.drive_transaction()

            self.seq_item_port.item_done()
            self.logger.debug("item_done()")

            self.logger.debug(f"Putting response: {self.rsp}")
            self.seq_item_port.put_response(self.rsp)
            self.logger.debug("Response put.")

    async def drive_transaction(self):

        # start driver as producer or consumer
        if self.cfg.driver_type is uvc_ssdt_type_enum.PRODUCER:
            await self.producer_loop()
        elif self.cfg.driver_type is uvc_ssdt_type_enum.CONSUMER:
            await self.consumer_loop()
        else:
            self.logger.critical(f"DRIVER, not handled driver {self.get_full_name()}")

    async def producer_loop(self):

        self.logger.debug("Running PRODUCER loop...")
        self.logger.debug(f"PRODUCER (req): data = {self.req.data}")

        self.vif.data.value = self.req.data
        self.vif.valid.value = 1
        self.rsp.data = self.req.data

        await RisingEdge(self.vif.clk)

        self.reset_bus()
        self.logger.debug(f"PRODUCER (rsp): data = {self.rsp.data}")

    async def consumer_loop(self):

        self.logger.debug("Running CONSUMER loop...")
        self.logger.debug(f"CONSUMER (req): data = {self.req}")

        while True:
            await ReadOnly()
            if (self.vif.valid.value.binstr == "1"):
                self.rsp.data = self.vif.data.value
                await RisingEdge(self.cfg.vif.clk)
                break
            await RisingEdge(self.cfg.vif.clk)
        self.logger.debug(f"CONSUMER (rsp): data = {self.rsp}")

    def reset_bus(self):
        self.vif.data.value = 0
        self.vif.valid.value = 0