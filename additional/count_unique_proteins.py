import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to input CSV file")

args = parser.parse_args()

df = pd.read_csv(args.input_file)

unique_ids = len(df['refseq_id'].unique())

print("There are " + str(unique_ids) + " unique protein unique IDs in the input file.")
