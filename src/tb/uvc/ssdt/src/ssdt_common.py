import vsc
from uvc.ssdt.src.uvc_ssdt_seq_item import uvc_ssdt_seq_item


def ssdt_seq_item_override(data_w = 0):
    """ Method to be used by the UVM Factory, to override sequence item parameters.
    This is a cheat way to apply the constraints over the created sequence item.
    """
    @vsc.randobj
    class ssdt_seq_item_updated(uvc_ssdt_seq_item):
        """ Cheat class to apply constraints using UVM Factory.
        """

        def __init__(self, name = "ssdt_seq_item_updated"):
            super().__init__(name)

        @vsc.constraint
        def ssdt_parameters_update(self):
            """Setting the correct DATA_WIDTH parameter"""
            self.SSDT_DATA_W == data_w
            self.data > 0
            self.data <= 2**(data_w)-1

    return ssdt_seq_item_updated