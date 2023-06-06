import argparse
import pandas as pd

# Set up argparse to accept an input CSV file
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to input CSV file")

args = parser.parse_args()

# Read in the input CSV file using pandas
df = pd.read_csv(args.input_file)

# Get the number of unique protein unique IDs
unique_ids = len(df['refseq_id'].unique())

print("There are " + str(unique_ids) + " unique protein unique IDs in the input file.")
