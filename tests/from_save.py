import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex

dataset = "test_dataset"
books = {
    "test": "the the the\nfoo the\nbar"
}

# books = {}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "gutenberg"
SAVE_FILE = PROJECT_ROOT/ "data" / "saves"/ "index.txt"
MANIFEST_FILE = PROJECT_ROOT / "data"/ "saves"/ "indexed.txt"

#for file in DATA_DIR.glob("*.txt"):
	#books[file.stem] = file.read_text()

if __name__ == "__main__":
	index = InvertedIndex.from_docs(books, dataset)
	index.save(SAVE_FILE, MANIFEST_FILE)
	del index
	index2 = InvertedIndex.from_save(SAVE_FILE, MANIFEST_FILE)
	print("index size:", len(index2.index))
	print(index2)
