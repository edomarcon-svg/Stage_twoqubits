import numpy as np
import logging
from dataclasses import dataclass
from typing import Callable, List, Optional
from scipy.optimize import minimize
from qutip import Qobj

logger = logging.getLogger(__name__) # Create a logger associated with this module's name


# ============================================================
# Result container
# ============================================================

# Dataclass automatically generates __init__, __repr__, etc.
# This class is just a structured container for optimization results

@dataclass
class CRABResult:
    control_pulses: List[np.ndarray] # list of optimized control pulses
    optimal_parameters: np.ndarray # final optimized parameter vector
    final_state: float # final state
    final_cost: float # final cost function value
    success: bool 
    message: str # message returned by the optimizer


# ============================================================
# CRAB Optimizer
# ============================================================

class CRABOptimizer:
    """
    CRAB (Chopped Random Basis) optimizer for quantum optimal control.
    This class builds control pulses as truncated random Fourier series and optimizes their coefficients.
    ----------
    Parameters
    ----------
    H_drift : Qobj
        Drift Hamiltonian.
    H_controls : list of Qobj
        List of control Hamiltonians.
    T : float
        Total evolution time.
    num_tslots : int
        Number of time grid points.
    num_freqs : int
        Number of Fourier components per control.
    freq_range : tuple
        Frequency range for uniform sampling.
    omega_bases : list of floats
        Base amplitudes for control pulses.
    basis_type : str
        'fourier' or 'uniform'.
    boundary_sigma : float
        Width of boundary suppression function.
    seed : int or None
        Random seed.
    solver : callable
        QuTiP solver (e.g. sesolve or mesolve).
    solver_options : dict or None
        Extra options for solver.
    """

    def __init__(
        self,
        H_drift: Qobj,
        H_controls: List[Qobj],
        T: float,
        num_tslots: int = 200,
        num_freqs: int = 5,
        freq_range: tuple = (0.1, 10.0),
        omega_bases: Optional[List[float]] = [2.0],
        basis_type: str = "fourier",
        boundary_sigma: float = 0.7,
        seed: Optional[int] = None,
        solver: Callable = None,
        solver_options: Optional[dict] = None,
    ):

        self.H_drift = H_drift
        self.H_controls = H_controls
        self.n_controls = len(H_controls) # number of control Hamiltonians

        self.T = T
        self.num_tslots = num_tslots
        self.tlist = np.linspace(0, T, num_tslots) # create time grid from 0 to T

        self.num_freqs = num_freqs
        self.freq_range = freq_range
        if len(omega_bases) == 1:
            self.omega_bases = [omega_bases[0]] * self.n_controls
        elif len(omega_bases) == self.n_controls:
            self.omega_bases = omega_bases
        else:
            raise ValueError("Length of omega_bases must be 1 or equal to number of controls")
        self.basis_type = basis_type
        self.boundary_sigma = boundary_sigma

        self.rng = np.random.default_rng(seed) # create a random number generator

        from qutip import sesolve
        self.solver = solver if solver is not None else sesolve # default solver: sesolve
        self.solver_options = solver_options or {} # store solver options

        # self.freqs = self._generate_frequencies() # generate initial random frequencies

    # =============================
    # Main optimization method
    # =============================

    def optimize(
        self,
        psi0: Qobj, # initial quantum state 
        cost_function: Callable, # user-defined cost function
        max_iter: int = 5000, # maximum optimizer iterations
        method: str = "Nelder-Mead", # optimization method 
        initial_guess: Optional[np.ndarray] = None, 
        clip_neg: bool = False,
        val_clip_neg: Optional[float] = None,
        clip_pos: bool = False,
        val_clip_pos: Optional[float] = None,
    ) -> CRABResult: 

        # if no initial guess is provided, generate a random one
        if initial_guess is None:
            initial_guess = self._random_initial_guess()
            
        # self.freqs = self._generate_frequencies() 
        self.freqs = [self._generate_frequencies() for _ in range(self.n_controls)] # generate frequencies for this optimization run

        # define objective function for SciPy optimizer
        def objective(params):
            pulses = self._build_all_controls(params, clip_neg, val_clip_neg, clip_pos, val_clip_pos) # build control pulses from parameters
            H = self._build_hamiltonian(pulses) # build time-dependent Hamiltonian

            result = self.solver(H, psi0, self.tlist, **self.solver_options) # solve Schrodinger equation
            final_state = result.states[-1] # extract final quantum state

            return cost_function(final_state, pulses) # cost value (puulses in case I want to add a penalty on negative pulses values) 
 
        opt = minimize(
            objective,
            initial_guess,
            method=method,
            options={"maxiter": max_iter},
        )

        # build optimal pulses from optimized parameters
        optimal_pulses = self._build_all_controls(opt.x, clip_neg, val_clip_neg, clip_pos, val_clip_pos)

        # run final simulation with optimal pulses
        final_result = self.solver(
            self._build_hamiltonian(optimal_pulses),
            psi0,
            self.tlist,
            **self.solver_options,
        )

        # extract final state
        final_state = final_result.states[-1]
        # compute final cost
        final_cost = cost_function(final_state, optimal_pulses)  

        # return structured result object
        return CRABResult(
            control_pulses=optimal_pulses,
            optimal_parameters=opt.x,
            final_state=final_state,
            final_cost=final_cost,
            success=opt.success,
            message=opt.message,
        )

    # ========================================================
    # Internal methods
    # ========================================================

    def _generate_frequencies(self):

        # uniform random frequencies
        if self.basis_type == "uniform":
            return self.rng.uniform(
                self.freq_range[0],
                self.freq_range[1],
                self.num_freqs,
            )
        
        # CRAB-style randomized Fourier frequencies
        elif self.basis_type == "fourier":
            r = self.rng.uniform(-0.5, 0.5, self.num_freqs)
            return np.array(
                [(i + r[i]) * 2 * np.pi / self.T for i in range(self.num_freqs)]
            )

        else:
            raise ValueError("Unsupported basis_type")

    # def _generate_frequencies(self):
     
    #     n_rand = self.num_freqs // 2
    #     n_peak = self.num_freqs - n_rand

    #     # frequenze casuali
    #     rand_freqs = self.rng.uniform(
    #         self.freq_range[0],
    #         self.freq_range[1],
    #         n_rand
    #     )

    #     # frequenze attorno a 2 omega_c
    #     omega_c = 1.0  
    #     peak_freqs = self.rng.uniform(
    #         1.5 * omega_c,
    #         2.5 * omega_c,
    #         n_peak
    #     )

    #     return np.concatenate([rand_freqs, peak_freqs])

    def _random_initial_guess(self):
        # total number of optimization parameters
        size = 2 * self.num_freqs * self.n_controls
        return self.rng.uniform(-0.5, 0.5, size) # random coefficients between -0.5 and 0.5

    def _boundary_function(self, t):
        # boundary suppression width
        sigma = self.boundary_sigma
        # smoothly suppress pulse at t=0 and t=T
        return (
            (1 - np.exp(-(t / sigma) ** 2))
            * (1 - np.exp(-((t - self.T) / sigma) ** 2))
        )

    # def _basis(self, t, coeffs_a, coeffs_b):
    #     # Fourier series: sum of sin and cos components
    #     return np.sum(
    #         coeffs_a * np.sin(self.freqs * t)
    #         + coeffs_b * np.cos(self.freqs * t)
    #     )
    def _basis(self, t, coeffs_a, coeffs_b, freqs):
        # Fourier series: sum of sin and cos components
        return np.sum(
            coeffs_a * np.sin(freqs * t)
            + coeffs_b * np.cos(freqs * t)
        )

    # def _build_single_control(self, params_block):
    #     # split parameter block into sin and cos coefficients
    #     coeffs_a = params_block[: self.num_freqs]
    #     coeffs_b = params_block[self.num_freqs :]

    #     # build pulse over full time grid
    #     pulse = np.array(
    #         [
    #             # self.omega_base + # constant offset
    #             self._basis(t, coeffs_a, coeffs_b)
    #             * self._boundary_function(t)
    #             for t in self.tlist
    #         ]
    #     )

    #     return pulse
    def _build_single_control(self, params_block, freqs):

        coeffs_a = params_block[: self.num_freqs]
        coeffs_b = params_block[self.num_freqs:]

        pulse = np.array([
            self._basis(t, coeffs_a, coeffs_b, freqs)
            * self._boundary_function(t)
            for t in self.tlist
        ])

        return pulse
    
    
    def _build_all_controls(self, params, clip_neg, val_clip_neg, clip_pos, val_clip_pos):

        pulses = []
        block_size = 2 * self.num_freqs
        for i in range(self.n_controls):
            block = params[i * block_size : (i + 1) * block_size]
            pulse = self.omega_bases[i] + self._build_single_control(block, self.freqs[i])

            if clip_neg:
                pulse = np.clip(pulse, val_clip_neg, None)
            if clip_pos:
                pulse = np.clip(pulse, None, val_clip_pos)

            pulses.append(pulse)

        return pulses

    def _build_hamiltonian(self, pulses):
        # start with drift Hamiltonian
        H = [self.H_drift]

        # Add time-dependent control terms
        for Hc, pulse in zip(self.H_controls, pulses):
            # Format required by QuTiP:
            # [H_control, time-dependent coefficient array]
            H.append([Hc, pulse])

        return H

