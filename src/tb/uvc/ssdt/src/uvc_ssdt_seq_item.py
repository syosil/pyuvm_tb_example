"""
SSDT-UVC sequence item with constraints using PyVSC.
"""

import vsc
from pyuvm import uvm_sequence_item


@vsc.randobj
class uvc_ssdt_seq_item(uvm_sequence_item):
    """ SSDT-UVC base sequence item with constraints.
    """

    def __init__(self, name):

        super().__init__(name)

        # Transaction objects
        # NOTE: This has a limitation: SSDT_DATA_W cannot be higher then 2**64. The same goes for the 'data'
        self.SSDT_DATA_W = vsc.rand_uint64_t()
        self.data = vsc.rand_bit_t(64)

    def __eq__(self, other) -> bool:
        """ defines how sequence items are compared. """
        if isinstance(other, self.__class__):
            return (self.data == other.data)
        else:
            return False

    def __str__(self) -> str:
        """ defines output string when printing sequence item. """
        if self.data is None:
            self.data = 0

        return (f"{self.get_name()} : data = {self.data};")