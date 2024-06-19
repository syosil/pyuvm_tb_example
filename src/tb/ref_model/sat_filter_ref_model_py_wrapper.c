#include <Python.h>
#include <stdio.h>

#include "sat_filter_ref_model.h"

// -------------------------------------------------------------
// Functions to be exposed to Python
// -------------------------------------------------------------

struct ref_model_input* input_struct = NULL;
struct ref_model_output* output_struct = NULL;

static PyObject* sat_filter_operation(PyObject* self, PyObject* args){

    // Default python object
    PyObject* input_struct_obj;
    PyObject* output_struct_obj;

    if (!PyArg_ParseTuple(args, "OO", &input_struct_obj,&output_struct_obj)){
        return NULL;
    }

    // Access the fields of the Python object
    PyObject* DATA_W_obj    = PyObject_GetAttrString(input_struct_obj, "DATA_W");
    PyObject* THRESHOLD_obj = PyObject_GetAttrString(input_struct_obj, "THRESHOLD");
    PyObject* in_valid_obj  = PyObject_GetAttrString(input_struct_obj, "valid");
    PyObject* in_data_obj   = PyObject_GetAttrString(input_struct_obj, "data");

    // Create input structure (required by sat_filter_operation())
    if(input_struct == NULL)
    {
        input_struct = (struct ref_model_input*) malloc(sizeof(struct ref_model_input));
    }

    // Extract the values from the Python objects
    input_struct->DATA_W  = PyLong_AsLong(DATA_W_obj);
    input_struct->THRESHOLD  = PyLong_AsLong(THRESHOLD_obj);
    input_struct->valid  = PyLong_AsLong(in_valid_obj);
    input_struct->data  = PyLong_AsLong(in_data_obj);

    // Reference Model Operation
    output_struct = sat_filter_ref_model(input_struct);

    // Set values return by C function to Python object
    PyObject* return_out_valid_obj = PyLong_FromLong(output_struct->valid);
    PyObject* return_out_data_obj = PyLong_FromLong(output_struct->data);
    PyObject* return_overflow_obj = PyLong_FromLong(output_struct->overflow);

    PyObject_SetAttrString(output_struct_obj, "valid", return_out_valid_obj);
    PyObject_SetAttrString(output_struct_obj, "data", return_out_data_obj);
    PyObject_SetAttrString(output_struct_obj, "overflow", return_overflow_obj);

    // Clean up
    Py_CLEAR(DATA_W_obj);
    Py_CLEAR(THRESHOLD_obj);
    Py_CLEAR(in_valid_obj);
    Py_CLEAR(in_data_obj);

    Py_CLEAR(return_out_valid_obj);
    Py_CLEAR(return_out_data_obj);
    Py_CLEAR(return_overflow_obj);

    Py_RETURN_NONE;
}

// -------------------------------------------------------------
// Method definition object for the module
// -------------------------------------------------------------
static PyMethodDef sat_filter_ref_model_wrapper_methods[] = {
    {"sat_filter_operation", sat_filter_operation, METH_VARARGS, "run operation"},
    {NULL, NULL, 0, NULL}
};

// -------------------------------------------------------------
// Module definition object
// -------------------------------------------------------------
static struct PyModuleDef sat_filter_ref_model_py_wrapper = {
    PyModuleDef_HEAD_INIT,
    "sat_filter_ref_model_py_wrapper",
    "Reference Model for Saturation Filter",
    -1,
    sat_filter_ref_model_wrapper_methods
};

// -------------------------------------------------------------
// Module initialization function
// -------------------------------------------------------------
PyMODINIT_FUNC PyInit_sat_filter_ref_model_py_wrapper(void) {
    return PyModule_Create(&sat_filter_ref_model_py_wrapper);
}