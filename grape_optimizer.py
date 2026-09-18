from dataclasses import dataclass
from typing import List
import numpy as np
from qutip import Qobj, commutator
from scipy.optimize import minimize
import logging

# ====================================
# Logger configuration
# ====================================
logger = logging.getLogger(__name__)  # Create a logger associated with this module
logger.setLevel(logging.INFO)         # Default logging level
if not logger.hasHandlers():          # Avoid duplicate handlers
    ch = logging.StreamHandler()      # StreamHandler prints to console
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# ====================================
# Result container
# ====================================
@dataclass
class GRAPEResult:
    """
    Data container for storing GRAPE optimization results.
    """
    control_pulses: List[np.ndarray]   # List of optimized control pulses
    final_fidelity: float              # Final fidelity of the optimized pulse
    iterations: int                    # Number of iterations performed
    success: bool                     
    message: str                       # Optional message about the optimization

# ===================================
# GRAPE Optimizer
# ===================================
class GRAPEOptimizer:
    """
    GRAPE (Gradient Ascent Pulse Engineering) optimizer.
    Supports multiple control Hamiltonians and modular optimization.
    """

    def __init__(
        self,
        H_drift: Qobj,               # Drift Hamiltonian
        H_controls: List[Qobj],      # List of control Hamiltonians
        T: float,                    # Total evolution time
        num_tslots: int = 50,        # Number of time steps
        omega_bases: List[float] = None,   # Base control amplitudes
        epsilon: float = 0.01,       # Gradient ascent step size
        seed: int = None,            # Random seed for reproducibility
        log_every: int = 100,        # Logging frequency in iterations
    ):
        self.H_drift = H_drift
        self.H_controls = H_controls
        self.n_controls = len(H_controls)       # Number of control Hamiltonians
        self.T = T
        self.num_tslots = num_tslots
        if omega_bases is None:
            self.omega_bases = [1.0] * self.n_controls  # default 1.0 for all
        elif len(omega_bases) != self.n_controls:
            raise ValueError(f"omega_bases must have length {self.n_controls}")
        else:
            self.omega_bases = omega_bases
        self.epsilon = epsilon
        self.tlist = np.linspace(0, T, num_tslots)   # Time grid from 0 to T
        self.dt = self.tlist[1] - self.tlist[0]      # Time step size
        self.rng = np.random.default_rng(seed)       # Random generator
        self.log_every = log_every                    # Logging frequency

    # --------------------------------------------------------
    # Generate random initial guess for controls
    # --------------------------------------------------------
    def initial_guess(self):
        """
        Returns a list of random initial control pulses for all Hamiltonians.
        Each pulse is centered around u_base with random noise added.
        """
        return [
            self.omega_bases[i] + self.rng.uniform(-5, 5, self.num_tslots)
            for i in range(self.n_controls)
        ]

    # --------------------------------------------------------
    # Forward propagation
    # --------------------------------------------------------
    def forward_propagation(self, controls, psi0):
        """
        Propagates the system density matrix forward in time using the controls.
        Returns the list of states at each timestep.
        """
        rho_list = [psi0]  # Start with initial state
        for t in range(self.num_tslots):
            H_total = self.H_drift
            # Add contributions from all control Hamiltonians at this time step
            for k, Hc in enumerate(self.H_controls):
                H_total += controls[k][t] * Hc
            # Exponentiate Hamiltonian to get unitary evolution for this step
            U = (-1j * H_total * self.dt).expm()
            # Propagate density matrix
            rho_list.append(U * rho_list[-1] * U.dag())
        return rho_list

    # --------------------------------------------------------
    # Backward propagation
    # --------------------------------------------------------
    def backward_propagation(self, controls, target_state):
        """
        Backward propagates the target state in time for gradient calculation.
        Returns the list of lambda states at each timestep.
        """
        lambda_list = [None] * (self.num_tslots + 1)
        lambda_list[-1] = target_state   # Final condition is the target state
        for t in reversed(range(self.num_tslots)):
            H_total = self.H_drift
            # Include all controls at this timestep
            for k, Hc in enumerate(self.H_controls):
                H_total += controls[k][t] * Hc
            # Compute unitary for this step
            U = (-1j * H_total * self.dt).expm()
            # Backward propagation formula
            lambda_list[t] = U.dag() * lambda_list[t + 1] * U
        return lambda_list

    # --------------------------------------------------------
    # Compute fidelity gradients
    # --------------------------------------------------------
    def compute_gradients(self, rho_list, lambda_list):
        """
        Compute gradients of the fidelity w.r.t each control pulse at all time steps.
        """
        gradients = [np.zeros(self.num_tslots) for _ in range(self.n_controls)]
        for k, Hc in enumerate(self.H_controls):
            for t in range(self.num_tslots):
                comm = commutator(Hc, rho_list[t])   # Commutator [Hc, rho]
                grad = -(lambda_list[t].dag() * (1j * self.dt * comm)).tr()  # Fidelity gradient
                gradients[k][t] = np.real(grad)      # Store real part
        return gradients

    # --------------------------------------------------------
    # Gradient ascent optimization
    # --------------------------------------------------------
    def optimize_gradient_ascent(
        self,
        psi0: Qobj,
        target_state: Qobj,
        max_iter: int = 1000,
        tol: float = 1e-8,
        goal: float = 0.999,
        initial_guess: list = None,   # Optional user-provided initial guess
    ) -> GRAPEResult:

        # Use random guess if none provided
        if initial_guess is None:
            controls = self.initial_guess()
        else:
            if len(initial_guess) != self.n_controls:
                raise ValueError(f"initial_guess must contain {self.n_controls} arrays")
            controls = []
            for i in range(self.n_controls):
                # time grid of the provided guess
                t_initial_guess = np.linspace(0, self.T, len(initial_guess[i]))
                # interpolate onto optimizer time grid
                interpolated = np.interp(self.tlist, t_initial_guess, initial_guess[i])
                controls.append(interpolated)

        F_prev = 0.0   # Previous fidelity for convergence check

        for it in range(1, max_iter + 1):
            # Forward and backward propagation
            rho_list = self.forward_propagation(controls, psi0)
            lambda_list = self.backward_propagation(controls, target_state)
            # Compute gradients
            gradients = self.compute_gradients(rho_list, lambda_list)

            # Update controls using gradient ascent
            for k in range(self.n_controls):
                controls[k] += self.epsilon * gradients[k]

            # Compute fidelity
            F_final = (target_state.dag() * rho_list[-1]).tr().real

            # Logging every log_every iterations
            if it % self.log_every == 0 or it == 1:
                logger.info(f"Iteration {it}, Fidelity: {F_final:.8f}")

            # Check for convergence or goal reached
            if abs(F_final - F_prev) < tol:
                logger.info(f"Convergence reached at iteration {it}, Fidelity: {F_final:.8f}")
                return GRAPEResult(controls, F_final, it, True, "Convergence reached")
            if F_final >= goal:
                logger.info(f"Target fidelity reached at iteration {it}, Fidelity: {F_final:.8f}")
                return GRAPEResult(controls, F_final, it, True, "Target fidelity reached")

            F_prev = F_final

        # Return result if max iterations reached without convergence
        return GRAPEResult(controls, F_final, max_iter, False, "Maximum iterations reached")

    # --------------------------------------------------------
    # L-BFGS-B optimization
    # --------------------------------------------------------
    def optimize_minimize(
        self,
        psi0: Qobj,
        target_state: Qobj,
        amp_bound=(0, 10.0),
        max_iter: int = 500,
        initial_guess: np.ndarray = None  # Optional initial guess
    ) -> GRAPEResult:


