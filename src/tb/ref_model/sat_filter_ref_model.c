/**
 * @file sat_filter_ref_model.c
 * @author João Carvalho
 * @brief Reference Model for Saturation Filter.
 * @version 0.1
 * @date 2024-04-15
 *
 * @copyright
 *
 */

#include <stdio.h>
#include <stdlib.h>

#include "sat_filter_ref_model.h"

static struct ref_model_output *ref_model_output = NULL;

/**
 * @brief Saturation filter operation.
 * - Receives a pointer with the inputs.
 * - Returns a pointer with the output values.
 * - The 'ref_model_input' structure is used to pass the threshold value.
 * - It is assumed that the input valid signal is always 1 when the reference model is launched.
 *
 * @param ref_model_input
 * @return struct ref_model_output*
 */
struct ref_model_output* sat_filter_ref_model(struct ref_model_input* ref_model_input)
{
    // Memory allocation for output structure
    if (ref_model_output == NULL){
        ref_model_output = (struct ref_model_output*)
            malloc(sizeof(struct ref_model_output));

        ref_model_output->valid = 0;
        ref_model_output->data = 0;
        ref_model_output->overflow = 0;
    }

    // Set output default values
    ref_model_output->valid = 0;
    ref_model_output->overflow = 0;

    if (ref_model_input->data <= ref_model_input->THRESHOLD)
    {
        ref_model_output->data = ref_model_input->data;
        ref_model_output->valid = 1;
    }
    else
    {
        ref_model_output->data = ref_model_input->THRESHOLD;
        ref_model_output->valid = 1;
        ref_model_output->overflow = 1;
    }

    #if _DEBUG_MODE_ == 1
    pretty_print(ref_model_input, ref_model_output);
    #endif

    return ref_model_output;
}

#if _DEBUG_MODE_ == 1
void pretty_print(struct ref_model_input* input, struct ref_model_output* output){
    printf("|---------------|----------------|\n");
    printf("| in_valid: %3d | out_valid: %3d |\n", input->valid, output->valid);
    printf("| in_data:  %3d | out_data:  %3d |\n", input->data, output->data);
    printf("|               | overflow:  %3d |\n", output->overflow);
    printf("|---------------|----------------|\n");
}
#endif