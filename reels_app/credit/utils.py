import os
import inspect

from flask import current_app
from openpyxl import load_workbook
import tmdbsimple as tmdb

# tmdb.API_KEY = os.getenv('TMDB_API')
tmdb.API_KEY = '9dc3cebfcea4371070e9193ab068fd52'
tmdb.REQUESTS_TIMEOUT = 5


class Film:
    """
    DIR ####; SCR ####; PROD ####. U.S., 1984, color, 160 min. Lang. RATED PG
    """

    def __init__(self, title, imdb_id):
        self.title = title
        self.imdb_id = imdb_id
        self.tmdb_id = None  # done
        self.response = None
        self.directors = []
        self.writers = []
        self.producers = []
        self.countries = []
        self.release_date = None
        self.runtime = None  # done
        self.rating = None

    def get_tmdb_id(self):
        response = tmdb.Find(self.imdb_id).info(external_source='imdb_id')
        self.tmdb_id = response['movie_results'][0]['id']

    # def get_response(self):
    #     self.response = tmdb.Find(self.tmdb_id).info()

    def get_release_date(self):
        response = tmdb.Movies(self.tmdb_id).info()
        self.release_date = response['release_date'][:4]

    def get_runtime(self):
        response = tmdb.Movies(self.tmdb_id).info()
        self.runtime = response['runtime']


def build_film_list(directory):
    """Parse the uploaded workbook and build a dictionary out of the data."""

    directory = current_app.config['CREDITS_FOLDER']
    manifest = os.listdir(directory)[0]

    wb = load_workbook(filename=f'{directory}/{manifest}')
    ws = wb.active

    last_row = ws.max_row
    first_row = 2

    films = []

    for row in range(first_row, last_row):
        film = Film(title=ws.cell(row, 1).value,
                    imdb_id=ws.cell(row, 2).value)
        films.append(film)

    for film in films:
        # Each of the class's attributes will be populated in this loop
        film.get_tmdb_id()
        film.get_release_date()
        film.get_runtime()
        print(f'Title: {film.title}')
        print(f'TMDB ID: {film.tmdb_id}')
        print(f'Release Date: {film.release_date}')
        print(f'Runtime: {film.runtime}')
        print('-------')


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
