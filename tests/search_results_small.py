import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import PartitionedInvertedIndex
from libnebula import SearchResults

dataset = "test_dataset"
books = {
    "test": "the the the\nfoo the\nbar"
}

# books = {}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "gutenberg"
MANIFEST_FILE = PROJECT_ROOT / "data"/ "saves"/ "manifest.tsv"
SAVE_DIR = PROJECT_ROOT / "data"/ "saves"
#for file in DATA_DIR.glob("*.txt"):
	#books[file.stem] = file.read_text()

if __name__ == "__main__":
	num_partitions = 5
	pindex = PartitionedInvertedIndex(num_partitions)
	pindex.load_manifest(MANIFEST_FILE)
	pindex.add_wave(books, dataset)
	filenames = pindex.save(SAVE_DIR)
	query = "foo bar"
	search_results = SearchResults.query_partitions(filenames, MANIFEST_FILE, query)
	print(search_results)
	
