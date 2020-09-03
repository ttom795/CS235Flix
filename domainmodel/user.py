from domainmodel.movie import Movie
from domainmodel.review import Review


class User:
    def __init__(self, user_name, password):
        self.__user_name = user_name.strip().lower()
        self.__password = password
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @user_name.setter
    def user_name(self, object_input):
        self.__user_name = object_input

    @password.setter
    def password(self, object_input):
        self.__password = object_input

    @watched_movies.setter
    def watched_movies(self, object_input):
        self.__watched_movies = object_input

    @reviews.setter
    def reviews(self, object_input):
        self.__reviews = object_input

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, object_input):
        self.__time_spent_watching_movies_minutes = object_input

    def __repr__(self):
        return "<User " + self.__user_name + ">"

    def __eq__(self, toCompare):
        return (self.__user_name == toCompare.__user_name)

    def __lt__(self, toCompare):
        return (self.__user_name < toCompare.__user_name)

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie):
        self.__watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        self.__reviews.append(review)