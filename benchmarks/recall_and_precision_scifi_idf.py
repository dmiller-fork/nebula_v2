import csv
import sys
from pathlib import Path
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import SearchResults
from libnebula import TFIDFcalc
from libnebula import KRankHeap
from libnebula import RankedResults
from libnebula import PartitionedInvertedIndex

dataset = "gutenberg"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_FILE = PROJECT_ROOT / "data"/ "saves"/ "manifest.tsv"
SAVE_DIR = PROJECT_ROOT / "data"/ "saves"

DATA_DIR = Path("/Volumes/home/repos/nebula/data/gutenberg")
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"
metadata = {}

with open(METADATA_DIR / "bookshelves.csv", newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        metadata[row["book_id"]] = row["bookshelves"]

adventure = {
    book_id
    for book_id, bookshelves in metadata.items()
    if "Adventure" in bookshelves
}

science_fiction = {
    book_id
    for book_id, bookshelves in metadata.items()
    if "Science Fiction" in bookshelves
}
print("starting test...")
print(len(adventure))
print(len(science_fiction))

"""
books = {}
DATA_DIR = PROJECT_ROOT / "data" / "gutenberg"

for file in DATA_DIR.glob("*.txt"):
	books[file.stem] = file.read_text()

if __name__ == "__main__":
	index = InvertedIndex.from_docs(books)
	query = "treasure voyage adventure pirates swords"

"""

if __name__ == "__main__":
	num_partitions = 500
	pindex = PartitionedInvertedIndex(num_partitions)
	pindex.load_manifest(MANIFEST_FILE)
	filenames = pindex.save(SAVE_DIR)

	query = "spaceship future technology alien planet"
	print("query is 5 terms:", query)
	search_results = SearchResults.query_partitions(filenames, query)
	tfidf = TFIDFcalc(pindex.book_lengths)

	# now run for loops
	book_scores = defaultdict(float)
	for term, book_postings in search_results.results.items():
		df = len(book_postings)
		idf = tfidf.calc_idf(df, tfidf.total_number_of_docs)
		## small optimization
		if idf == 0:
			continue
		for bookid, lines in book_postings.items():
			term_count = sum(lines.values())
			tf = tfidf.calc_tf(
						term_count,
						tfidf.book_lengths[bookid]
					)
			book_scores[bookid] += idf
	# scoring/heap logic
	k = 20 
	rank_heap = KRankHeap(k)

	for bookid, score in book_scores.items():
		rank_heap.add_result(bookid, score)
	
	#Ranked Results logic
	ranked_results = RankedResults(search_results.results, rank_heap.heap)
	results = [next(iter(item)) for item in ranked_results.ranked_results]

	relevant = len(set(results) & science_fiction)

	precision = relevant / len(results)
	recall = relevant / len(science_fiction)
	print(f"number of docs in dataset: {len(pindex.book_lengths)}")
	print(f"number of relevant docs in dataset: {len(science_fiction)}")
	print(f"number of docs returned: {k}")
	print(f"number of relevant docs in results: {relevant}")
	print(f"Precision@{k}: {precision:.2%}")
	print(f"Recall@{k}:    {recall:.2%}")
	print(f"Max possible recall given docs returned: {k/len(science_fiction):.2%}")
