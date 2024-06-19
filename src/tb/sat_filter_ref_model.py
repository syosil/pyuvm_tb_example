""" Saturation Filter Reference Model handler.
"""

import cocotb
from pyuvm import uvm_component, uvm_analysis_port, uvm_tlm_analysis_fifo
from ref_model import sat_filter_ref_model_py_wrapper as ref_model
from ref_model.sat_filter_ref_model_utils import SeqItem, SeqItemOut


class sat_filter_ref_model(uvm_component):
    """ Handler for Reference Model.
    """

    def __init__(self, name="sat_filter_ref_model", parent=None):

        super().__init__(name, parent)

        # analysis port for sending ref model item
        self.analysis_port = None

        # FIFOs for connecting to UVC's ap's
        self.uvc_ssdt_producer_fifo = None
        self.uvc_ssdt_consumer_fifo = None

        self.threshold = None

    def build_phase(self):
        super().build_phase()

        self.uvc_ssdt_producer_fifo = uvm_tlm_analysis_fifo("uvc_ssdt_producer_fifo", self)
        self.uvc_ssdt_consumer_fifo = uvm_tlm_analysis_fifo("uvc_ssdt_consumer_fifo", self)

        self.analysis_port = uvm_analysis_port(f"{self.get_name()}_analysis_port", self)

    async def run_phase(self):
        await super().run_phase()

        # Sample item from UVC producer's FIFO
        cocotb.start_soon(self.sample_item(self.uvc_ssdt_producer_fifo))

    async def sample_item(self, fifo):

        # The 'ref_model_input' structure is used to pass the threshold value.
        seq_input_item = SeqItem(THRESHOLD=self.threshold)
        seq_output_item = SeqItemOut()

        while True:
            item = await fifo.get()

            self.logger.debug(f"-------------------------------")
            self.logger.info(f"Get item : {item}")

            input_item = item.clone()
            output_item = item.clone()

            self.logger.debug(f"FIFO : {input_item.get_name()}")

            # Update values
            seq_input_item.set_values(item.data)

            # Send input item to reference model
            ref_model.sat_filter_operation(seq_input_item, seq_output_item)

            output_item.data = seq_output_item.data
            output_item.valid = seq_output_item.valid

            self.logger.debug(f"output_item : {output_item}")
            self.analysis_port.write(output_item)