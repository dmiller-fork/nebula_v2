import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import PartitionedInvertedIndex
from libnebula import SearchResults

dataset = "gutenberg"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = PROJECT_ROOT / "data"/ "saves"/ "manifest.tsv"
SAVE_DIR = PROJECT_ROOT / "data"/ "saves"

DATA_DIR = Path("/Volumes/home/repos/nebula/data/gutenberg")


files = list(DATA_DIR.glob("*.txt"))
book_lengths = {}
for start in range(0, len(files), 1000):
	batch = files[start:start + 1000]

	books = {}
	for file in batch:
		text = file.read_text()
		bookname = file.stem
		books[bookname] = text
		book_lengths[bookname] = len(text.split())
	# process books here
	num_partitions = 5
	pindex = PartitionedInvertedIndex(num_partitions)
	pindex.load_manifest(MANIFEST_FILE)
	pindex.add_wave(books, dataset)
	filenames = pindex.save(SAVE_DIR)

query = "treasure jim"
search_results = SearchResults.query_partitions(filenames, MANIFEST_FILE, query)
print(search_results)
