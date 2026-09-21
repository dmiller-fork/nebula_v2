.PHONY: run_all test data clean

run_all:
	@for file in tests/*.py; do \
		echo "Running $$file"; \
		python3 "$$file"; \
	done

test:
	./scripts/download_gutenberg_test.sh

data:
	./scripts/download_gutenberg_data.sh

large:
	./scripts/download_gutenberg_large.sh

clean:
	rm -f data/gutenberg/*.txt
