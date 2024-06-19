from pyuvm import uvm_object
from enum import IntEnum


class uvc_ssdt_type_enum(IntEnum):
    """ Type of driver: PRODUCER or CONSUMER """
    PRODUCER = 0
    CONSUMER = 1

class uvc_ssdt_config(uvm_object):
    """ Configuration object for SSDT-UVC.
    """
    def __init__(self, name='ssdt_config'):

        super().__init__(name)

        #############################
        # General configuration
        #############################

        # Setting agent type
        # uvm_active_passive_enum.UVM_ACTIVE or uvm_active_passive_enum.UVM_PASSIVE
        self.is_active = None

        # Virtual Interface for SSDT
        self.vif = None

        # Driver type: uvc_ssdt_type_enum.PRODUCER OR uvc_ssdt_type_enum.CONSUMER
        self.driver_type = None

        # Set 'data' field width
        self.DATA_WIDTH = None