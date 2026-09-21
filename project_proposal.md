# project structure
	- just seven classes
```
class InvertedIndex:
class PartitionedInvertedIndex:
class SearchResults:
class TFIDFcalc:
class KRankHeap:
class RankedResults:
class TrieNode:
class Trie:
```
# project goals
	- break up the data structures so they can be performed in waves or in parallel

# major tasks
	- create_inverted_index -> save -> load -> add_wave -> print_size
	- benchmark searchresults (show overhead of defaultdict)
	- BM25
	- toolchain for processing PDFs
	- process literature review as a dag and store
	- create trie -> store idf scores of each word in trie
	- benchmarks

## first major benchmark
	- I tried scaling to 10k docs, and had to scale up hardware and change the infra
	- for hardware, the gutenberg books are mounted on NAS, this frees up some hard drive for making the inverted index as big as necessary.
	- for infra, I am splitting the inverted index into partitions and persisting them.
	- for each batch (~1k to ~2k docs) a temp index for each partition gets created
	- after temp creation, those temp partitions can be added to their corresponding persisted partitions
	- at query time, partitions will likely get read into memory one at a time to generate search results
	- search results are the portions of the inverted index relevant to query, so the search result dictionary can be fully in memory
	- from their infrastructure should be same, and I can update TF-IDF to BM25
	- might have to do benchmark study on number of partitions versus query time
