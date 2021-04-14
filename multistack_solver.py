import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import cmath
import functools as ftl

def multilayer_opt(beta, d, n, k0):
    '''Based on the physics of sec 5.2.3 Slab Waveguide
    Models an n-layer slab waveguide. 
    Minimize to find guided modes.

    Inputs
    beta: propagation constant, float
    d: layer thickesses, 1D iterable of floats
    n: layer RI, iterable of floats same length as d 
    k0: wave vector in free space

    Outputs:
    diff: float
    '''

    # From equation 5.20
    kx = [cmath.sqrt((k0*ni)**2 - beta**2) for ni in n]

    # From figure 5.7
    alpha = [1j*kxi for kxi in kx]

    # From figure 5.7. Easier to use delta plus one to put into 
    # eqn 5.20 matrix
    delta_p_1 = [a*di for a, di in zip(alpha[1:], d[1:])]

    # From equation 5.20
    matrices = [np.array([[(a+a_p1)*np.exp(-d_p1), (a-a_p1)*np.exp(d_p1)],
                        [(a-a_p1)*np.exp(-d_p1), (a+a_p1)*np.exp(d_p1)]]
    )/(2*a) for a, a_p1, d_p1 in zip(alpha, alpha[1:], delta_p_1)]

    # Find the product of the eqn 5.20 matrices
    M = ftl.reduce(np.matmul, matrices)
    diff = M[0,0]

    return abs(diff)
    
# System parameters
lam0 = 750  # nm
mid_thickness = np.arange(1,10) # nm
thicknesses = [np.array([0, 400, 95, u, 0]) for u in mid_thickness] # nm
n = [1.45, 2.02, 1.66, 0.66, 1.45] # RIU

# Calculation parameters
k0 = 2*np.pi/lam0

# The algorithm requires a starting guess, so give a range of starting guesses
n_guesses = np.arange(1.45, 2.0, 0.01)
beta_in = k0*n_guesses

# Pre-allocate an array to output beta at all starting guesses,
# which is a good check for if the algorithm found a minimum
bmat_out = np.ones((len(mid_thickness), len(beta_in)))

# Preallocate an array for effective index, with default value 
# as air (1)
neff = np.ones((len(mid_thickness), len(beta_in)))

for i, t in enumerate(thicknesses):
    for j, b_in in enumerate(beta_in):

        # Grab the raw output for the colour plot
        bmat_out[i, j] = abs(multilayer_opt(b_in, t, n, k0).real)

        # Attempt to find a local minimum for a given initual guess: beta_in
        try:
            beta_out, r = opt.newton(multilayer_opt, x0=b_in,
            args=(t, n, k0), maxiter=100, tol=1e-10, full_output=True)
        except:
            beta_out = k0

        # Check if it looks minimized, then calculate the effective index
        # from the propagation constant and replace the default "air" value 
        # with this new value
        if abs(multilayer_opt(beta_out, t, n, k0).real)<0.1 :
            neff[i, j] = beta_out.real/k0


print(neff)

# Output
fig, ax = plt.subplots()

cb = ax.pcolor(mid_thickness, n_guesses, bmat_out.T)
fig.colorbar(cb)

for ne in neff.T:
    ax.plot(mid_thickness, ne.real, 'wo', ms=1)

ax.set_ylim([1.45, 2.0])
ax.set_xlabel('Guide thickness (nm)')
ax.set_ylabel(r'$n_{eff}$')
plt.show()
