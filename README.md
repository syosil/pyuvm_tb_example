# pyuvm_tb_example

This is an example of how to create reusable UVCs with PyUVM.

The DUT is very simple design which accepts a transaction from the
producer agent and forwards it if the value is lower than a certain
threshold. If above the threshold then it saturates.

It also includes a reference model written in C.

Go to the src/tb direcotry and run:

make sim

to simulate the design.

# Requirements

* Python 3.10 or newer
* Proper setup of pyuvm environment
* Icarus 11 or newer

# Directory Structure

/
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

