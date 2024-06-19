# pyuvm_tb_example

This is an example of how to create reusable UVCs with PyUVM.

The DUT is very simple design which accepts a transaction from the
producer agent and forwards it if the value is lower than a certain
threshold. If above the threshold then it saturates.

It also includes a reference model written in C.

Go to the src/tb direcotry and run:

make sim

to simulate the design. Look in the section below for more info on how to setup the design.

# Requirements and Setup

* Python 3.10 or newer
* Proper setup of pyuvm environment
* Icarus 11 or newer

We recommend setting up a Python virtual environment and then install the following Python modules:

    cocotb == 1.8.1
    pyuvm == 2.9.1
    pyvsc == 0.8.8.*
    cocotb-coverage == 1.1.0
    constrainedrandom == 1.1.2
    pytest == 8.1

# Directory Structure

    ROOT
    ├── docs
    └── src
        ├── rtl
        └── tb
            ├── ref_model
            ├── tests
            ├── uvc
            │   └── ssdt
            │       ├── docs
            │       │   ├── figures
            │       │   └── waves
            │       ├── src
            │       └── tb
            └── vseqs

