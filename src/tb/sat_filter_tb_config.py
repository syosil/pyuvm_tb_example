from pyuvm import uvm_object

from uvc.ssdt.src.uvc_ssdt_config import uvc_ssdt_config


class sat_filter_tb_config(uvm_object):

    def __init__(self, name="cl_sdt_tb_config"):

        super().__init__(name)

        self.data_width = None
        self.threshold = None

        self.ssdt_prod_cfg = uvc_ssdt_config.create("ssdt_prod_cfg")
        self.ssdt_cons_cfg = uvc_ssdt_config.create("ssdt_cons_cfg")

    def build_phase(self):

        self.ssdt_prod_cfg.DATA_WIDTH = self.data_width
        self.ssdt_cons_cfg.DATA_WIDTH = self.data_width