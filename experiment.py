import numpy as np
import matplotlib.pyplot as plt
from blockcode import Block_code
from adjustText import adjust_text
from scipy import stats

def make_chart(xs, ys, labels, xlabel, title, filename, integer_xticks=False):
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.scatter(xs, ys, zorder=3, s=65, color='steelblue')
    slope, intercept, r_val, _, _ = stats.linregress(xs, ys)
    x_line = np.linspace(min(xs) - 0.05*(max(xs)-min(xs)),
                         max(xs) + 0.05*(max(xs)-min(xs)), 200)
    ax.plot(x_line, slope*x_line + intercept, color='tomato', linewidth=1.5,
            linestyle='--',  zorder=2)
    ax.legend(fontsize=10)
    texts = [ax.text(x, y, lbl, fontsize=7.5, color='#333')
             for x, y, lbl in zip(xs, ys, labels)]
    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle='-', color='#bbb', lw=0.7),
                expand=(1.5, 1.8), force_text=(0.5, 0.8))
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("$d_{\\min}$", fontsize=12)
    ax.set_title(title, fontsize=13)
    if integer_xticks:
        ax.set_xticks(sorted(set(int(x) for x in xs)))
    ax.set_yticks(sorted(set(ys)))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_ylim(0, max(ys) + 2)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"Saved {filename}")

# ── Charts 1 & 2: varied n and k ────────────────────────────────────────────
configs = [
    (5,  2, [[1,0,1,1,0],[0,1,1,0,1]]),
    (5,  3, [[1,0,0,1,1],[0,1,0,1,0],[0,0,1,0,1]]),
    (6,  2, [[1,0,1,1,0,1],[0,1,1,0,1,1]]),
    (6,  3, [[1,0,0,1,1,0],[0,1,0,1,0,1],[0,0,1,0,1,1]]),
    (6,  4, [[1,0,0,0,1,1],[0,1,0,0,1,0],[0,0,1,0,0,1],[0,0,0,1,1,1]]),
    (7,  2, [[1,0,1,1,1,0,1],[0,1,1,0,1,1,0]]),
    (7,  4, [[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]]),
    (7,  5, [[1,0,0,0,0,1,1],[0,1,0,0,0,1,0],[0,0,1,0,0,0,1],[0,0,0,1,0,1,1],[0,0,0,0,1,1,0]]),
    (8,  2, [[1,0,1,1,1,0,1,0],[0,1,1,1,0,1,0,1]]),
    (8,  4, [[1,0,0,0,1,1,1,0],[0,1,0,0,1,1,0,1],[0,0,1,0,1,0,1,1],[0,0,0,1,0,1,1,1]]),
    (8,  5, [[1,0,0,0,0,1,1,0],[0,1,0,0,0,1,0,1],[0,0,1,0,0,0,1,1],[0,0,0,1,0,1,1,0],[0,0,0,0,1,0,1,1]]),
    (8,  6, [[1,0,0,0,0,0,1,1],[0,1,0,0,0,0,1,0],[0,0,1,0,0,0,0,1],[0,0,0,1,0,0,1,1],[0,0,0,0,1,0,1,0],[0,0,0,0,0,1,0,1]]),
    (9,  2, [[1,0,1,1,1,0,1,0,1],[0,1,1,0,1,1,0,1,1]]),
    (9,  4, [[1,0,0,0,1,1,1,0,0],[0,1,0,0,1,1,0,1,0],[0,0,1,0,1,0,1,0,1],[0,0,0,1,0,1,1,0,1]]),
    (9,  5, [[1,0,0,0,0,1,1,0,1],[0,1,0,0,0,1,0,1,1],[0,0,1,0,0,0,1,1,1],[0,0,0,1,0,1,1,1,0],[0,0,0,0,1,1,0,1,0]]),
    (10, 2, [[1,0,1,1,1,0,1,0,1,1],[0,1,1,0,1,1,1,1,0,1]]),
    (10, 4, [[1,0,0,0,1,1,1,0,0,1],[0,1,0,0,1,1,0,1,0,1],[0,0,1,0,1,0,1,0,1,1],[0,0,0,1,0,1,1,0,1,1]]),
    (10, 6, [[1,0,0,0,0,0,1,1,0,1],[0,1,0,0,0,0,1,0,1,1],[0,0,1,0,0,0,0,1,1,1],[0,0,0,1,0,0,1,1,1,0],[0,0,0,0,1,0,1,0,1,1],[0,0,0,0,0,1,0,1,1,1]]),
    (10, 8, [[1,0,0,0,0,0,0,0,1,1],[0,1,0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0,0,1],[0,0,0,1,0,0,0,0,1,1],[0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,1,0,0,0,1],[0,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,0,1,0,1]]),
    (12, 4, [[1,0,0,0,1,1,0,1,1,0,1,0],[0,1,0,0,1,0,1,1,0,1,1,0],[0,0,1,0,0,1,1,1,0,0,1,1],[0,0,0,1,0,0,1,0,1,1,1,1]]),
    (12, 6, [[1,0,0,0,0,0,1,1,0,1,0,1],[0,1,0,0,0,0,1,0,1,0,1,1],[0,0,1,0,0,0,0,1,1,1,0,1],[0,0,0,1,0,0,1,1,1,0,1,0],[0,0,0,0,1,0,1,0,0,1,1,1],[0,0,0,0,0,1,0,1,0,1,1,1]]),
    (12, 9, [[1,0,0,0,0,0,0,0,0,1,1,0],[0,1,0,0,0,0,0,0,0,1,0,1],[0,0,1,0,0,0,0,0,0,0,1,1],[0,0,0,1,0,0,0,0,0,1,1,1],[0,0,0,0,1,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0,0,0,1,0],[0,0,0,0,0,0,1,0,0,0,0,1],[0,0,0,0,0,0,0,1,0,1,0,1],[0,0,0,0,0,0,0,0,1,0,1,1]]),
    (15,11, [[1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],[0,1,0,0,0,0,0,0,0,0,0,1,1,0,0],[0,0,1,0,0,0,0,0,0,0,0,0,1,1,0],[0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],[0,0,0,0,1,0,0,0,0,0,0,1,1,0,1],[0,0,0,0,0,1,0,0,0,0,0,1,0,1,0],[0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],[0,0,0,0,0,0,0,1,0,0,0,1,1,1,0],[0,0,0,0,0,0,0,0,1,0,0,0,1,1,1],[0,0,0,0,0,0,0,0,0,1,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,1,1,0,1,1]]),
]

