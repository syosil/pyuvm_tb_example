""" Saturation Filter virtual Sequencer.
"""

from pyuvm import uvm_sequencer


class sat_filter_tb_virt_sequencer(uvm_sequencer):
    """ Virtual sequencer component for Saturation Filter TB.
    """

    def __init__(self, name="sat_filter_tb_virt_sequencer", parent=None):

        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None     # Configuration object

        self.ssdt_producer_sequencer = None     # Handler for producer sequencer
        self.ssdt_consumer_sequencer = None     # Handler for consumer sequencer

    def build_phase(self):

        super().build_phase()