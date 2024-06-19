""" SSDT interface wrapper
"""

class ssdt_interface_wrapper():
    """ Python interface wrapper for SSDT.
    """

    def __init__(self, clk=None, rst=None, name="ssdt_interface"):

        self.name  = name

        self.clk   = clk
        self.rst   = rst

        self.valid = None
        self.data  = None

    def connect(self, clk_signal, reset_signal, valid_signal, data_signal):
        """ Connecting the signals to the interface.
        """

        self.clk = clk_signal
        self.rst = reset_signal

        self.valid  = valid_signal
        self.data   = data_signal
