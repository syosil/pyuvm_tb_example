from pyuvm import uvm_object

from uvc.ssdt.src.uvc_ssdt_config import uvc_ssdt_config

#TODO: Improve class to create objects from method.

class ssdt_b2b_cfg(uvm_object):
    """ Configuration object for SSDT-UVC B2B.
    """
    def __init__(self, name='base_test_config'):

        super().__init__(name)

        self.ssdt_prod_cfg = uvc_ssdt_config.create("uvc_ssdt_b2b_producer")
        self.ssdt_cons_cfg = uvc_ssdt_config.create("uvc_ssdt_b2b_consumer")