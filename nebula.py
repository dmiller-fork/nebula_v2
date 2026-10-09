import sys
from pathlib import Path
from collections import defaultdict
sys.path.append(str(Path(__file__).parent.parent))
import time

from libnebula import InvertedIndex
from libnebula import PartitionedInvertedIndex
from libnebula import SearchResults
from libnebula import TFIDFcalc
from libnebula import KRankHeap
from libnebula import RankedResults
from libnebula import Trie

dataset = "gutenberg"

PROJECT_ROOT = Path(__file__).resolve().parent
MANIFEST_FILE = PROJECT_ROOT / "data"/ "saves"/ "manifest.tsv"
SAVE_DIR = PROJECT_ROOT / "data"/ "saves"
DATA_DIR = Path("/Volumes/home/repos/nebula/data/gutenberg")
TRIE_FILE = PROJECT_ROOT / "data"/ "saves"/ "trie.bin"

def main():
	flag = True
	if Path(MANIFEST_FILE).exists():
		print("index already exists, loading index and trie, takes a 2 min")
		start = time.perf_counter()
		num_partitions = 500
		pindex = PartitionedInvertedIndex(num_partitions)
		pindex.load_manifest(MANIFEST_FILE)
		filenames = pindex.save(SAVE_DIR)
		trie = Trie.from_save(TRIE_FILE)
		print(f"Load time: {time.perf_counter() - start:.2f}s")
	else:
		req = input("no index loaded. Type '/build' to build index or /quit to quit\n")
		if req == "/build":
			trie = Trie()
			files = list(DATA_DIR.glob("*.txt"))
			if not files: raise FileNotFoundError(f"Could not load files; is drive mounted? ")
			book_lengths = {}
			for start in range(0, len(files), 1000):
				batch = files[start:start + 1000]

				books = {}
				for file in batch:
					text = file.read_text()
					bookname = file.stem
					books[bookname] = text
					book_lengths[bookname] = len(text.split())
				trie.add_docs(books)
				# process books here
				num_partitions = 500
				pindex = PartitionedInvertedIndex(num_partitions)
				pindex.load_manifest(MANIFEST_FILE)
				pindex.add_wave(books, dataset)
				filenames = pindex.save(SAVE_DIR)
			trie.save(TRIE_FILE)		
		else:
			flag = False	
		
	while flag:
		try:
	
			print("search with wildcard character '$' or filter character '!' at end of terms")
			print()
			query = input("nebula> ").strip()
		except EOFError:
			print()
			break

		if query in ("/quit", "/exit"):
			break
		if query == "/dump":
			confirm = input("Delete all saved search data? [y/N]: ")

			if confirm.lower() == "y":
				for filename in SAVE_DIR.iterdir():
					if filename.is_file():
						filename.unlink()
				continue
		if query == "/build":
			break
	
		if query.startswith("/trie "):
			terms = query.removeprefix("/trie ").strip()
			print("get list for stem: 'trea'")
			for term in terms.split():
				words = trie.words_with_stem(term)
				for word in words:
					print(word, trie.get_df(word))		
			continue
		if not query: #check for empty input 
			continue

		# Parse Query looking for special terms "!" and "$" at the end of words
		full_query = ""
		snippet_terms = []
		query_words = query.split()
		for word in query_words:
			if word[-1] == '$':
				terms = trie.words_with_stem(word[0:-1])
				if len(terms) > 20:
					print(f"Expands to {len(terms)} terms.")
					confirm = input("Continue? (y/n): ").lower()
					if confirm != "y":
						continue
				snippet_terms.extend(terms)
				expand_terms = " ".join(terms)
				full_query += " " + expand_terms
			if word[-1] == '!':
				full_query += " " + word[0:-1]
			else:
				full_query += " " + word
				snippet_terms.append(word)
		print("full query: ", full_query)
		print("snippet_terms: ", snippet_terms)
			
		## Generate Search Results
		search_results = SearchResults.query_partitions(filenames, full_query)
		
		## Generate Scores for each book
		tfidf = TFIDFcalc(pindex.book_lengths)
		book_scores = defaultdict(float)
		for term, book_postings in search_results.results.items():
			df = len(book_postings)
			idf = tfidf.calc_bm25idf(df, tfidf.total_number_of_docs)
			## small optimization
			if idf == 0:
				continue
			for bookid, lines in book_postings.items():
				term_count = sum(lines.values())
				tf = tfidf.calc_bm25tf(
					term_count,
					tfidf.book_lengths[bookid],
					tfidf.avg_doc_length
				)
				book_scores[bookid] += tf * idf
		
		## Push the top scores onto the Heap
		k = 5 
		rank_heap = KRankHeap(k)

		for bookid, score in book_scores.items():
			rank_heap.add_result(bookid, score)

		## Generate Snippets
		ranked_results = RankedResults(search_results.results, rank_heap.heap)
		window_size = 5
		ranked_results.getSnippetStarts(window_size, snippet_terms)
		books = {}
		"""
		LOAD BOOKS HERE (see snippets loaded in test)
		"""
		if(books):
			ranked_results.generateSnippets(books, window_size);

			## Print Results
			for i, snippet_dict in enumerate(ranked_results.snippets):
				for book_name, snippet in snippet_dict.items():
					print(" ")
					title = ranked_results.get_title(books[book_name])
					print(f"{i+1}. [{book_name}:{ranked_results.ranked_results[i][book_name][1]}] {title}")
					print("----------------------------------------------------------------------")
					lines = snippet.split("\n")
					for line in lines:
						print(line)
				print(" ")
				print(" ")
		else:
			for book_dict in ranked_results.ranked_results:
				print(book_dict)		
if __name__ == "__main__":
	main()
