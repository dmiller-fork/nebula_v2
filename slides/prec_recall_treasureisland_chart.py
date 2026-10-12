
import matplotlib.pyplot as plt
import numpy as np

methods = ["BM25", "TF-IDF", "TF only", "IDF only"]

precision = [5.00, 0.00, 0.00, 5.00]
recall = [100.00, 0.00, 0.00, 100.00]

x = np.arange(2)
width = 0.2
offsets = np.arange(4) * width - 1.5 * width

fig, ax = plt.subplots()

for i, method in enumerate(methods):
    ax.bar(x + offsets[i],
           [precision[i], recall[i]],
           width, label=method)

ax.set_ylabel("Percentage (%)")
ax.set_title("Treasure Island Query: Precision and Recall")
ax.set_xticks(x)
ax.set_xticklabels(["Precision@20", "Recall@20"])
ax.set_ylim(0, 100)
ax.legend()

plt.tight_layout()
plt.show()

