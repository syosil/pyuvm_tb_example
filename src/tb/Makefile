# --------------------- NOT COCOTB ARGS --------------------------------------
ROOT_DIR = $(shell pwd)

# Defining paths
RTL_DIR = $(ROOT_DIR)/../rtl
TB_DIR = $(ROOT_DIR)

TB_TESTS_DIR = $(TB_DIR)/tests
# Get all file names from the test folder to be used in the MODULE arg
TB_TESTS_FILENAMES = $(shell find $(TB_TESTS_DIR) -type f \( -iname "test*.py" -or -iname "*test.py" \) -exec basename {} .py \; | paste -s -d ',')

TB_VSEQS_DIR = $(TB_DIR)/vseqs

SSDT_TESTS_DIR = $(TB_DIR)/uvc/ssdt/tb

REF_MODEL_SOURCEDIR := $(TB_DIR)/ref_model
REF_MODEL_BUILDDIR := $(REF_MODEL_SOURCEDIR)/_build

# Make dir if does not exist
$(shell mkdir -p $(REF_MODEL_BUILDDIR))

# because Makefile is in a different directory
export PYTHONPATH = $(TB_DIR):$(TB_TESTS_DIR)

# TODO: This is hard coded because to build it requires the 'Python.h' lib that is only installed with 'python-dev' package.
export PYTHON_H_HOME = '/usr/include/python3.10'
export PYTHON_LIB = $(VIRTUAL_ENV)/lib/python3.10/:$(REF_MODEL_BUILDDIR):$(TB_TESTS_DIR)
export PYTHON_H_HOME = /mnt/common/itd/software/install/python/3.12.0.RL8/include/python3.12/
export PYTHON_LIB = $(VIRTUAL_ENV)/lib/python3.12/:$(REF_MODEL_BUILDDIR):$(TB_TESTS_DIR)

export PYUVM_LOG_LEVEL := INFO

# --------------------- COCOTB ARGS --------------------------------------

# Defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
COCOTB_LOG_LEVEL ?= INFO
export COCOTB_REDUCED_LOG_FMT = 1

# Verilog source files to include
VERILOG_INCLUDE_DIRS := $(RTL_DIR)
VERILOG_SOURCES := $(RTL_DIR)/sat_filter.sv
VERILOG_SOURCES += $(RTL_DIR)/sat_filter_wrapper.sv

# TOPLEVEL is the DUT instance
TOPLEVEL := sat_filter_wrapper

# RTL Parameters
THRESHOLD ?= 8
DATA_W ?= 4

COMPILE_ARGS += -P$(TOPLEVEL).THRESHOLD=$(THRESHOLD)
COMPILE_ARGS += -P$(TOPLEVEL).DATA_W=$(DATA_W)

# MODULE is the basename of the Python test file
MODULE := $(TB_TESTS_FILENAMES)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# ------------------------------------------------------------------------------

# To run our targets and cocotb targets
sim: build-ref-model
debug: local-debug
clean::
	@$(MAKE) local-clean -C $(TB_DIR)

# ------------------------------------------------------------------------------
# Because of Reference Model
# ------------------------------------------------------------------------------

DEBUG_MODE := 0

# Compiler
CC := gcc

# Flags for compilation (adding warnings are always good)
CFLAGS = -g -Wall --debug

# Source files
REF_MODEL_SOURCES = $(REF_MODEL_SOURCEDIR)/sat_filter_ref_model.c \
					$(REF_MODEL_SOURCEDIR)/sat_filter_ref_model.h

ifeq ($(PYUVM_LOG_LEVEL), DEBUG)
	$(info PYUVM_LOG_LEVEL is ${PYUVM_LOG_LEVEL})
	DEBUG_MODE := 1
endif

# -------------------------------------------------------------------------------

# Build 'sat_filter_ref_model' module as a shared library
.PHONY: build-ref-model
build-ref-model: build-python
	@cp $(REF_MODEL_BUILDDIR)/sat_filter_ref_model_py_wrapper.so $(REF_MODEL_SOURCEDIR)/

# Build 'sat_filter_ref_model.c' module
.PHONY: build-C
build-C: $(REF_MODEL_SOURCES)
	@$(CC) $(CFLAGS) -shared -fPIC \
		-o $(REF_MODEL_BUILDDIR)/sat_filter_ref_model.o \
		$(REF_MODEL_SOURCES) \
		-D_DEBUG_MODE_=$(DEBUG_MODE)
#-shared -fPIC

# Build wrapper module to be used in Python
.PHONY: build-python
build-python: $(REF_MODEL_SOURCEDIR)/sat_filter_ref_model_py_wrapper.c build-C
	@$(CC) $(CFLAGS) -shared -fPIC \
		-o $(REF_MODEL_BUILDDIR)/sat_filter_ref_model_py_wrapper.so \
		-I $(PYTHON_H_HOME) -I $(PYTHON_LIB) \
		$(REF_MODEL_SOURCES) \
		$(REF_MODEL_SOURCEDIR)/sat_filter_ref_model_py_wrapper.c

# -------------------------------------------------------------------------------
# Because of PyVSC and coverage
# -------------------------------------------------------------------------------

# PyVSC (help debug)
export VSC_SOLVEFAIL_DEBUG = 0
export VSC_CAPTURE_SRCINFO = 0
export VSC_DEBUG = 0

THE_SIM_BUILD = $(TB_DIR)/$(SIM_BUILD)
COV_FILES = $(shell find $(THE_SIM_BUILD) -type f \( -iname "*.xml" \))

# https://pyucis.readthedocs.io/en/latest/commands.html
.PHONY: coverage-merge
coverage-merge:
	@echo ""
	@echo "======================================================"
	@echo "Merging coverage files..."
	@echo $(THE_SIM_BUILD)
	@echo $(COV_FILES)
	@echo "======================================================"
	@echo ""
	@$(VIRTUAL_ENV)/bin/pyucis merge --out $(THE_SIM_BUILD)/merge_cov.xml $(THE_SIM_BUILD)/*.xml

.PHONY: coverage-view
coverage-view: coverage-merge
	@echo ""
	@echo "======================================================"
	@echo "Opening PyUCIS-viewer"
	@echo "======================================================"
	@echo ""
	@$(VIRTUAL_ENV)/bin/pyucis-viewer $(THE_SIM_BUILD)/merge_cov.xml

.PHONY: coverage
coverage: coverage-view

# -------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------

.PHONY: local-clean
local-clean:
	@echo -e "\n------------------ Internal cleanup --------------------\n"
	# Remove build stuff from ref. model
	@rm -fv $(shell find $(REF_MODEL_SOURCEDIR) -type f \( -iname "*.*o" \);)
	# Remove all __pycache__ folders
	@rm -fvr $(shell find $(ROOT_DIR) -type d \( -iname '__pycache__' \);)

.PHONY: local-debug
local-debug::
	@echo -e "\n--------------------------------------\n"
	@echo DEBUG_MODE = $(DEBUG_MODE)

	@echo TB_TESTS_FILENAMES = $(TB_TESTS_FILENAMES)

	@echo SOURCES = $(REF_MODEL_SOURCES)
	@echo SOURCEDIR = $(REF_MODEL_SOURCEDIR)
	@echo BUILDDIR = $(REF_MODEL_BUILDDIR)

	@echo PYTHONPATH = $(PYTHONPATH)
	@echo "run 'where python' "
	@echo -e "\n--------------------------------------\n"

.PHONY: local-help
local-help::
	@echo -e "\n--------------------------------------\n"
	@echo DEBUG_MODE = $(DEBUG_MODE)