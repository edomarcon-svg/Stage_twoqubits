"""Strict, serializable experiment configuration; frequencies are angular frequencies."""
from dataclasses import asdict, dataclass, field, fields
import json
import math
from pathlib import Path
import re


@dataclass
class Case:
    name: str = "1q"
    couplings: list[float] = field(default_factory=lambda: [0.3])
    qubit_frequencies: list[float] = field(default_factory=lambda: [2.0])
    control: str = "independent"
    direct_exchange: float = 0.0


@dataclass
class Target:
    kind: str = "fock"
    value: float = 6
    theta: float = 0.0
    squeezing_unit: str = "r"
    reset_qubits: bool = False


@dataclass
class Control:
    nodes: int = 81
    total_frequency_bounds: list[float] = field(default_factory=lambda: [0.5, 3.0])
    filter_cutoff: float | None = 3.0
    max_slew: float | None = None
    fluence_weight: float = 0.0
    slew_weight: float = 0.0


@dataclass
class Optimization:
    seeds: list[int] = field(default_factory=lambda: list(range(8)))
    frequencies: int = 20
    frequency_range: list[float] = field(default_factory=lambda: [0.05, 3.0])
    crab_max_evaluations: int = 1600
    grape_max_iterations: int = 200
    grape_max_evaluations: int = 1600
    refine_top: int | None = None
    workers: int = 1
    blas_threads: int = 1
    ftol: float = 1e-12
    gtol: float = 1e-7
    objective: str = "probability"
    objective_scale: float = 1.0
    root_epsilon: float = 1e-12
    crab_initial_std: float | None = None
    warm_starts: list[dict] = field(default_factory=list)


@dataclass
class Validation:
    dimension_increment: int = 20
    trajectory_points: int = 601
    atol: float = 1e-10
    rtol: float = 1e-10
    fidelity_tolerance: float = 1e-3
    truncation_tolerance: float = 1e-5
    edge_tolerance: float = 1e-5
    edge_levels: int = 5
    hold_time: float = 0.0
    phase_grid_points: int = 121
    hold_points: int = 201
    spectral_threshold: float = 3.0


