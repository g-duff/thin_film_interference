float complex calculate_senkrecht_reflection(
    float complex *incident_wavevector_normal_component,
    float complex *transmission_wavevector_normal_component
);

float complex calculate_senkrecht_transmission (
    float complex *incident_wavevector_normal_component,
    float complex *transmission_wavevector_normal_component
);

float complex calculate_parallel_reflection(
        float complex *incident_wavevector_normal_component,
        float complex *transmission_wavevector_normal_component,
        const float complex *incident_refractive_index,
        const float complex *transmission_refractive_index
);

float complex calculate_parallel_transmission(
        float complex *incident_wavevector_normal_component,
        float complex *transmission_wavevector_normal_component,
        const float complex *incident_refractive_index,
        const float complex *transmission_refractive_index
);
