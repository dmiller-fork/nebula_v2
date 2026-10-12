
import matplotlib.pyplot as plt

# Replace these example placeholders with your measurements
docs = [30, 1000, 2000, 10000]
index_size_mb = [48, 1200, 2200, 10000]

plt.scatter(docs, index_size_mb)

plt.xlabel("Number of Documents")
plt.ylabel("Inverted Index Size (MB)")
plt.title("Inverted Index Size vs. Number of Documents")

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

