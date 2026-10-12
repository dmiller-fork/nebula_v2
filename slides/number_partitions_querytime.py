
import matplotlib.pyplot as plt

# Replace with your measured values
partitions = [5, 10, 20, 50, 100, 200, 500]
runtime_seconds = [141.34, 60.20, 30.30, 13.39, 5.25, 2.90, 1.61]

plt.scatter(partitions, runtime_seconds)

plt.xlabel("Number of Partitions")
plt.ylabel("Query Runtime (seconds)")
plt.title("Query Runtime vs. Number of Partitions")

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

