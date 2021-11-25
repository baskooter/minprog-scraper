import pandas as pd
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def main(output_file_name, input_file_name):
    movies_df = pd.read_csv(input_file_name)

    
    fig = plt.figure()
    # Instead of set_figwidth(30)
    fig.set_size_inches(30, fig.get_figheight(), forward=True)

    # Remove the data that is irrelevant for this code from the dataframe
    # Get the average rating per movie
    movies_df = movies_df[['year', 'rating']].groupby('year').mean('rating')
    
    movies_df_plotbar = movies_df.plot(kind='bar', legend=None)

    # For better visibility, skip the naming of every other year
    myLocator = mticker.MultipleLocator(2)
    movies_df_plotbar.xaxis.set_major_locator(myLocator)

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