results = []
for n, k, G_rows in configs:
    b = Block_code([int("".join(map(str, bits)), 2) for bits in G_rows], n)
    d = b.d_min
    results.append((n, k, n-k, k/n, d))

labels12 = [f"({r[0]},{r[1]})" for r in results]

make_chart([r[2] for r in results], [r[4] for r in results], labels12,
           "Redundancy  r = n - k",
           "$d_{\\min}$ vs Redundancy: each point is an $(n,k)$ code",
           "latex/dmin_vs_redundancy.png", integer_xticks=True)

make_chart([r[3] for r in results], [r[4] for r in results], labels12,
           "Code rate  R = k/n",
           "$d_{\\min}$ vs Code Rate - each point is an $(n,k)$ code",
           "latex/dmin_vs_rate.png")

# ── Chart 3: fixed k=3, vary n (rate drops, r grows, d_min grows) ────────────
fixed_k_configs = [
    (4,  3, [[1,0,0,1],[0,1,0,1],[0,0,1,1]]),
    (5,  3, [[1,0,0,1,1],[0,1,0,1,0],[0,0,1,0,1]]),
    (6,  3, [[1,0,0,1,1,0],[0,1,0,1,0,1],[0,0,1,0,1,1]]),
    (7,  3, [[1,0,0,1,1,1,0],[0,1,0,1,1,0,1],[0,0,1,0,1,1,1]]),
    (8,  3, [[1,0,0,1,1,1,0,0],[0,1,0,1,0,1,1,0],[0,0,1,0,1,1,0,1]]),
    (9,  3, [[1,0,0,1,1,1,0,1,0],[0,1,0,1,0,1,1,0,1],[0,0,1,0,1,1,1,1,0]]),
    (10, 3, [[1,0,0,1,1,1,0,1,0,1],[0,1,0,1,0,1,1,0,1,1],[0,0,1,0,1,1,1,1,0,1]]),
    (11, 3, [[1,0,0,1,1,1,0,1,0,1,1],[0,1,0,1,0,1,1,0,1,1,0],[0,0,1,0,1,1,1,1,0,1,1]]),
    (12, 3, [[1,0,0,1,1,1,0,1,0,1,1,0],[0,1,0,1,0,1,1,0,1,1,0,1],[0,0,1,0,1,1,1,1,0,1,1,1]]),
    (13, 3, [[1,0,0,1,1,1,0,1,0,1,1,0,1],[0,1,0,1,0,1,1,0,1,1,0,1,1],[0,0,1,0,1,1,1,1,0,1,1,1,0]]),
    (14, 3, [[1,0,0,1,1,1,0,1,0,1,1,0,1,0],[0,1,0,1,0,1,1,0,1,1,0,1,0,1],[0,0,1,0,1,1,1,1,0,1,1,1,0,1]]),
    (15, 3, [[1,0,0,1,1,1,0,1,0,1,1,0,1,0,1],[0,1,0,1,0,1,1,0,1,1,0,1,0,1,1],[0,0,1,0,1,1,1,1,0,1,1,1,0,1,1]]),
]

fk_results = []
for n, k, G_rows in fixed_k_configs:
    b = Block_code([int("".join(map(str, bits)), 2) for bits in G_rows], n)
    d = b.d_min
    fk_results.append((n, k, n-k, k/n, d))

ns3    = [r[0] for r in fk_results]
dmins3 = [r[4] for r in fk_results]
rates3 = [r[3] for r in fk_results]
labels3 = [f"({r[0]},{r[1]})\nR={r[3]:.2f}" for r in fk_results]

fig, ax = plt.subplots(figsize=(13, 6))
ax.scatter(ns3, dmins3, zorder=3, s=65, color='steelblue')
ax.plot(ns3, dmins3, color='steelblue', linewidth=0.8, alpha=0.35, zorder=1)

slope, intercept, r_val, _, _ = stats.linregress(ns3, dmins3)
x_line = np.linspace(min(ns3)-0.3, max(ns3)+0.3, 200)

texts = [ax.text(n, d, lbl, fontsize=7, color='#333')
         for n, d, lbl in zip(ns3, dmins3, labels3)]
adjust_text(texts, ax=ax,
            arrowprops=dict(arrowstyle='-', color='#bbb', lw=0.7),
            expand=(1.5, 1.8), force_text=(0.5, 0.8))

ax.set_xlabel("Block length  n  (fixed k = 3)", fontsize=12)
ax.set_ylabel("$d_{\\min}$", fontsize=12)
ax.set_title("$d_{\\min}$ vs Block Length at Fixed $k=3$ - rate decreases as $n$ grows", fontsize=13)
ax.set_xticks(ns3)
ax.set_yticks(sorted(set(dmins3)))
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_ylim(0, max(dmins3) + 2)
plt.tight_layout()
plt.savefig("latex/dmin_vs_n_fixed_k.png", dpi=150)
print("Saved dmin_vs_n_fixed_k.png")
