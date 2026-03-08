import numpy as np

def terzaghi(u0, H, Tx, time_step, nodes, Cv, n_terms):
    u0 = np.array(u0, dtype=float)
    Z = np.linspace(0, H, nodes)                 
    p_data = np.zeros((time_step, nodes), dtype=float)
    T = np.linspace(0, Tx, time_step, dtype=float)
    Bm_data = np.zeros(n_terms, dtype=float)

    for n in range(n_terms):
        m = (2 * n) + 1
        Bm_data[n] = (2.0 / H) * np.trapz(
            u0 * np.sin((np.pi * m * Z) / (2.0 * H)),
            Z
        )

    for i in np.arange(nodes):
        z = Z[i]

        for j in np.arange(len(T)):
            t = T[j]
            S = 0.0

            for n in range(n_terms):
                m = (2 * n) + 1
                Bm = Bm_data[n]
                S += np.sin((m * np.pi * z) / (2.0 * H)) * np.exp(-((m**2) * (np.pi**2) * Cv * t) / (4.0 * (H**2))) * Bm 
                 
            p_data[j, i] = S
    return p_data, Z, T


def Get_Terazaghi1d_Analytical_u0(u0, H, num, P, Tx, time_step, Cv, n_terms):
    nodes = num + 1
    p_data, Z, T  = terzaghi(u0, H, Tx, time_step, nodes, Cv,n_terms)

    return p_data , Z, T/(60*60*24), 
