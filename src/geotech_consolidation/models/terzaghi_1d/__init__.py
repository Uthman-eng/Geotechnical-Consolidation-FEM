"""1D single-layer Terzaghi consolidation: FEM and analytical (Fourier series) solvers."""

from .analytical import Get_terzaghi1d_Analytical
from .fem import Get_terzaghi1D_FEA
from .u0_analytical import Get_terzaghi1d_Analytical_u0

__all__ = [
    "Get_terzaghi1D_FEA",
    "Get_terzaghi1d_Analytical",
    "Get_terzaghi1d_Analytical_u0",
]
