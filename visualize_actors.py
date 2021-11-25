import pandas as pd
import argparse
import matplotlib.pyplot as plt

def main(output_file_name, input_file_name):
    # Set the size of the png figure
    plt_1 = plt.figure(figsize=(15, 15))

    movies_df = pd.read_csv(input_file_name)

    # Turn the string of actors to a list of actors
    movies_df['actors'] = movies_df['actors'].apply(eval)

    movies_df = movies_df.explode('actors')

    # Remove some white spaces from the actor names
    movies_df['actors'] = movies_df['actors'].apply(str.lstrip)

    # Calculate how many times each name is mentioned in the dataframe, 
    # take the top 50 of these names
    movies_df = movies_df['actors'].value_counts()
    movies_df = movies_df.head(50)
    
    movies_df_plotbar = movies_df.plot(kind='bar', legend=None)
    movies_df_plotbar.get_figure().savefig(output_file_name)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("output", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.input)