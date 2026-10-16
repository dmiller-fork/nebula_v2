# Getting started
    - clone the repo
    - download the first 10k docs of the gutenberg dataset (using script in scripts folder). Should be about 10GB.
    - update the path variable DATA_DIR in nebula.py to point to the dataset
    - then run the program: `python3 nebula.py`.
	- the first command should be `/build` to build the inverted index. Should be about 10GB.
	- after that search using the '$' query expander at the end of terms or the '!' filter remove search terms from snippets.
	- one last feature is the /trie command which lets you explore document frequency of stems

### Environment Setup

Nebula uses two environments:

- **Development machine:** Contains the Nebula source code, Python environment, and indexing and retrieval tools.
- **Synology NAS:** Stores the document corpus and runs the corpus acquisition scripts.

#### Corpus Acquisition

1. Copy the `scripts/` directory to the Synology NAS.
2. Run the corpus acquisition script on the NAS to download the documents directly to NAS storage.
3. Configure Nebula on the development machine to access the corpus at its mounted NAS path.
4. Run indexing and retrieval operations from the development machine.

The `scripts/` directory is deployed to the NAS for corpus acquisition; the rest of the repository remains on the development machine.
