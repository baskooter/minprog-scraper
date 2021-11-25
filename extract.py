import pandas as pd
import argparse

def main(output_file_name, input_file_name, topN):
    movies_df = pd.read_csv(input_file_name)

    movies_df = movies_df.groupby('year').head(topN)
    movies_df.to_csv(output_file_name, index=False)   

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("-n", "--topN",   type=int, default = 5, help="Top N movies")
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("output", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.input, args.topN)