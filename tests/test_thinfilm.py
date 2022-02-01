import thinfilm as tf   # The code to test
import unittest         # The test framework
import numpy as np


class BaseFunctions(unittest.TestCase):

    def test_calculateAngleOfTransmission_normalIncidence(self):
        '''Snell's law at normal incidence'''
        # Given
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        incidentAngle = 0

        # When
        transmissionAngle = tf.calculateTransmissionAngle(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle)

        # Then
        self.assertEqual(transmissionAngle, 0)

    def test_calculateAngleOfTransmission_obliqueIncidence(self):
        '''Snell's law, incident at 45 degrees tested
        against exact sine values for total internal reflection'''
        # Given
        coverRefractiveIndex = 2
        substrateRefractiveIndex = np.sqrt(2)
        incidentAngle = 45*tf.degrees

        # When
        transmissionAngle = tf.calculateTransmissionAngle(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle)

        # Then
        self.assertAlmostEqual(transmissionAngle, np.pi/2)

    def test_calculatePhaseDifference_normalIncidence(self):
        '''Phase difference from reflections indide a film at normal incidence
        tested against film thicknesses of fractional wavelengths'''

        # Given
        tau = 2*np.pi

        freeSpaceWavelength = 800
        transmissionAngle = 0
        filmRefractiveIndex = 2.0

        comparisonFactors = (0, 1/2, 1/4, 1/6)

        filmThicknesses = [cf*freeSpaceWavelength for cf in comparisonFactors]
        freeSpaceWavenumber = tau/freeSpaceWavelength

        # When
        actualPhaseDifference = [tf.calculatePhaseDifference(freeSpaceWavenumber, filmRefractiveIndex, t, transmissionAngle) for t in filmThicknesses]

        # Then
        expectedPhaseDifference = [cf*2*filmRefractiveIndex*tau for cf in comparisonFactors]
        phaseResiduals = (pout - pcomp for pout, pcomp in
                           zip(actualPhaseDifference, expectedPhaseDifference))
        phaseResiduals = sum(phaseResiduals)

        self.assertAlmostEqual(phaseResiduals, 0)

    def test_calculatePhaseDifference_angledincidence(self):
        ''' Phase difference from reflections indide a film at 60 degrees
        tested against film thicknesses of fractional wavelengths and
        exact cosine values'''

        # Given
        tau = 2*np.pi
        freeSpaceWavelength = 800
        transmissionAngle = 60*tf.degrees
        filmRefractiveIndex = 2.0

        comparisonFactors = (0, 1/2, 1/4, 1/6)
        filmThicknesses = [cf*freeSpaceWavelength for cf in comparisonFactors]
        freeSpaceWavenumber = tau/freeSpaceWavelength

        # When
        actualPhaseDifference = [tf.calculatePhaseDifference(freeSpaceWavenumber, filmRefractiveIndex, t, transmissionAngle) for t in filmThicknesses]

        # Then
        expectedPhaseDifference = [cf*2*filmRefractiveIndex*tau*0.5 for cf in comparisonFactors]
        phaseResiduals = (pout - pcomp for pout, pcomp in
                           zip(actualPhaseDifference, expectedPhaseDifference))
        phaseResiduals = sum(phaseResiduals)

        self.assertAlmostEqual(phaseResiduals, 0)


class Fresnel(unittest.TestCase):

    def test_fresnelSenkrecht_energyconservation(self):
        '''Energy conservation for reflected and transmitted
        amplitudes of s poarised light at an air-glass interface'''

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        transmissionAngle = tf.calculateTransmissionAngle(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle)

        # When
        reflection = tf.calculateSenkrechtReflection(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle, transmissionAngle)
        transmission = tf.calculateSenkrechtTransmission(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle, transmissionAngle)

        # Then
        reflectivity = reflection**2
        transmissivity = transmission**2 * substrateRefractiveIndex*np.cos(transmissionAngle)/coverRefractiveIndex/np.cos(incidentAngle)
        energy = reflectivity + transmissivity
        self.assertAlmostEqual(energy, 1)

    def test_fresnelParallel_energyconservation(self):
        '''Energy conservation for reflected and transmitted
        amplitudes of p poarised light at an air-glass interface'''

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefrativeIndex = 1.5
        transmissionAngle = tf.calculateTransmissionAngle(coverRefractiveIndex, substrateRefrativeIndex, incidentAngle)

        # When
        reflection = tf.calculateParallelReflection(coverRefractiveIndex, substrateRefrativeIndex, incidentAngle, transmissionAngle)
        transmission = tf.calculateParallelTransmission(coverRefractiveIndex, substrateRefrativeIndex, incidentAngle, transmissionAngle)


        # Then
        reflectivity = reflection**2
        transmissivity = transmission**2 * substrateRefrativeIndex*np.cos(transmissionAngle)/coverRefractiveIndex/np.cos(incidentAngle)
        test_energy = reflectivity + transmissivity
        self.assertAlmostEqual(test_energy, 1)


class Ellipsometry(unittest.TestCase):

    def test_regpro_SoI(self):
        '''Compare calculated psi and delta values for SoI thin film against
        output from the Regress Pro application 
        using the same input parameters'''

        freeSpaceWavelength, expectedTanPsi, expectedCosDelta = np.genfromtxt('./tests/SoI_regressPro.txt',
                                                           skip_header=1, unpack=True, usecols=(0, 2, 5))

        # Given
        refractiveIndices = [1.0, 3.8, 1.45, 3.8]
        filmThicknesses = [220, 3000]
        incidentAngle = 65*tf.degrees

        # When
        psi, delta = tf.ellipsometry(freeSpaceWavelength, incidentAngle, refractiveIndices, filmThicknesses)


        # Then
        tanPsiResiduals = np.tan(psi) - expectedTanPsi
        cosDeltaResiduals = np.cos(delta) - expectedCosDelta

        tanPsiResiduals = sum(tanPsiResiduals)
        cosDeltaResiduals = sum(cosDeltaResiduals)
        totalResiduals = round(tanPsiResiduals+cosDeltaResiduals, 4)

        self.assertAlmostEqual(totalResiduals, 0)


if __name__ == '__main__':
    unittest.main()
