
from benchmark import HashBenchmark

input_sizes = [10, 100, 1000, 10000]
num_iterations = [1000, 5000, 10000]

benchmark = HashBenchmark(input_sizes, num_iterations)
benchmark.run_benchmarks()