# Use random guess if none provided
        if initial_guess is None:
            controls = self.initial_guess()
        else:
            if len(initial_guess) != self.n_controls:
                raise ValueError(f"initial_guess must contain {self.n_controls} arrays")
            controls = []
            for i in range(self.n_controls):
                # time grid of the provided guess
                t_initial_guess = np.linspace(0, self.T, len(initial_guess[i]))
                # interpolate onto optimizer time grid
                interpolated = np.interp(self.tlist, t_initial_guess, initial_guess[i])
                controls.append(interpolated)


       # Generate initial guess if not provided
        if initial_guess is None:
            initial_guess = []
            for _ in range(self.n_controls):
                initial_guess.extend(
                    self.rng.uniform(amp_bound[0], amp_bound[1], self.num_tslots - 2)
                )
            initial_guess = np.array(initial_guess)
        else:
            if len(initial_guess) != self.n_controls:
                raise ValueError(f"initial_guess must contain {self.n_controls} arrays")
            flat_guess = []
            for i in range(self.n_controls):
                pulse = np.asarray(initial_guess[i])
                t_initial = np.linspace(0, self.T, len(pulse))
                interp_pulse = np.interp(self.tlist, t_initial, pulse)
                flat_guess.extend(interp_pulse[1:-1])  # only inner points
            initial_guess = np.array(flat_guess)

        bounds = [amp_bound] * len(initial_guess)

        # Objective function for L-BFGS-B
        def objective(inner_controls_flat):
            inner_controls = []
            for k in range(self.n_controls):
                start = k * (self.num_tslots - 2)
                end = start + (self.num_tslots - 2)
                ctrl = np.zeros(self.num_tslots)
                ctrl[0] = self.omega_bases[k]
                ctrl[-1] = self.omega_bases[k]
                ctrl[1:-1] = inner_controls_flat[start:end]  # inner time steps
                inner_controls.append(ctrl)

            # Forward propagation and fidelity
            rho_list = self.forward_propagation(inner_controls, psi0)
            F = (target_state.dag() * rho_list[-1]).tr().real

            # Backward propagation for gradients
            lambda_list = self.backward_propagation(inner_controls, target_state)
            gradients = self.compute_gradients(rho_list, lambda_list)

            # Flatten gradients for optimizer (exclude boundaries)
            grad_flat = []
            for g in gradients:
                grad_flat.extend(g[1:-1])
            return 1 - F, -np.array(grad_flat)

        # Run SciPy L-BFGS-B optimizer
        result = minimize(
            objective,
            initial_guess,
            method="L-BFGS-B",
            jac=True,
            bounds=bounds,
            options={"maxiter": max_iter, "disp": True}
        )

        # Reconstruct optimized control pulses
        optimized_controls = []
        for k in range(self.n_controls):
            start = k * (self.num_tslots - 2)
            end = start + (self.num_tslots - 2)
            ctrl = np.zeros(self.num_tslots)
            ctrl[0] = self.omega_bases[k]       # use base amplitude per control
            ctrl[-1] = self.omega_bases[k]
            ctrl[1:-1] = result.x[start:end]
            optimized_controls.append(ctrl)

        final_fidelity = 1 - result.fun
        return GRAPEResult(
            control_pulses=optimized_controls,
            final_fidelity=final_fidelity,
            iterations=result.nit,
            success=result.success,
            message=result.message
        )
