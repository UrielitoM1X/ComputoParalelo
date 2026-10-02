import glob
import pandas as pd
import matplotlib.pyplot as plt

archivos = [f for f in glob.glob("results/*.csv") if "resumen" not in f]
df = pd.concat([pd.read_csv(f) for f in archivos], ignore_index=True)

g = (df.groupby(["variant", "n"])
     .agg(t_mean=("seconds", "mean"), t_std=("seconds", "std"), gflops=("gflops", "mean"))
     .reset_index())

g.to_csv("results/resumen.csv", index=False)
print(g.to_string(index=False))

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for v, s in g.groupby("variant"):
    ax[0].errorbar(s.n, s.t_mean, yerr=s.t_std, marker="o", capsize=3, label=v)
    ax[1].plot(s.n, s.gflops, marker="o", label=v)

ax[0].set(xscale="log", yscale="log", xlabel="n", ylabel="tiempo de pared [s]", title="Tiempo (promedio +- desv. est.)")
ax[1].set(xscale="log", yscale="log", xlabel="n", ylabel="GFLOPS", title="Rendimiento")
ax[0].legend()
ax[1].legend()
fig.tight_layout()
fig.savefig("results/practica1.png", dpi=150)