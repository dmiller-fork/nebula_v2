import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import PartitionedInvertedIndex

dataset = "gutenberg"

books = {}
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = Path("/Volumes/home/repos/nebula/data/gutenberg")

SAVE_FILE = PROJECT_ROOT / "data" / "saves" / "index.txt"
MANIFEST_FILE = PROJECT_ROOT / "data" / "saves" / "manifest.txt"


for file in enumerate(DATA_DIR.glob("*.txt")):
	if i >= 100:
		break
	for attempt in range(5):
		try:
			books[file.stem] = file.read_text()
			break
		except FileNotFoundError:
			print(f"{file} unavailable, retrying...")
			time.sleep(1)
	else:
		print(f"Could not read {file}")
if __name__ == "__main__":
	num_partitions = 5
	pindex = PartitionedInvertedIndex(num_partitions)
	print(pindex.partitions)
	word = "word"
	hash_id = pindex.hash_string(word, pindex.num_partitions)
	pindex.add_wave(books, dataset)
