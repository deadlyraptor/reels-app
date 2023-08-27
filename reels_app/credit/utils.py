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
        self.movie_info = None  # done
        self.directors = []
        self.writers = []
        self.producers = []
        self.countries = []  # done
        self.languages = []  # done
        self.release_date = None  # done
        self.runtime = None  # done
        self.genres = []  # done
        self.rating = None

    def get_tmdb_id(self):
        response = tmdb.Find(self.imdb_id).info(external_source='imdb_id')
        self.tmdb_id = response['movie_results'][0]['id']

    def get_movie_info(self):
        self.movie_info = tmdb.Movies(self.tmdb_id).info()

    def get_release_date(self):
        self.release_date = self.movie_info['release_date'][:4]

    def get_runtime(self):
        self.runtime = self.movie_info['runtime']

    def get_countries(self):
        production_countries = self.movie_info['production_countries']
        countries = []
        for country in production_countries:
            countries.append(country['name'])
        self.countries = countries

    def get_languages(self):
        spoken_languages = self.movie_info['spoken_languages']
        languages = []
        for language in spoken_languages:
            languages.append(language['english_name'])
        self.languages = languages

    def get_genres(self):
        tmdb_genres = self.movie_info['genres']
        genres = []
        for genre in tmdb_genres:
            genres.append(genre['name'])
        self.genres = genres

    def get_crew(self):
        """Return the director(s), screenwriter(s), and producer(s) of the
        queried film."""

        crew = tmdb.Movies(self.tmdb_id).credits()['crew']

        for crew_member in crew:
            if crew_member['job'] == 'Director':
                self.directors.append(crew_member['name'])
            if crew_member['job'] == 'Screenplay':
                self.writers.append(crew_member['name'])
            if crew_member['job'] == 'Producer':
                self.producers.append(crew_member['name'])


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
        film.get_movie_info()
        film.get_release_date()
        film.get_runtime()
        film.get_countries()
        film.get_languages()
        film.get_genres()
        film.get_crew()
        print(f'Title: {film.title}')
        print(f'TMDB ID: {film.tmdb_id}')
        print(f'Release Date: {film.release_date}')
        print(f'Runtime: {film.runtime}')
        print(f'Countries: {film.countries}')
        print(f'Languages: {film.languages}')
        print(f'Genres: {film.genres}')
        print(f'Directors: {film.directors}')
        print(f'Writers: {film.writers}')
        print(f'Producers: {film.producers}')
        print('-------')
