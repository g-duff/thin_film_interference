#include <stdio.h>
#include <complex.h>
#include <tgmath.h>

float complex calculate_senkrecht_reflection (
    float complex *incident_wavevector_normal_component,
    float complex *transmission_wavevector_normal_component
) {
    float complex numerator = (*incident_wavevector_normal_component) - (*transmission_wavevector_normal_component);
    float complex denominator = (*incident_wavevector_normal_component) + (*transmission_wavevector_normal_component);
    return numerator / denominator;
}

float complex calculate_senkrecht_transmission (
    float complex *incident_wavevector_normal_component,
    float complex *transmission_wavevector_normal_component
) {
    float complex numerator = 2 * (*incident_wavevector_normal_component);
    float complex denominator = (*incident_wavevector_normal_component) + (*transmission_wavevector_normal_component);
    return numerator / denominator;
}

float complex calculate_parallel_reflection(
        float complex *incident_wavevector_normal_component,
        float complex *transmission_wavevector_normal_component,
        const float complex *incident_refractive_index,
        const float complex *transmission_refractive_index
) {
        float complex numerator = (*incident_wavevector_normal_component) * pow(*transmission_refractive_index,2) - 
            (*transmission_wavevector_normal_component) * pow(*incident_refractive_index,2);
        float complex denominator = (*incident_wavevector_normal_component) * pow(*transmission_refractive_index,2) + 
            *transmission_wavevector_normal_component * pow(*incident_refractive_index,2);
        return numerator / denominator;
}

float complex calculate_parallel_transmission(
        float complex *incident_wavevector_normal_component,
        float complex *transmission_wavevector_normal_component,
        const float complex *incident_refractive_index,
        const float complex *transmission_refractive_index
) {
        float complex numerator = 2 * (*incident_wavevector_normal_component) * (*incident_refractive_index) * (*transmission_refractive_index);
        float complex denominator = (*incident_wavevector_normal_component) * pow(*transmission_refractive_index,2) + 
            (*transmission_wavevector_normal_component) * pow(*incident_refractive_index,2);
        return numerator / denominator;
}
