import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.run import run_terazaghi_1d

def test_single_layer_model_runs():
    result = run_terazaghi_1d(
        H=10.0,
        Cv=1e-3,
        Mv=1e-4,
        q=100.0,
        t_final=10.0,
        num=21,
        n_steps=11,
    )

    assert "u_hist" in result
    assert "z" in result
    assert "t" in result
    assert "settlement" in result
    assert "kappa" in result
    assert result["u_hist"].shape[0] == result["t"].shape[0]
    assert result["u_hist"].shape[1] == result["z"].shape[0]
    assert result["settlement"].shape == result["z"].shape
    assert np.all(np.isfinite(result["settlement"]))
