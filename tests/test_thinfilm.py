import thinfilm as tf   # The code to test
import unittest         # The test framework
import numpy as np
import random


class BaseFunctions(unittest.TestCase):

    def test_snellnormal(self):
        n1 = 1.0
        n2 = 1.5
        theta_i = 0
        snell_out = tf.snell_theta_t(n1, n2, theta_i)
        self.assertEqual(snell_out, 0)

    def test_snellangle(self):
        n1 = 2
        n2 = np.sqrt(2)
        theta_i = 45*tf.degrees
        snell_out = tf.snell_theta_t(n1, n2, theta_i)
        self.assertAlmostEqual(snell_out, np.pi/2)

    def test_phase_normalincidence(self):
        tau = 2*np.pi

        lam0 = 800
        theta_t = 0
        nf = 2.0

        comparison_factors = (0, 1/2, 1/4, 1/6)

        thick = [cf*lam0 for cf in comparison_factors]
        phase_compare = [cf*2*nf*tau for cf in comparison_factors]

        k0 = tau/lam0

        phase_out = [tf.phase_difference(k0, nf, t, theta_t) for t in thick]

        phase_residuals = (pout - pcomp for pout, pcomp in 
            zip(phase_out, phase_compare))
        phase_residuals = sum(phase_residuals)

        self.assertAlmostEqual(phase_residuals, 0)


    def test_phase_angledincidence(self):
        tau = 2*np.pi

        lam0 = 800
        theta_t = 60*tf.degrees
        nf = 2.0
        
        comparison_factors = (0, 1/2, 1/4, 1/6)

        thick = [cf*lam0 for cf in comparison_factors]
        phase_compare = [cf*2*nf*tau*0.5 for cf in comparison_factors]

        k0 = tau/lam0

        phase_out = [tf.phase_difference(k0, nf, t, theta_t) for t in thick]

        phase_residuals = (pout - pcomp for pout, pcomp in 
            zip(phase_out, phase_compare))
        phase_residuals = sum(phase_residuals)

        self.assertAlmostEqual(phase_residuals, 0)


class Fresnel(unittest.TestCase):

    def test_fresnel_s_energyconservation(self):

        theta_i = 15
        n_1 = 1.0
        n_2 = 1.5
    
        theta_t = tf.snell_theta_t(n_1, n_2, theta_i)
        
        r = tf.fresnel_r_s(n_1, n_2, theta_i, theta_t)
        t = tf.fresnel_t_s(n_1, n_2, theta_i, theta_t)

        R = r**2
        T = t**2 * n_2*np.cos(theta_t)/n_1/np.cos(theta_i)

        test_energy = R + T 
        self.assertAlmostEqual(test_energy, 1)


    def test_fresnel_p_energyconservation(self):

        theta_i = 15
        n_1 = 1.0
        n_2 = 1.5
        
        theta_t = tf.snell_theta_t(n_1, n_2, theta_i)
        
        r = tf.fresnel_r_p(n_1, n_2, theta_i, theta_t)
        t = tf.fresnel_t_p(n_1, n_2, theta_i, theta_t)

        R = r**2
        T = t**2 * n_2*np.cos(theta_t)/n_1/np.cos(theta_i)

        test_energy = R + T
        self.assertAlmostEqual(test_energy, 1)


class Ellipsometry(unittest.TestCase):

    def test_snellnormal(self):
        n1 = 1.0
        n2 = 1.5
        snell_out = tf.snell_theta_t(n1, n2, 0)
        self.assertEqual(snell_out, 0)

    def test_regpro_SoI(self):
        lambda_0, tan_psi_rp, cos_delta_rp = np.genfromtxt('./tests/SoI_regressPro.txt', 
            skip_header=1, unpack=True, usecols=(0, 2, 5))

        n_cov = 1.0

        n_in = [3.8, 1.45, 3.8]
        t_in = [220, 3000]

        AOI = 65

        k0 = 2*np.pi/lambda_0
        theta_i = AOI*tf.degrees

        n_in.reverse()
        t_in.reverse()

        r_s = tf.next_r_s(k0, theta_i, n_cov, n_in[:], t_in[:])
        r_p = tf.next_r_p(k0, theta_i, n_cov, n_in[:], t_in[:])

        psi, delta = tf.psi_delta(r_s, r_p)

        psi_residules = np.tan(psi) - tan_psi_rp
        delta_residules = np.cos(delta) - cos_delta_rp

        psi_residules = sum(psi_residules)
        delta_residules = sum(delta_residules)

        total_residules = round(psi_residules+delta_residules, 4)

        self.assertEqual(total_residules, 0)


if __name__ == '__main__':
    unittest.main()