"""Unambiguous state and actuator diagnostics; no hardware heat claims."""
import numpy as np
import qutip as qt


def state_metrics(model, state):
    full = model.expand(state)
    amp = full.reshape(model.dimension,2**model.nqubits)
    rho = amp @ amp.conj().T
    rq = amp.T @ amp.conj()
    p = np.diag(rho).real
    norm = float(np.vdot(full,full).real)
    cavity_p = float(np.vdot(model.target_cavity,rho @ model.target_cavity).real)
    objective_p = float(np.vdot(state,model.target_operator @ state).real)
    n = np.arange(model.dimension)
    parity = (-1.)**(np.repeat(n,2**model.nqubits)+np.tile([i.bit_count() for i in range(2**model.nqubits)],model.dimension))
    qpop = np.diag(rq).real
    excited = [float(sum(qpop[i] for i in range(len(qpop)) if (i >> (model.nqubits-1-j)) & 1)) for j in range(model.nqubits)]
    a = qt.destroy(model.dimension).full()
    x = (a+a.conj().T)/np.sqrt(2)
    p_op = (a-a.conj().T)/(1j*np.sqrt(2))
    def av(op):
        return float(np.trace(rho@op).real)
    vx, vp = av(x@x)-av(x)**2, av(p_op@p_op)-av(p_op)**2
    cov = av((x@p_op+p_op@x)/2)-av(x)*av(p_op)
    minvar = float(np.linalg.eigvalsh([[vx,cov],[cov,vp]])[0])
    eig = np.linalg.eigvalsh(rho)
    eig = eig[eig>1e-14]
    out = {"target_probability":objective_p,"fidelity_root":float(np.sqrt(np.clip(objective_p,0,1))),
           "cavity_target_probability":cavity_p,"cavity_fidelity_root":float(np.sqrt(np.clip(cavity_p,0,1))),
           "norm_error":abs(norm-1),"purity":float(np.trace(rho@rho).real),
           "cavity_entropy_nats":float(-np.sum(eig*np.log(eig))),
           "mean_photons":float(p@n),"photon_variance":float(p@(n*n)-(p@n)**2),
           "parity_expectation":float(np.sum(parity*abs(full)**2)),
           "parity_error":float(abs(np.sum(parity*abs(full)**2)-model.initial_parity)),
           "qubit_excited_populations":excited,"qubits_ground_probability":float(qpop[0]),
           "minimum_quadrature_variance":minvar,
           "squeezing_dB":float(-10*np.log10(2*minvar)) if minvar>0 else None}
    if model.nqubits == 2:
        qrho = qt.Qobj(rq,dims=[[2,2],[2,2]])
        out["qubit_concurrence"] = float(qt.concurrence(qrho))
        singlet = np.array([0,1,-1,0])/np.sqrt(2)
        out["singlet_population"] = float(np.vdot(singlet,rq@singlet).real)
    return out


def actuator_metrics(model, signal, nodes, points=4001, spectral_threshold=3.0):
    ts = np.linspace(0,signal.duration,points)
    modulation = model.physical_map @ signal.values(nodes,ts)
    rates = model.physical_map @ nodes @ signal.matrix(ts,derivative=True).T
    command = model.physical_map @ nodes
    metrics = []
    for j, delta in enumerate(modulation):
        u = delta+model.bare_frequencies[j]
        # Uniform endpoint-excluded samples; include the rFFT Nyquist bin.
        sampled = delta[:-1]-np.mean(delta[:-1])
        power = abs(np.fft.rfft(sampled))**2
        if len(power)>2:
            power[1:-1] *= 2
        omega = 2*np.pi*np.fft.rfftfreq(len(sampled),d=ts[1]-ts[0])
        power_above = float(power[omega > spectral_threshold].sum()/power.sum()) if power.sum() > 1e-24 else 0.
        omega99 = 0. if power.sum()<1e-24 else float(omega[min(np.searchsorted(np.cumsum(power)/power.sum(),.99),len(omega)-1)])
        metrics.append({"modulation_fluence":float(np.trapezoid(delta**2,ts)),
                        "total_frequency_fluence":float(np.trapezoid(u**2,ts)),
                        "slew_max_sampled":float(np.max(abs(rates[j]))),
                        "slew_rms":float(np.sqrt(np.trapezoid(rates[j]**2,ts)/signal.duration)),
                        "command_slew_max":float(np.max(abs(np.diff(command[j])))/signal.h),
                        "omega_99_ac":omega99,"ac_power_fraction_above_threshold":power_above,"spectral_threshold":spectral_threshold,"total_frequency_min":float(u.min()),
                        "total_frequency_max":float(u.max()),"terminal_modulation":float(delta[-1])})
    return {"channels":metrics,"modulation_fluence_total":sum(m["modulation_fluence"] for m in metrics),
            "normalized_hilbert_schmidt_control_cost":sum(m["modulation_fluence"] for m in metrics)/4,
            "modulation_fluence_max_channel":max(m["modulation_fluence"] for m in metrics),
            "total_frequency_fluence_total":sum(m["total_frequency_fluence"] for m in metrics),
            "omega_99_worst_channel":max(m["omega_99_ac"] for m in metrics),
            "slew_worst_channel":max(m["slew_max_sampled"] for m in metrics),
            "ac_power_fraction_above_threshold_worst":max(m["ac_power_fraction_above_threshold"] for m in metrics)}


def phase_space(model, rho, points):
    # Grid expands with occupation; report normalization error instead of silently
    # interpreting a clipped Wigner integral as a physical quantity.
    n = float(np.diag(rho).real@np.arange(model.dimension))
    limit = max(6., np.sqrt(2*max(n,0)+1)+4)
    grid = np.linspace(-limit,limit,points)
    w = qt.wigner(qt.Qobj(rho),grid,grid)
    integral = float(np.trapezoid(np.trapezoid(w,grid,axis=1),grid))
    absolute = float(np.trapezoid(np.trapezoid(abs(w),grid,axis=1),grid))
    return grid,w,{"wigner_integral":integral,"wigner_negative_volume":.5*(absolute-integral),
                   "wigner_integral_error":abs(integral-1)}
