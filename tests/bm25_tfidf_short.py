import sys
from pathlib import Path
from collections import defaultdict
sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import PartitionedInvertedIndex
from libnebula import SearchResults
from libnebula import TFIDFcalc

dataset = "test_dataset"
books = {
	"book1": "the the the\nfoo the\nbar",
	"book2": "the boo is a foo\n baz",
	"book3": "treasure is here\n treasure"
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
	# print(search_results)

	# tfidf object creates doc_lengths and total_number_of_docs
	tfidf = TFIDFcalc(pindex.book_lengths) # this gives setup for doc_word_count

	# now run triple for loop 
	book_scores = defaultdict(float)
	for term, books in search_results.results.items():
		df = len(books)
		idf = tfidf.calc_bm25idf(df, tfidf.total_number_of_docs)
		## small optimization
		if idf == 0:
			continue
		for bookid, lines in books.items():
			term_count = sum(lines.values())
			tf = tfidf.calc_bm25tf(
				term_count, 
				tfidf.book_lengths[bookid], 
				tfidf.avg_doc_length
			)
			book_scores[bookid] += tf * idf
	for bookid, score in book_scores.items():
		print(bookid, score)
