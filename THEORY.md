# Theory & Verification

This document summarises the mathematical formulation implemented in this repo and the verification/validation results reported in the dissertation
(*Finite Element Modelling of Consolidation Settlement: Implementation, Verification and Open-Source Delivery*, Aziz, 2026). The sections and equations here refer to that dissertation. This file reports, rather than re-derives, the methodology and equations. For implementation see [src/geotech_consolidation/models/](src/geotech_consolidation/models/); for verification see [notebooks/](notebooks/) and [demo/](demo/) (Settle3 comparisons).

## 1. Governing equation and assumptions

Terzaghi 1D consolidation is uncoupled, a linear parabolic PDE, structurally identical to the heat equation.

**Terzaghi PDE:**

$$\frac{\partial u}{\partial t} = C_v \nabla^2 u$$

**Coefficient of consolidation:**

$$c_v = \frac{k}{m_v \gamma_w}$$

With $u$ excess pore pressure, $k$ hydraulic conductivity, $m_v$ coefficient of volume compressibility, $\gamma_w = 9.81\ \text{kN/m}^3$.

**Assumptions:** 1D strain, small deformation, full saturation, incompressible grains and pore fluid, Darcy flow, homogeneous properties. This extends to multi-layer cases using piecewise-constant properties per layer.

## 2. Analytical reference solutions

**Uniform initial condition** (*single drainage at the ground boundary*):

$$u_e(z,t) = \sum_{n=1}^{\infty} \frac{2u_i}{n\pi}\,(1 - \cos n\pi)\,\sin\!\left(\frac{n\pi z}{2d}\right)\exp\!\left(-\frac{n^2\pi^2 c_v t}{4d^2}\right)$$

**Generalised series** (*arbitrary `u0`*):

$$u(z,t) = \sum_{n=1,3,5,\dots} B_n \,\sin\!\left(\frac{n\pi z}{2H}\right) \exp\!\left(-\frac{n^2\pi^2 c_v t}{4H^2}\right)$$

**Generalised coefficient** (*$L^2$ orthogonal projection of `u0` onto each odd sine basis element*):

$$B_n = \frac{2}{H}\int_0^H u_0(z)\,\sin\!\left(\frac{n\pi z}{2H}\right)\,dz,
\qquad n = 1,3,5,\dots$$

The basis $\sin(n\pi z / 2H)$ satisfies the boundary conditions exactly and is orthogonal in $L^2([0,H])$. The integral for $B_n$ has **no closed form** for the
Boussinesq `u0` and is evaluated by trapezoidal quadrature, introducing aliasing behaviour (Section 8).

This solution and its quadrature are implemented and verified in [notebooks/0_Analytical_Fourier_Quadrature.ipynb](notebooks/0_Analytical_Fourier_Quadrature.ipynb).

## 3. Weak form and finite element formulation

**Weak integral form** *(with the boundary term vanishing):*

$$\int_\Omega v \frac{\partial u}{\partial t}\, dx + C_v \int_\Omega \nabla v \cdot \nabla u \, dx = 0$$

Pore pressure is approximated with **linear functions** (CG1, $p=1$). Backward Euler discretisation at each time step then becomes:

$$\int_\Omega v\, u^{n+1} \, dx + \Delta t\, C_v \int_\Omega \nabla v \cdot \nabla u^{n+1} \, dx
= \int_\Omega v\, u^n \, dx$$

where $u^n$ is the previous time step pore pressure, and $u^{n+1}$ is the next time step pore pressure.

## 4. Settlement post-processing

The variational formulation gives pore pressure, **not displacement**. Settlement is post-processed from the dissipated pore pressure field.

**Settlement integral**:

$$s(t) = \int_0^H m_v(z)\,[\,u_0(z) - u(z,t)\,]\, dz$$

This is evaluated numerically via **trapezoidal quadrature** over depth. For 2D, this integration is performed column-by-column through the nodal array to give a surface settlement profile. Settlement is measured only as downward displacement; other axes are ignored.

## 5. A priori convergence bounds

Error is measured in $L^2$ inner-product spaces, which FEM solutions naturally live in. Comparing the analytical and FEM solutions produces convergence plots and convergence rates against FEM theory.

**Interpolation error in $H^1$** *(Brenner & Scott, 2008, Theorem 5.4.4):*

$$\lVert u - u_h \rVert_{H^1} \le C\, h^{m-1}\, \lvert u \rvert_{H^m}$$

**Aubin–Nitsche duality lifts this to $L^2$**, gaining one power of $h$ *(Brenner & Scott, 2008, Theorem 5.4.8):*

$$\lVert u - u_h \rVert_{L^2} \le C\, h^{m}\, \lvert u \rvert_{H^m}$$

**Linear elements** ($p=1$) bring the bound to:

$$\lVert u - u_h \rVert_{L^2} \le C\, h^2\, \lvert u \rvert_{H^2}$$

$u$ is assumed smooth relative to the linear polynomial degree, so $m = p+1$ is appropriate.

Temporal convergence is first order, $O(\Delta t)$, from the backward Euler bound *(Larsson & Bengzon, 2013)*.

