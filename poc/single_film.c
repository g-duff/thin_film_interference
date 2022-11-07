#include <stdio.h>
#include <complex.h>
#include <tgmath.h>


float complex calculate_film_reflection(
    float complex reflection_out_of,
    float complex reflection_into,
    float complex transmission_into,
    float complex transmission_back,
    float complex accumulated_phase
) {
    float complex numerator = transmission_into * reflection_out_of * transmission_back;
    float complex demoninator = exp(-1 * I  * accumulated_phase) + 
        reflection_into * reflection_out_of;
    return reflection_into + numerator / demoninator;
}