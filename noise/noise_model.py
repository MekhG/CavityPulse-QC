"""
noise/noise_model.py

Constructs the Lindblad collapse operators that encode irreversible
interaction between the bosonic mode and its environment. Without these
operators the simulation would describe an idealized, lossless cavity
rather than a realistic, noisy one.

Two channels are modeled, mirroring the qubit project's T1/T2 split:

  Photon loss   (rate kappa)     -- the bosonic analogue of T1 relaxation.
                                     Collapse operator: sqrt(kappa) * a
                                     Drives population from |n> toward |n-1>,
                                     continuously throughout the evolution,
                                     directly competing with the drive's
                                     attempt to build up population in |1>.

  Photon dephasing (rate gamma_phi) -- the bosonic analogue of T2 dephasing.
                                     Collapse operator: sqrt(gamma_phi) * a^dag a
                                     Destroys coherences between different
                                     Fock states without directly changing
                                     level populations, which suppresses the
                                     interference the drive relies on to
                                     build up |1> population cleanly.
"""

import qutip as qt


def build_collapse_operators(n_levels, kappa, gamma_phi):
    """
    Build the list of Lindblad collapse operators for a truncated bosonic
    mode.

    Parameters
    ----------
    n_levels : int
        Number of Fock levels kept in the truncated Hilbert space.
    kappa : float
        Photon loss rate.
    gamma_phi : float
        Photon dephasing rate.

    Returns
    -------
    list of qutip.Qobj
        Collapse operators [sqrt(kappa) * a, sqrt(gamma_phi) * a^dag a].
    """
    a = qt.destroy(n_levels)
    n_op = a.dag() * a

    c_ops = [
        (kappa ** 0.5) * a,
        (gamma_phi ** 0.5) * n_op,
    ]
    return c_ops

