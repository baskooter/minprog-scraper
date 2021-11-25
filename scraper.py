# Name:
# Student number:
"""
Scrape top movies from www.imdb.com between start_year and end_year (e.g., 1930 and 2020)
Continues scraping until at least a top 5 for each year can be created.
Saves results to a CSV file
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
from math import ceil
import argparse
import requests

def main(output_file_name, start_year, end_year):
    page = 1
    movies_df = pd.DataFrame() 

    while True:
        IMDB_URL = f'https://www.imdb.com/search/title/?title_type=feature&release_date={str(start_year)}-01-01,{str(end_year)}-01-01&num_votes=5000,&sort=user_rating,desc&start={str(page)}&view=advanced'
        # Load website with BeautifulSoup
        html = requests.get(IMDB_URL, timeout=7) 
        dom = BeautifulSoup(html.text, features="lxml")
        
        # Extract movies from website
        movies_df = movies_df.append(extract_movies(dom))

        # Add 50 to the url to go to the next 50 movies in the list
        page+=50

        # Chcek if there are 5 movies for each year, or if 4000 movies have been added
        if not 0 in movies_df['year'].value_counts().values and not 1 in movies_df['year'].value_counts().values and not 2 in movies_df['year'].value_counts().values and not 3 in movies_df['year'].value_counts().values and not 4 in movies_df['year'].value_counts().values or page > 4001:
            break

    # Save correctly sorted results to output file
    movies_df = movies_df.sort_values(by = 'year')
    movies_df.to_csv(output_file_name, index=False)   

# Extraxts the movies from the current url
def extract_movies(dom):
    # Initialize the arrays for the data
    movie_title = []
    movie_year = []
    movie_rating = []
    movie_stars = []
    movie_duration = []
    movie_url = []

    # Look through the html of the site to add the data
    for movies in dom.find_all('div', class_='lister-item'):
        movie_title.append(movies.h3.a.text)
        movie_rating.append(movies.find('div', class_='ratings-imdb-rating').strong.text)
        movie_year_str = movies.h3.find('span', class_= 'lister-item-year')
        movie_year_str = movie_year_str.text
        movie_year_str = movie_year_str.replace('(', '').replace(')', '')
        if (len(movie_year_str.split(' ')) > 1):
            movie_year_str = movie_year_str.split(' ')[1]
        movie_year.append(movie_year_str)

        star_names = ""
        # There can be multiple stars for one movie, this loop adds all of them
        for stars in movies.find_all('p')[2]:
            for char in stars.text:
                if char.isalpha() or char == " " :
                    star_names += char
                if char == ",":
                    star_names += ";"
        if len(star_names.split("     ")) == 1:
            star_names = None
        else:
            star_names = star_names.split("     ")[1].replace('Stars', '').split(";")
        movie_stars.append(star_names)

        duration = movies.find('p', class_='text-muted').find('span', class_='runtime')
        duration_str = ""
        # Make sure only the correct characters get stored
        for char in duration.text:
            if char.isnumeric():
                duration_str += char
        movie_duration.append(duration_str)
    
        movie_url.append("https://www.imdb.com" + movies.h3.a['href'])

    data_dict = {'title': movie_title, 'year': movie_year, 'rating': movie_rating, 'actors': movie_stars, 'duration': movie_duration, 'url': movie_url}
    df = pd.DataFrame(data_dict)

    return df

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-s", "--start_year", type=int, default = 1930, help="starting year (default: 1930)")
    parser.add_argument("-e", "--end_year",   type=int, default = 2020, help="starting year (default: 2020)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.start_year, args.end_year)