Convergence is verified in [notebooks/1_terzaghi_1d_singlelayer.ipynb](notebooks/1_terzaghi_1d_singlelayer.ipynb) and [notebooks/3_terzaghi_2d.ipynb](notebooks/3_terzaghi_2d.ipynb); results are summarised in Section 9.

## 6. Boundary and initial conditions

**Dirichlet** *(drained ground surface, post-loading):*

$$u = 0 \quad \text{on } \Gamma_D \subset \partial\Omega$$

**Neumann** *(impermeable base):*

$$\frac{\partial u}{\partial n} = 0 \quad \text{on } \Gamma_N \subset \partial\Omega$$

For 2D, lateral boundaries are treated as **freely draining** (not impermeable). Multi-layer interface pore-pressure continuity is satisfied through the shared mesh node.

The initial condition uses the Boussinesq strip-load stress field. In 1D this is simplified to directly beneath the centre of the load; in 2D the full stress field is used.

**1D Boussinesq strip-load stress** *(directly beneath the centre of the load)*:

$$\sigma_z(z) = \frac{2q}{\pi}\left[\arctan\!\left(\frac{B}{2z}\right)
+ \frac{Bz}{2z^2 + \tfrac{B^2}{2}}\right]$$

**2D Boussinesq strip-load stress field:**

$$\sigma_z(X,Z) = \frac{q}{\pi}\left[\arctan\!\left(\frac{X+B}{Z}\right)
- \arctan\!\left(\frac{X-B}{Z}\right)
+ Z\left(\frac{X+B}{(X+B)^2+Z^2} - \frac{X-B}{(X-B)^2+Z^2}\right)\right]$$

$Z$ is depth (positive down), $X$ is horizontal distance from the load centre, $B$ is the strip half-width.

## 7. Multi-layer interface: Darcy flux continuity

**Darcy flux:**

$$q = -\left(\frac{k}{\gamma_w}\right)\frac{\partial u}{\partial z}$$

Flux continuity across an interface requires:

$$k_1 \left.\frac{\partial u}{\partial z}\right|_- = k_2 \left.\frac{\partial u}{\partial z}\right|_+$$

Since $k_1 \neq k_2$, the pore-pressure gradient is discontinuous — the kink is a feature of the exact solution, not an FEM artefact (see [notebooks/2_terzaghi_1d_multilayer.ipynb](notebooks/2_terzaghi_1d_multilayer.ipynb)). Gradient jump magnitude (1D):

$$\left[\frac{\partial u}{\partial z}\right]
= \left.\frac{\partial u}{\partial z}\right|_+ \left(1 - \frac{k_2}{k_1}\right)$$

When $k_2 = k_1$ the jump vanishes (single-layer case recovered). Pore-pressure continuity is enforced through the shared CG1 node. Flux continuity is enforced only naturally (a known property of continuous Galerkin at material interfaces), whereas a mixed formulation would enforce it pointwise.

## 8. Nyquist aliasing of the Fourier benchmark

The generalised coefficients $B_m$ require trapezoidal quadrature over the discrete node array:

$$B_m \approx \Delta z \left[\tfrac{1}{2}f(z_0) + f(z_1) + \dots + f(z_{n-1}) + \tfrac{1}{2}f(z_n)\right]$$

Accurate $B_m$ requires the sine basis to be resolved on the mesh; otherwise **aliasing** appears. The Nyquist–Shannon sampling theorem gives $N_\text{crit} = N_\text{elements}$; below this, error emerges from the analytical solution itself (see [notebooks/0_Analytical_Fourier_Quadrature.ipynb](notebooks/0_Analytical_Fourier_Quadrature.ipynb)).

## 9. Verification & validation results

**Convergence rates summary**:

| Condition | Spatial slope | Temporal slope | Theory |
|---|---|---|---|
| Uniform `u0` | 2.015 | 1.032 | $O(h^2)$ <br> $O(\Delta t)$ |
| Boussinesq `u0` | 2.055 | 1.072 | $O(h^2)$ <br> $O(\Delta t)$ |

Both initial conditions recover the same slopes. The bound depends on solution smoothness, not on the initial condition.

**Settle3 validation** (see [demo/](demo/)):

- 1D single-layer and 1D multi-layer: within ~1% at all time points.
- 2D multi-layer: overpredicts by 7.83% at $t = 1\ \text{year}$, converging to ~0.91% by
  $t = 10\ \text{years}$.

## References

- Aziz, U. (2026). *Finite Element Modelling of Consolidation Settlement: Implementation, Verification and Open-Source Delivery* (BEng dissertation).
- Brenner, S. C., and Scott, L. R. (2008). *The Mathematical Theory of Finite Element Methods* (3rd ed.). Springer.
- Larsson, M. G., and Bengzon, F. (2013). *The Finite Element Method: Theory, Implementation, and Applications*. Springer.
- Craig, R. F. (2004). *Craig's Soil Mechanics* (7th ed.). Spon Press.
- Terzaghi, K. (1943). *Theoretical Soil Mechanics*. Wiley.
