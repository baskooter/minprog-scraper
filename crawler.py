# Name: Bas Kooter
# Student number:

from helpers import simple_get
from bs4 import BeautifulSoup
import pandas as pd
from math import ceil
import argparse
import requests

def main(output_file_name, input_file_name):

    movies_df = pd.read_csv(input_file_name)
    languages_list = []

    for url in movies_df['url']:
        IMDB_URL = url
        
        # Load website with BeautifulSoup
        html = requests.get(IMDB_URL, timeout=7) 
        dom = BeautifulSoup(html.text, features="lxml")

        # Extract languages from website
        languages_list.append(extract_language(dom))

    movies_df['languages'] = languages_list

    # Reorder the columns
    columns = ['title','rating','year','actors','languages','duration', 'url']
    movies_df = movies_df[columns]
    
    # Save results to output file
    movies_df.to_csv(output_file_name, index=False)   

# Extraxts the movies from the current url
def extract_language(dom):
    language_list = []

    languages = dom.find('section', attrs={"data-testid":"Details"})
    languages = languages.find('li', attrs={"data-testid":"title-details-languages"})
    languages = languages.find_all('a')
    for i in range(len(languages)):
        language_list.append(languages[i].text)
    return language_list

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
