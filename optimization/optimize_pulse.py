"""
optimization/optimize_pulse.py

Uses SciPy's L-BFGS-B to tune the pulse amplitude. As in the qubit
version of this project, this is not a search for a bigger number -- it
is a search for the drive strength that best balances coherent buildup
of the |1> Fock population against continuous photon loss and dephasing
over a fixed pulse duration. The landscape is nontrivial precisely
because too small an amplitude under-drives the mode, and too large an
amplitude overshoots into higher Fock states (and back down again)
before the pulse ends.
"""

from scipy.optimize import minimize

from simulation.pulse_simulator import run_simulation


def _negative_fidelity(amplitude_array, config):
    """
    Objective function for the minimizer. SciPy minimizes, so the sign is
    flipped on the fidelity to turn "maximize fidelity" into "minimize
    negative fidelity".
    """
    amplitude = amplitude_array[0]
    fidelity, _ = run_simulation(amplitude, config, return_states=False)
    return -fidelity


def optimize_pulse_amplitude(config, initial_guess=None, bounds=(0.05, 5.0)):
    """
    Optimize the Gaussian pulse amplitude to maximize final-state fidelity
    with the target Fock state.

    Parameters
    ----------
    config : module
        The system_config module.
    initial_guess : float, optional
        Starting amplitude for L-BFGS-B. Defaults to config.INITIAL_AMPLITUDE.
    bounds : tuple
        (min_amplitude, max_amplitude) search bounds. Amplitude is kept
        positive and bounded above to avoid the optimizer wandering into
        physically extreme drive strengths that would require a much
        larger Fock-space truncation to represent accurately.

    Returns
    -------
    optimal_amplitude : float
    optimal_fidelity : float
    """
    if initial_guess is None:
        initial_guess = config.INITIAL_AMPLITUDE

    result = minimize(
        _negative_fidelity,
        x0=[initial_guess],
        args=(config,),
        method="L-BFGS-B",
        bounds=[bounds],
    )

    optimal_amplitude = result.x[0]
    optimal_fidelity = -result.fun

    return optimal_amplitude, optimal_fidelity
