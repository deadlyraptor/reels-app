import os

from flask import current_app
from openpyxl import load_workbook
import tmdbsimple as tmdb

# tmdb.API_KEY = os.getenv('TMDB_API')
tmdb.API_KEY = '9dc3cebfcea4371070e9193ab068fd52'
tmdb.REQUESTS_TIMEOUT = 5


def build_film_dict(directory):
    """Parse the uploaded workbook and build a dictionary out of the data."""

    directory = current_app.config['CREDITS_FOLDER']
    manifest = os.listdir(directory)[0]

    wb = load_workbook(filename=f'{directory}/{manifest}')
    ws = wb.active

    last_row = ws.max_row
    first_row = 2

    films = []

    for row in range(first_row, last_row):
        film = dict(film_title=ws.cell(row, 1).value,
                    imdb_id=ws.cell(row, 2).value)
        films.append(film)


def get_movie_id(query):
    """Get the movie's TMDB id."""
    search = tmdb.Search()
    response = search.movie(query=query)
    if search.results:
        return search.results[0]['id']
    else:
        return


def get_year(movie_id):
    """Return the release year of the queried film."""
    movie = tmdb.Movies(movie_id)
    # print(movie.info()['release_date'][:4])
    return movie.info()['release_date'][:4]


def get_crew(movie_id):
    """Return the director(s), screenwriter(s), and producer(s) of the queried
    film."""
    movie = tmdb.Movies(movie_id)

    crew_list = movie.credits()['crew']

    directors = []
    screenwriters = []
    producers = []

    for crew in crew_list:
        # get director
        if crew['job'] == 'Director':
            directors.append(crew['name'])
        if crew['job'] == 'Story':
            screenwriters.append(crew['name'])
        if crew['job'] == 'Producer':
            producers.append(crew['name'])

    print(directors, screenwriters, producers)
    return directors, screenwriters, producers
