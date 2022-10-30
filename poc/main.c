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
        float complex incident_wavevector_normal_component,
        float complex transmission_wavevector_normal_component,
        float complex incident_refractive_index,
        float complex transmission_refractive_index
) {
        float complex numerator = incident_wavevector_normal_component * pow(transmission_refractive_index,2) - 
            transmission_wavevector_normal_component * pow(incident_refractive_index,2);
        float complex denominator = incident_wavevector_normal_component * pow(transmission_refractive_index,2) + 
            transmission_wavevector_normal_component * pow(incident_refractive_index,2);
        return numerator / denominator;
}

float complex calculate_parallel_transmission(
        float complex incident_wavevector_normal_component,
        float complex transmission_wavevector_normal_component,
        float complex incident_refractive_index,
        float complex transmission_refractive_index
) {
        float complex numerator = 2 * incident_wavevector_normal_component * incident_refractive_index * transmission_refractive_index;
        float complex denominator = incident_wavevector_normal_component * pow(transmission_refractive_index,2) + 
            transmission_wavevector_normal_component * pow(incident_refractive_index,2);
        return numerator / denominator;
}

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

int main (void) {
    const int number_of_films = 2;
    const float thicknesses[number_of_films] = {220, 3000};
    
    const int number_of_layers = number_of_films+2;
    const float refractive_indexes[number_of_layers] = {1.0, 3.8, 1.45, 3.8};

    const float wavelength = 500.056;
    const float incident_angle = 65.0 * M_PI /180.0;

    float freespace_wavevector = 2.0*M_PI/wavelength;
    float complex wavevector_normal_components[number_of_layers];

    for (int i=0; i<number_of_layers; i++) {
        float n = refractive_indexes[i];
        wavevector_normal_components[i] = freespace_wavevector * csqrt(pow(n, 2) - pow(sin(incident_angle) * refractive_indexes[0], 2));
    }

    float complex senkrecht_reflection = calculate_senkrecht_reflection(
        &wavevector_normal_components[number_of_layers-2], &wavevector_normal_components[number_of_layers-1]);
    float complex parallel_reflection = calculate_parallel_reflection(
        wavevector_normal_components[number_of_layers-2], wavevector_normal_components[number_of_layers-1],
        refractive_indexes[number_of_layers-2], refractive_indexes[number_of_layers-1]);

    for (int i=number_of_films; i>0; i--) {

        const float *film_thickness = &thicknesses[i-1];

        float film_refractive_index = refractive_indexes[i];
        float complex film_wavevector_normal_component = wavevector_normal_components[i];

        float incident_refractive_index = refractive_indexes[i-1];
        float complex incident_wavevector_normal_component = wavevector_normal_components[i-1];

        float complex accumulated_phase = 2 * (*film_thickness) * film_wavevector_normal_component;

        parallel_reflection = calculate_film_reflection(
            parallel_reflection,
            calculate_parallel_reflection(
                incident_wavevector_normal_component, film_wavevector_normal_component,
                incident_refractive_index, film_refractive_index),
            calculate_parallel_transmission(
                incident_wavevector_normal_component, film_wavevector_normal_component,
                incident_refractive_index, film_refractive_index),
            calculate_parallel_transmission(
                film_wavevector_normal_component, incident_wavevector_normal_component,
                film_refractive_index, incident_refractive_index),
            accumulated_phase
        );

        senkrecht_reflection = calculate_film_reflection(
            senkrecht_reflection,
            calculate_senkrecht_reflection(
                &incident_wavevector_normal_component, &film_wavevector_normal_component),
            calculate_senkrecht_transmission(
                &incident_wavevector_normal_component, &film_wavevector_normal_component),
            calculate_senkrecht_transmission(
                &film_wavevector_normal_component, &incident_wavevector_normal_component),
            accumulated_phase
        );
    }

    printf("%1.7f + %1.7fi\n", creal(senkrecht_reflection), cimag(senkrecht_reflection));
    printf("%1.7f + %1.7fi\n", creal(parallel_reflection), cimag(parallel_reflection));
}
