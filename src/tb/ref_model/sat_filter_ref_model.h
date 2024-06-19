/**
 * @file sat_filter_ref_model.h
 * @author João Carvalho
 * @brief Saturation Filter Reference Model library.
 * @version 0.1
 * @date 2024-04-15
 *
 * @copyright
 *
 */
#ifndef REF_MODEL_H
#define REF_MODEL_H

/**
 * @brief Macro defining the default value of the threshold parameter.
 *
 */
#ifndef _THRESHOLD_
#define _THRESHOLD_ 8
#endif

/**
 * @brief Macro defining the default value of the data width parameter.
 *
 */
#ifndef _DATA_W_
#define _DATA_W_ 4
#endif

/**
 * @brief Macro defining debug mode.
 *
 */
#ifndef _DEBUG_MODE_
#define _DEBUG_MODE_ 0
#endif

struct ref_model_input{
    int DATA_W;
    int THRESHOLD;
    int valid;
    int data;
};

struct ref_model_output{
    int valid;
    int data;
    int overflow;
};

struct ref_model_output* sat_filter_ref_model(struct ref_model_input* seq_item);
void pretty_print(struct ref_model_input* input, struct ref_model_output* output);

#endif