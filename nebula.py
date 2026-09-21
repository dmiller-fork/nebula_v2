import sys
from pathlib import Path
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import InvertedIndex
from libnebula import Trie
from libnebula import SearchResults
from libnebula import TFIDFcalc
from libnebula import KRankHeap
from libnebula import RankedResults

def main():
	print("Building inverted index and trie...")
	
	books = {}
	PROJECT_ROOT = Path(__file__).resolve().parent
	DATA_DIR = PROJECT_ROOT / "data" / "gutenberg"

	for file in DATA_DIR.glob("*.txt"):
		books[file.stem] = file.read_text()
	index = InvertedIndex.from_docs(books)
	trie = Trie.from_docs(books)

	print("built index of:", books.keys())
	print("search with wildcard character '$' or filter character '!' at end of terms")
	print()

	while True:
		try:
			query = input("nebula> ")
		except EOFError:
			print()
			break

		if query in ("quit", "exit"):
			break

		if not query: #check for empty input 
			continue

		# Parse Query looking for special terms "!" and "$" at the end of words
		full_query = ""
		snippet_terms = []
		query_words = query.split()
		for word in query_words:
			if word[-1] == '$':
				terms = trie.words_with_stem(word[0:-1])
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
		search_results = SearchResults.query_index(index, full_query);
		
		## Generate Scores for each book
		tfidf = TFIDFcalc(books) # this gives setup for doc_word_count
		book_scores = defaultdict(float)
		for term, book_postings in search_results.results.items():
			df = len(book_postings)
			idf = tfidf.calc_idf(df, tfidf.total_number_of_docs)
			## small optimization
			if idf == 0:
				continue
			for bookid, lines in book_postings.items():
				term_count = sum(lines.values())
				tf = tfidf.calc_tf(term_count, tfidf.book_lengths[bookid])
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

if __name__ == "__main__":
	main()
