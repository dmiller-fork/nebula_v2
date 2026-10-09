# partitining benchmarks
## setup
	- I've setup 5 tests to benchmark query time.
	- The corpus is 10k docs, which is a 10GB inverted index.
	- The inverted index will be created with 5, 10, 20, 50, and 100 partitions.
	- The test will use the following code:

```

query = "treasure voyage adventure pirates swords"
print("query is 5 terms:", query)

times = []

for _ in range(10):
	start = time.perf_counter()
	SearchResults.query_partitions(filenames, MANIFEST_FILE, query)
	times.append(time.perf_counter() - start)

print(f"mean:	{sum(times) / len(times):.6f}s")
print(f"min:	{min(times):.6f}s")

```
## procedure
	- pick a long query (5 words) so file IO has some effect.
	- in dependent variable is number of partitions
	- For each run, run the query 10 times, and take the query time.
	- dependent variable is average query time over ten runs

## Hypothesis
The goal is to see a curve where number of partitions reduces query time linearly.

Eventually, file I/O will have a greater effect on query time, so the curve should show a negative relationship until a certain point, and then spike up like a "v".

## Results
I did the partitioning, and the query time only went down for standard 5 term queries. I started the study at 5 partitions, and the query time was a little over 8 minutes. I optimized the code a little, and got the query time down to about 2 min 20 seconds. Then I started the study in earnest, doing 5, 10, 20, 50, 100, and 500 partitions. An increase in number of partitions linearly decreased the query time, even all the way to 500 partitions. The final query time for a 5 term query with 500 partitions was about 1 second, and I stopped there.

One interesting note however, is that I have the ability to create very long queries by adding the $ sign at the end of a stem. With a long query like this, it could take a very long time because each partition needs to be opened and closed. We are talking more than 30 minutes, so it might be worth it, to limit the number of query terms allowed at the user interface level, just to prevent extremely long queries.
