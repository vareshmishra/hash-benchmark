import hashlib
import timeit
import pandas as pd

class HashBenchmark:
    def __init__(self, input_sizes, num_iterations):
        """
        Initializes the HashBenchmark object with the given input sizes and 
        number of iterations, and creates empty dictionaries for storing the 
        benchmark results.
        
        Parameters:
        input_sizes (list): List of integers representing different input sizes to be used in benchmarking.
        num_iterations (list): List of integers representing different numbers of iterations to be used in benchmarking.
        """
        self.input_sizes = input_sizes
        self.num_iterations = num_iterations
        
        self.sha256_results = {}
        self.blake2b_results = {}
        
    def benchmark(self, algorithm, data, num_iterations, **kwargs):
        """
        Times the execution of a given algorithm function using the provided data and 
        number of iterations, and returns the time taken.
        
        Parameters:
        algorithm (function): The hash algorithm function to be timed.
        data (bytes): The data to be hashed.
        num_iterations (int): The number of times to run the algorithm.
        **kwargs: Any additional keyword arguments required by the algorithm function.
        """
        return timeit.timeit(lambda: algorithm(data, **kwargs), number=num_iterations)
    
    def run_benchmarks(self):
        """
        Runs the benchmarking of SHA-256 and BLAKE2b hash algorithms on the 
        specified input sizes and number of iterations, and saves the results to CSV files.
        """
        for input_size in self.input_sizes:
            data = b'0' * input_size
            self.sha256_results[input_size] = {}
            self.blake2b_results[input_size] = {}
            for n in self.num_iterations:
                sha256_time = self.benchmark(hashlib.sha256, data, n)
                blake2b_time = self.benchmark(hashlib.blake2b, data, n, digest_size=32)
                self.sha256_results[input_size][n] = sha256_time
                self.blake2b_results[input_size][n] = blake2b_time
        
        # Convert results dictionaries to Pandas DataFrames
        self.sha256_df = pd.DataFrame(self.sha256_results).round(4)
        self.blake2b_df = pd.DataFrame(self.blake2b_results).round(4)
        
        # Set DataFrames' row and column names
        self.sha256_df.index.name = 'Iterations'
        self.blake2b_df.index.name = 'Iterations'
        self.sha256_df.columns.name = 'Input size'
        self.blake2b_df.columns.name = 'Input size'
        
        # Set display options for Pandas DataFrames
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 100)
        
        # Write DataFrames to CSV files
        self.sha256_df.to_csv('sha256_data.csv', index=False)
        self.blake2b_df.to_csv('blake2b_data.csv', index=False)
        
        # Print the DataFrames as tables
        print("SHA-256 times:\n", self.sha256_df)
        print("\nBLAKE2b times:\n", self.blake2b_df)
