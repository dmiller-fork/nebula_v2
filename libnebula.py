import string
from collections import defaultdict
import heapq
import math
import functools

# this file has six classes: 

## InvertedIndex
## PartitionedInvertedIndex
## SearchResults
## TFIDFcalc
## KRankHeap
## RankedResults
## TrieNode
## Trie

# GLOBALS
PUNCTUATION = string.punctuation + "“”‘’"

# Alternate Constructor decorators from section 8.16 in Python Cookbook 2013-Beazley
class InvertedIndex:
	# Primary Constructor
	def __init__(self):
		self.index = defaultdict(lambda: defaultdict(int))
		self.indexed = defaultdict()

	# Alternate Constructor/Loader
	@classmethod
	def from_docs(cls, docs, dataset):
		index = cls()
	
		for doc, text in docs.items():
			lines = text.splitlines()
			index.indexed[doc] = dataset
			for line_number, line in enumerate(lines, start=1):
				words = line.split()

				for word in words:
					word = word.strip(PUNCTUATION).lower()
					index.index[word][(doc, line_number)] += 1
		return index
	# Alternate Constructor/Loader
	@classmethod
	def from_save(cls, savefile, manifestfile):
		index = cls()

		with open(savefile, "r") as f:
			for line in f:
				word, doc, line_number, count = line.rstrip("\n").split("\t")
				index.index[word][(doc, int(line_number))] = int(count)

		with open(manifestfile, "r") as f:
			for line in f:
				doc, dataset = line.rstrip("\n").split("\t")
				index.indexed[doc] = dataset

		return index

	# Create Save File
	def save(self, savefile, manifestfile):
		with open(savefile, "w") as f:
			for word, locations in self.index.items():
				for (doc, line_number), count in locations.items():
					f.write(f"{word}\t{doc}\t{line_number}\t{count}\n")
		with open(manifestfile, "w") as f:
			for doc, dataset in self.indexed.items():
				f.write(f"{doc}\t{dataset}\n")

	def __str__(self):
		output = ""

		for word, occurrences in list(self.index.items())[:3]:
			output += f"{word}: {occurrences}\n"
		datasets = set()
		for dataset in self.indexed.values():
			datasets.add(dataset)
		output += f"Indexed documents: {len(self.indexed)} from {len(datasets)} dataset(s)\n"
		return output

class PartitionedInvertedIndex:
	def __init__(self, num_partitions):
		self.partitions = [
			InvertedIndex()
			for _ in range(num_partitions)
		]
		self.num_partitions = num_partitions
		self.manifest = defaultdict(set)

	@staticmethod
	def hash_string(s, modulus):
		mult = 997
		return functools.reduce(lambda v, c: (v*mult+ord(c))%modulus, s, 0)
	
	def add_wave(self, docs, dataset):
		for doc, text in docs.items():
			if doc in self.manifest[dataset]:
				print(f"doc {doc} already indexed")
				continue
			lines = text.splitlines()
			for line_number, line in enumerate(lines, start=1):
				words = line.split()

				for word in words:
					word = word.strip(PUNCTUATION).lower()
					hash_id = self.hash_string(word, self.num_partitions)
					self.partitions[hash_id].index[word][(doc, line_number)] += 1
			self.manifest[dataset].add(doc)
		return self.partitions

	# Create Save File
	def save(self, directory):
		for i, partition in enumerate(self.partitions):
			filename = directory / f"{i+1}of{self.num_partitions}.tsv"
			with open(filename, "a") as f:
				for word, locations in partition.index.items():
					for (doc, line_number), count in locations.items():
						f.write(f"{word}\t{doc}\t{line_number}\t{count}\n")
		with open(directory / "manifest.tsv", "a") as f:
			for dataset, docs in self.manifest.items():
				for doc in docs:
					f.write(f"{dataset}\t{doc}\n")

	## load manifest before adding waves to ensure same doc is not indexed twice
	def load_manifest(self, manifest_file):
		try:
			with open(manifest_file, "r") as f:
				for line in f:
					dataset, doc = line.rstrip("\n").split("\t")
					self.manifest[dataset].add(doc)
				print("manifest loaded...")
		except FileNotFoundError:
			print("no manifest to load...")

class SearchResults:
	"""
	SearchResults is a projection of the inverted index
	that only includes the query terms.

	The tuple key is unpacked a three level dictionary:
	search_results.resultsterm][bookid][line] = count

	Note. This is a reference copy, so READ ONLY
	Do Not Modify search results or you will modify inverted index
	"""
	# Primary Constructor
	def __init__(self):
		self.results = defaultdict(
			lambda: defaultdict(
				lambda: defaultdict(int)
			)
		)

	# Alternate Constructor/Loader
	@classmethod
	def query_index(cls, index, query):
		results = cls()
		query_words = query.split()
		for word in query_words:
			word = word.strip(PUNCTUATION).lower()
			if word in index.index:
				for (bookid, line_number), count in index.index[word].items():
					results.results[word][bookid][line_number] = count
		return results

