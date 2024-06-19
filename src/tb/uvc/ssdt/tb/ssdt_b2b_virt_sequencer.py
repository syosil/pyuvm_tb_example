""" SSDT-UVC virtual Sequencer
"""

from pyuvm import uvm_sequencer


class ssdt_b2b_virt_sequencer(uvm_sequencer):
    """ Virtual sequencer component for SSDT-UVC B2B TB.
    """

    def __init__(self, name="ssdt_b2b_sequencer", parent=None):

        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None     # Configuration object

        self.ssdt_producer_sequencer = None     # Handler for producer sequencer
        self.ssdt_consumer_sequencer = None     # Handler for consumer sequencer