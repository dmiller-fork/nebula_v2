# general concepts
	- so partitions are single inverted indexes
	- the entire inverted index is never entirely in memory
	- the manifest is stored as lines (dataset, book, length)
	- the manifest is entirely in memory as two data structures:
		- manifest is dataset[book]
		- book_lenghts is book_lengths[book]
	- purpose of manifest to not re-save books already in inverted index again
	- purpose of book_lengths is for the TF_IDF calculations
	- separate purposes for in memory, but convenvient to persist together 
