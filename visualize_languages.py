import pandas as pd
import argparse
import matplotlib.pyplot as plt

def main(output_file_name, input_file_name):
    movies_df = pd.read_csv(input_file_name)

    # Turn the string of actors to a list of actors
    movies_df['languages'] = movies_df['languages'].apply(eval)

    movies_df = movies_df.explode('languages')

    # Calculate how many times each name is mentioned in the dataframe, 
    # take the top 50 of these names
    top_languages = movies_df['languages'].value_counts()
    top_languages = top_languages.head(10)

    # Remove irrelevant columns for this code
    columns = ['year', 'languages']
    movies_df = movies_df[columns]

    # Only keep track of movies that are made in a language in the top 10
    movies_df = movies_df[movies_df['languages'].isin(list(top_languages.index))]

    movies_df = movies_df.groupby(['year', 'languages']).size()
    movies_df = movies_df.reset_index()
    movies_df = movies_df.set_index('year')
    movies_df.columns = ['languages', 'count']

    languages_decade = {'English' : 0, 'French': 0, 'German': 0, 'Italian': 0, 'Spanish': 0, 'Japanese': 0, 'Russian' : 0, 'Latin' : 0, 'Mandarin': 0, 'Hindi': 0}
    i = 0
    languages_decades_list = []
    testn = 0
    currentYear = 1931
    decades = []

    for years in movies_df.index:
        if currentYear < years:
            if currentYear % 10 == 0:
                decades.append(currentYear)
                languages_decades_list.append(languages_decade)
                languages_decade = {'English' : 0, 'French': 0, 'German': 0, 'Italian': 0, 'Spanish': 0, 'Japanese': 0, 'Russian' : 0, 'Latin' : 0, 'Mandarin': 0, 'Hindi': 0}
                i = 0
        currentYear = years
        if len(movies_df.loc[years].values) > 2:
            for values in movies_df.loc[years].values:
                languages_decade[values[0]] = languages_decade[values[0]] + values[1]
        else:
            languages_decade[values[0]] = languages_decade[values[0]] + values[1]
        i += 1
        
    languages_df = pd.DataFrame(languages_decades_list, index = decades)

    languages_df_plotbar = languages_df.plot()
    languages_df_plotbar.get_figure().savefig(output_file_name)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top 10 languages from movies per year")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("output", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.input)