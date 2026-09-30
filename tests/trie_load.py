import sys
from pathlib import Path
from collections import defaultdict

sys.path.append(str(Path(__file__).parent.parent))

from libnebula import Trie

books = {
	"book1": "the the the\nfoo the\nbar",
	"book2": "the boo is a foo\nbar",
	"book3": "treasure is here\n treasure"
}

# books = {}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "gutenberg"
TRIE_FILE = PROJECT_ROOT / "data"/ "saves"/ "trie.bin"

# for file in DATA_DIR.glob("*.txt"):
#	books[file.stem] = file.read_text()

if __name__ == "__main__":
	#index = InvertedIndex.from_docs(books)
	trie = Trie.from_save(TRIE_FILE)

	print("get list for stem: 'trea'")
	words = trie.words_with_stem("trea")
	for word in words:
		print(word, trie.get_df(word))

