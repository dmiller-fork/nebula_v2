import sys
from pathlib import Path
from collections import defaultdict
sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import PartitionedInvertedIndex
from libnebula import SearchResults
from libnebula import TFIDFcalc
from libnebula import KRankHeap
from libnebula import RankedResults

dataset = "gutenberg"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = PROJECT_ROOT / "data"/ "saves"/ "manifest.tsv"
TRIE_FILE = PROJECT_ROOT / "data"/ "saves"/ "trie.bin"
SAVE_DIR = PROJECT_ROOT / "data"/ "saves"

DATA_DIR = Path("/Volumes/home/repos/nebula/data/gutenberg")

files = list(DATA_DIR.glob("*.txt"))
for start in range(0, len(files), 1000):
	batch = files[start:start + 1000]

	books = {}
	for file in batch:
		text = file.read_text()
		bookname = file.stem
		books[bookname] = text
	# process books here
    trie = Trie.from_docs(books)

trie.save(TRIE_FILE)

if __name__ == "__main__":
    print("get list for stem: 'trea'")
    words = trie.words_with_stem("trea")
    for word in words:
        print(word, trie.get_df(word))