@dataclass
class Experiment:
    name: str = "fock6"
    dimension: int = 40
    omega_c: float = 1.0
    duration: float = 104.71975511965978
    factor_taus: int | None = None
    tau_s_coupling: float = 0.3
    intervals: int = 800
    initial_state: str = "bare"
    parity_reduction: bool = True
    target_probability_goal: float = 0.99
    cases: list[Case] = field(default_factory=lambda: [Case()])
    target: Target = field(default_factory=Target)
    control: Control = field(default_factory=Control)
    optimization: Optimization = field(default_factory=Optimization)
    validation: Validation = field(default_factory=Validation)

    def to_dict(self):
        return asdict(self)

    @property
    def tau_s(self):
        return math.pi / (2 * self.tau_s_coupling)

    def validate(self):
        if (isinstance(self.tau_s_coupling, bool)
                or not isinstance(self.tau_s_coupling, (int, float))
                or not math.isfinite(self.tau_s_coupling) or self.tau_s_coupling <= 0):
            raise ValueError("tau_s_coupling must be finite and positive")
        if self.factor_taus is not None:
            if isinstance(self.factor_taus, bool) or not isinstance(self.factor_taus, int) or self.factor_taus < 1:
                raise ValueError("factor_taus must be a positive integer or null")
            self.duration = self.factor_taus * self.tau_s
        integer_fields = [(self, ["dimension", "intervals"]), (self.control,["nodes"]),
            (self.optimization,["frequencies","crab_max_evaluations","grape_max_iterations","grape_max_evaluations","workers","blas_threads"]),
            (self.validation,["dimension_increment","trajectory_points","edge_levels","phase_grid_points","hold_points"])]
        for obj,names in integer_fields:
            for name in names:
                value = getattr(obj,name)
                if not isinstance(value,int) or isinstance(value,bool):
                    raise ValueError(f"{name} must be an integer")
        if self.optimization.refine_top is not None and (not isinstance(self.optimization.refine_top,int) or isinstance(self.optimization.refine_top,bool)):
            raise ValueError("refine_top must be an integer or null")
        if not self.name or not isinstance(self.name, str):
            raise ValueError("name must be a nonempty string")
        if self.dimension < 3 or self.intervals < 2:
            raise ValueError("dimension >= 3 and intervals >= 2 required")
        if self.omega_c <= 0 or self.duration <= 0:
            raise ValueError("omega_c and duration must be positive")
        if self.initial_state not in {"bare", "ground"}:
            raise ValueError("initial_state must be bare or ground")
        if not 0 < self.target_probability_goal <= 1:
            raise ValueError("target_probability_goal must lie in (0, 1]")
        if not self.cases or len({c.name for c in self.cases}) != len(self.cases):
            raise ValueError("cases must have unique names")
        for c in self.cases:
            if not c.name or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for ch in c.name):
                raise ValueError("case names may contain only letters, digits, _ and -")
            if len(c.couplings) not in (1, 2) or len(c.couplings) != len(c.qubit_frequencies):
                raise ValueError("each case needs 1 or 2 couplings and matching qubit_frequencies")
            if c.control not in {"common", "independent"}:
                raise ValueError("control must be common or independent")
            if len(c.couplings) == 1 and c.direct_exchange != 0:
                raise ValueError("direct_exchange requires two qubits")
        t = self.target
        if t.kind not in {"fock", "squeezed", "cat"}:
            raise ValueError("target kind must be fock, squeezed or cat")
        if t.kind == "fock" and (t.value != int(t.value) or not 0 <= t.value < self.dimension):
            raise ValueError("Fock target must be an integer in [0, dimension)")
        if t.kind == "cat" and t.value <= 0:
            raise ValueError("cat alpha must be positive (alpha=0 is singular)")
        if t.kind == "squeezed" and t.value < 0:
            raise ValueError("squeezing strength must be nonnegative")
        if t.squeezing_unit not in {"r", "dB"}:
            raise ValueError("squeezing_unit must be r or dB")
        if t.squeezing_unit != "r" and t.kind != "squeezed":
            raise ValueError("dB units apply only to squeezed targets")
        u = self.control
        if u.nodes < 3 or u.nodes > self.intervals + 1:
            raise ValueError("3 <= control.nodes <= intervals + 1 required")
        if len(u.total_frequency_bounds) != 2 or not 0 < u.total_frequency_bounds[0] < u.total_frequency_bounds[1]:
            raise ValueError("total_frequency_bounds must satisfy 0 < lower < upper")
        for c in self.cases:
            if any(not u.total_frequency_bounds[0] < w < u.total_frequency_bounds[1] for w in c.qubit_frequencies):
                raise ValueError("each bare qubit frequency must lie strictly inside the total-frequency bounds")
        if u.filter_cutoff is not None and u.filter_cutoff <= 0:
            raise ValueError("filter_cutoff must be positive or null")
        if u.max_slew is not None and u.max_slew <= 0:
            raise ValueError("max_slew must be positive or null")
        if min(u.fluence_weight, u.slew_weight) < 0:
            raise ValueError("regularization weights must be nonnegative")
        o = self.optimization
        if not o.seeds or any(not isinstance(s, int) or isinstance(s, bool) or s < 0 for s in o.seeds) or len(set(o.seeds)) != len(o.seeds):
            raise ValueError("seeds must be distinct nonnegative integers")
        if o.frequencies < 1 or len(o.frequency_range) != 2 or not 0 <= o.frequency_range[0] < o.frequency_range[1]:
            raise ValueError("invalid CRAB frequencies")
        if min(o.crab_max_evaluations, o.grape_max_iterations, o.grape_max_evaluations, o.workers, o.blas_threads) < 1:
            raise ValueError("optimization budgets and worker/thread counts must be positive")
        if o.refine_top is not None and not 1 <= o.refine_top <= len(o.seeds):
            raise ValueError("refine_top must be null or between 1 and number of seeds")
        if min(o.ftol, o.gtol) <= 0:
            raise ValueError("optimizer tolerances must be positive")
        if o.objective not in {"probability", "root"}:
            raise ValueError("objective must be probability or root")
        if min(o.objective_scale, o.root_epsilon) <= 0 or (o.crab_initial_std is not None and o.crab_initial_std <= 0):
            raise ValueError("objective scale, root epsilon and initial std must be positive")
        names = set()
        for warm in o.warm_starts:
            if set(warm)-{"name","case","path","format","rescale_time"} or not {"name","case","path","format"} <= set(warm):
                raise ValueError("Invalid warm_start fields")
            name = warm["name"]
            if not isinstance(name,str) or not name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in name) or name in names:
                raise ValueError("warm_start names must be unique safe names")
            names.add(name)
            if warm["case"] not in {c.name for c in self.cases} or not isinstance(warm["path"],str) or not warm["path"]:
                raise ValueError("warm_start requires an existing case and a path")
            if warm["format"] not in {"v2", "legacy_crab", "legacy_grape", "legacy_smooth"}:
                raise ValueError("Unsupported warm_start format")
            if not isinstance(warm.get("rescale_time",False),bool):
                raise ValueError("rescale_time must be boolean")
        v = self.validation
        if v.hold_points < 2 or v.spectral_threshold <= 0:
            raise ValueError("hold_points >= 2 and spectral_threshold > 0 required")
        if v.dimension_increment < 2 or v.trajectory_points < 3 or not 1 <= v.edge_levels < self.dimension or v.phase_grid_points < 21:
            raise ValueError("invalid validation grids or edge_levels")
        if min(v.atol, v.rtol, v.fidelity_tolerance, v.truncation_tolerance, v.edge_tolerance) <= 0 or v.hold_time < 0:
            raise ValueError("validation tolerances must be positive; hold_time >= 0")
        # No NaN/Inf may enter a configuration or its saved JSON.
        json.dumps(self.to_dict(), allow_nan=False)
        return self


def _strict(cls, data):
    names = {f.name for f in fields(cls)}
    unknown = set(data) - names
    if unknown:
        raise ValueError(f"Unknown {cls.__name__} fields: {sorted(unknown)}")
    return cls(**data)


def from_dict(data):
    d = dict(data)
    for key, cls in [("target", Target), ("control", Control), ("optimization", Optimization), ("validation", Validation)]:
        if key in d:
            d[key] = _strict(cls, d[key])
    if "cases" in d:
        d["cases"] = [_strict(Case, x) for x in d["cases"]]
    return _strict(Experiment, d).validate()


def _without_json_comments(text):
    """Remove JSONC comments, preserving strings and diagnostic line/column positions."""
    tokens = re.compile(r'"(?:\\.|[^"\\])*"|//[^\r\n]*|/\*[\s\S]*?(?:\*/|\Z)')

    def replace(match):
        token = match.group()
        if token.startswith('"'):
            return token
        if token.startswith("/*") and not token.endswith("*/"):
            raise json.JSONDecodeError("Unterminated JSONC block comment", text, match.start())
        return "".join(c if c in "\r\n" else " " for c in token)

    return tokens.sub(replace, text)


def load_config(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonc":
        text = _without_json_comments(text)
    raw = json.loads(text)
    for warm in raw.get("optimization", {}).get("warm_starts", []):
        warm["path"] = str((path.parent / warm["path"]).resolve())
    return from_dict(raw)