class TFIDFcalc:
	""" this class is necessary because
		there are many definitions of term frequency tf
		and inverse document frequency idf.
		in the def below tf is normalized by doc_length
		and idf is a log calculation log(N/n),
		where N is total number of docs, and
		n is number of docs in which query term t_k occurs,
		where k is an iterator for each query term.
	"""
	def __init__(self, books):
		self.book_lengths = {
			bookid: len(text.split())
			for bookid, text in books.items()
		}
		self.total_number_of_docs = len(books)

	@staticmethod
	def calc_tf(freq_of_term, doc_length):
		return freq_of_term / doc_length 

	@staticmethod
	def calc_idf(number_of_docs_w_term, total_number_of_docs):
		return math.log(total_number_of_docs / number_of_docs_w_term)

class KRankHeap:
	def __init__(self, k):
		self.k = k
		self.heap = []

	def add_result(self, item, rank):
		entry = (rank, item)

		if len(self.heap) < self.k:
			heapq.heappush(self.heap, entry)
		elif rank > self.heap[0][0]:
			heapq.heapreplace(self.heap, entry)

	def list_results(self):
		return sorted(self.heap, reverse=True)

class RankedResults:
	""" This class compiles search results and rank_scores into 
	score_list->books_dict->list of tuples (term, line, count)
	
	Note. This is a reference copy, so READ ONLY
	Do Not Modify Ranked results or you will modify inverted index
	"""
	def __init__(self, search_results, rank_scores):
		self.ranked_results = []
		self.snippets = []
		for score, book in rank_scores:
			results = []

			for term in search_results:
				if book in search_results[term]:
					for line, count in search_results[term][book].items():
						results.append((term, line, count))
			results.sort(key=lambda x: x[1]) #sorts tuples by line number
			self.ranked_results.append({book: results})

	def getSnippetStarts(self, window_size, terms):
		for book_dict in self.ranked_results:
			for book, results in book_dict.items():

				highest_count = 0
				highest_starting_line_tuple = (0, 0, 0)

				for i, (term, line, count) in enumerate(results):
					if term in terms:
						start_tuple = (term, line, count)
						start_line = line
						window_count = 0

						for term, line, count in results[i:]:
							if line > start_line + window_size:
								break

							if term in terms:
								window_count += count

						if window_count > highest_count:
							highest_count = window_count
							highest_starting_line_tuple = start_tuple
			book_dict[book] = highest_starting_line_tuple
			book = highest_starting_line_tuple
		
	def generateSnippets(self, books, window_size):

		for book_dict in self.ranked_results:
			for book, start_tuple in book_dict.items():

				if start_tuple == (0, 0, 0):
					self.snippets.append({
						book: "no snippets found"
					})
					continue

				start_line = start_tuple[1]
				lines = books[book].splitlines()
				snippet = lines[start_line - 1:start_line - 1 + window_size]

				self.snippets.append({
					book: "\n".join(snippet)
				})
	@staticmethod
	def get_title(book_text):
		lines = book_text.splitlines()
		for line in lines:
			if line.startswith("Title:"):
				return line.removeprefix("Title:").strip()

class TrieNode:
	def __init__(self):
		self.children = {}
		self.is_word = False


class Trie:
	def __init__(self):
		self.trie = TrieNode()
	
	# Alternate Constructor/Loader
	@classmethod
	def from_docs(cls, docs):
		trie = cls()

		for doc, text in docs.items():
			lines = text.splitlines()

			for line_number, line in enumerate(lines, start=1):
				words = line.split()

				for word in words:
					word = word.strip(PUNCTUATION).lower()
					trie.insert(word)
		return trie

	def insert(self, word):
		node = self.trie

		for char in word:
			if char not in node.children:
				node.children[char] = TrieNode()
			node = node.children[char]

		node.is_word = True

	def contains(self, word):
		node = self.trie

		for char in word:
			if char not in node.children:
				return False
			node = node.children[char]

		return node.is_word
	def words_with_stem(self, stem):
		node = self.trie

		# Find the node corresponding to the stem
		for char in stem:
			if char not in node.children:
				return []
			node = node.children[char]

		# Collect words below that node
		words = []

		def collect(node, prefix):
			if node.is_word:
				words.append(prefix)

			for char, child in node.children.items():
				collect(child, prefix + char)

		collect(node, stem)

		return words
