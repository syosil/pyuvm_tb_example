""" Sat_filter Coverage collector"""

import vsc
from pyuvm import uvm_subscriber

class sat_filter_coverage(uvm_subscriber):

    def __init__(self, name, parent):

        super().__init__(name, parent)

    def build_phase(self):
        self.logger.info("Start build_phase()-> Sat_filter coverage")
        super().build_phase()

        # Create the covergroup
        self.cg_sat_filter = covergroup_sat_filter(f"{self.get_full_name()}.cg_sat_filter")

        self.logger.info("End build_phase()-> Sat_filter coverage")

    # Write function to sample the covergroup
    def write(self, signal):
        """Sampling method"""

        self.logger.info(f"Sat_filter_coverage received OVF signal {signal}")
        self.cg_sat_filter.sample(signal)


# Covergroup class to sample the ovf signal
@vsc.covergroup
class covergroup_sat_filter(object):
    def __init__(self, name):
        self.options.name = name

        # Define the parameters accepted by the sample function
        self.with_sample(
            ovf = vsc.bit_t(1)
        )

        self.cp_ovf = vsc.coverpoint(self.ovf, bins = {
            "ovf_0" : vsc.bin(0),
            "ovf_1" : vsc.bin(1)}
        )
