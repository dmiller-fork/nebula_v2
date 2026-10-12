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
