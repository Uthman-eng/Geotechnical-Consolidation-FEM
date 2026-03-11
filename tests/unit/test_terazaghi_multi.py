import numpy as np
import pytest

pytest.importorskip("dolfinx")
pytest.importorskip("mpi4py")

from src.geotech_consolidation.models.run import run_terazaghi_multilayer


def test_multilayer_model_runs():
    result = run_terazaghi_multilayer(
        H=10.0,
        depths=[0.0, 5.0, 10.0],
        Cv=[1e-3, 5e-4],
        Mv=[1e-4, 2e-4],
        q=100.0,
        t_final=10.0,
        num=21,
        n_steps=11,
    )

    assert "u_hist" in result
    assert "z" in result
    assert "t" in result
    assert "settlement" in result
    assert "kappa_profile" in result
    assert "Mv_profile" in result
    assert result["u_hist"].shape[0] == result["t"].shape[0]
    assert result["u_hist"].shape[1] == result["z"].shape[0]
    assert result["settlement"].shape == result["z"].shape
    assert result["kappa_profile"].shape == result["z"].shape
    assert result["Mv_profile"].shape == result["z"].shape
    assert np.all(np.isfinite(result["settlement"]))
    assert np.isclose(result["kappa_profile"][0], 1e-3)
    assert np.isclose(result["kappa_profile"][-1], 5e-4)
    assert np.isclose(result["Mv_profile"][0], 1e-4)
    assert np.isclose(result["Mv_profile"][-1], 2e-4)
