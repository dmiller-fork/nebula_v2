import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex

dataset = "gutenberg30"

books = {}

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = Path("/Volumes/home/repos/nebula/data/gutenberg")

SAVE_FILE = PROJECT_ROOT / "data" / "saves" / "index.txt"
MANIFEST_FILE = PROJECT_ROOT / "data" / "saves" / "indexed.txt"

for file in DATA_DIR.glob("*.txt"):
	books[file.stem] = file.read_text()

if __name__ == "__main__":
	index = InvertedIndex.from_docs(books, dataset)
	print("index size:", len(index.index))
	print(index)
	index.save(SAVE_FILE, MANIFEST_FILE)
