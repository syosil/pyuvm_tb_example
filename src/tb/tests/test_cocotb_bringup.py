""" Basic cocotb test.
"""
from random import randint

import cocotb
from cocotb.triggers import RisingEdge
from cocotb.types import Logic, LogicArray

async def reset(dut):
    """ Reset operation.
    """

    # Reset
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

@cocotb.test()
async def bringup_test(dut):
    """ Bringup Test. Just reset.
    """

    # creates clock of 5ns
    # cocotb.start_soon(Clock(dut.clk, 5, units="ns").start())

    # Wait some time
    await RisingEdge(dut.clk)

    # Reset
    await reset(dut)

    # Wait some time
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

@cocotb.test()
async def test_seq_data(dut):
    """ Test that sends sequential values [0:2:max_value].
    """

    await RisingEdge(dut.clk)
    dut.in_valid.value = 1

    dut_bit_w = dut.DATA_W.value
    max_value = 2**dut_bit_w-1
    cocotb.log.info(f"DATA_W = {dut_bit_w}, max_value = {max_value}")

    for in_data in range(0,max_value,2):
        dut.in_data.value = in_data
        await RisingEdge(dut.clk)
        cocotb.log.info(f"IN_DATA = {dut.in_data.value.integer}")

    dut.in_valid.value = 0

@cocotb.test()
async def test_send_X_data(dut):
    """ Test that send 'X' and 'Z'.
    """

    await RisingEdge(dut.clk)
    dut.in_valid.value = 1

    dut_bit_w = dut.DATA_W.value
    n_cycles = 4
    cocotb.log.info(f"DATA_W = {dut_bit_w}, max_value = {n_cycles}")

    for _ in range(0,n_cycles):
        dut.in_data.value = LogicArray("X"*dut_bit_w)
        await RisingEdge(dut.clk)
        cocotb.log.info(f"IN_DATA = {dut.in_data.value.binstr}")

    for _ in range(0,n_cycles):
        dut.in_data.value = LogicArray("Z"*dut_bit_w)
        await RisingEdge(dut.clk)
        cocotb.log.info(f"IN_DATA = {dut.in_data.value.binstr}")

    dut.in_valid.value = 0

@cocotb.test()
async def test_rand_all(dut):
    """ Test that sends random values between [0:max_value], 'max_value*2' times.
    """

    await RisingEdge(dut.clk)

    dut_bit_w = dut.DATA_W.value
    max_value = 2**dut_bit_w-1
    cocotb.log.info(f"DATA_W = {dut_bit_w}, max_value = {max_value}")

    for _ in range(0,max_value*2):
        dut.in_valid.value = randint(0,1)
        dut.in_data.value = randint(0,max_value)
        await RisingEdge(dut.clk)
        cocotb.log.info(f"IN_DATA = {dut.in_data.value.integer}")

    dut.in_valid.value = 0
