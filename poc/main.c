#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <tgmath.h>

#include "fresnel.h"
#include "single_film.h"


int main (void) {
    const int NUMBER_OF_FILMS = 2;
    const int NUMBER_OF_LAYERS = NUMBER_OF_FILMS+2;
    
    float *thicknesses = (float*)malloc(NUMBER_OF_FILMS * sizeof(float));
    thicknesses[0] = 220;
    thicknesses[1] = 3000;

    const float complex refractive_indexes[NUMBER_OF_LAYERS] = {1.0, 3.8, 1.45, 3.8};

    const float wavelength = 500.056;
    const float incident_angle = 65.0 * M_PI /180.0;

    const float freespace_wavevector = 2.0*M_PI/wavelength;
    float complex wavevector_normal_components[NUMBER_OF_LAYERS];

    for (int i=0; i<NUMBER_OF_LAYERS; i++) {
        float n = refractive_indexes[i];
        wavevector_normal_components[i] = freespace_wavevector * csqrt(pow(n, 2) - pow(sin(incident_angle) * refractive_indexes[0], 2));
    }

    const float complex *film_refractive_index = &refractive_indexes[NUMBER_OF_LAYERS-1];
    const float complex *incident_refractive_index = film_refractive_index-1;
    
    float complex *film_wavevector_normal_component = &wavevector_normal_components[NUMBER_OF_LAYERS-1];
    float complex *incident_wavevector_normal_component = film_wavevector_normal_component-1;

    float complex senkrecht_reflection = calculate_senkrecht_reflection(
        incident_wavevector_normal_component, film_wavevector_normal_component);
    float complex parallel_reflection = calculate_parallel_reflection(
                incident_wavevector_normal_component, film_wavevector_normal_component,
                incident_refractive_index, film_refractive_index);

    for (int i=NUMBER_OF_FILMS-1; i>-1; i--) {

        film_refractive_index--;
        film_wavevector_normal_component--;
        incident_refractive_index--;
        incident_wavevector_normal_component--;
        
        const float film_thickness = thicknesses[i];
        float complex accumulated_phase = 2 * film_thickness * (*film_wavevector_normal_component);

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
                incident_wavevector_normal_component, film_wavevector_normal_component),
            calculate_senkrecht_transmission(
                incident_wavevector_normal_component, film_wavevector_normal_component),
            calculate_senkrecht_transmission(
                film_wavevector_normal_component, incident_wavevector_normal_component),
            accumulated_phase
        );
    }

    printf("%1.7f + %1.7fi\n", creal(senkrecht_reflection), cimag(senkrecht_reflection));
    printf("%1.7f + %1.7fi\n", creal(parallel_reflection), cimag(parallel_reflection));

    free(thicknesses);
}
