"""
pulses/pulse_shapes.py

Waveform generation is kept in its own module, isolated from the physics
of the simulation itself. This is the one piece of the pipeline a hardware
engineer would redesign first when moving to more advanced pulse families
(e.g. flat-top pulses with smooth edges, or shapes tailored to suppress
leakage into higher Fock states).
"""

import numpy as np


def gaussian_envelope(t, amplitude, center, sigma):
    """
    Gaussian-shaped drive envelope Omega(t).

    Omega(t) = A * exp( -(t - t0)^2 / (2 * sigma^2) )

    A smooth, continuously differentiable envelope avoids the sharp
    turn-on/turn-off transients that a square pulse would introduce.
    Sharp discontinuities carry broadband spectral content that can drive
    unwanted transitions into higher Fock levels of the truncated
    oscillator -- the bosonic-mode analogue of unwanted qubit leakage.

    Parameters
    ----------
    t : float or np.ndarray
        Time (or array of times) at which to evaluate the envelope.
    amplitude : float
        Peak drive amplitude A.
    center : float
        Pulse center t0.
    sigma : float
        Pulse width.

    Returns
    -------
    float or np.ndarray
        Drive envelope value(s) at time(s) t.
    """
    return amplitude * np.exp(-((t - center) ** 2) / (2 * sigma ** 2))

