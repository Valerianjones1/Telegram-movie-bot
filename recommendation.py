from re import M
import pandas as pd
import numpy as np
import random


ratings_data = pd.read_csv(
    "./Dataset/ratings.csv")

movie_names = pd.read_csv(
    "./Dataset/movies.csv")
movie_data = pd.merge(ratings_data, movie_names, on='movieId')

data_movie = dict()


def start_movies():
    ratings_mean_count = pd.DataFrame(
        movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(
        movie_data.groupby('title')['rating'].count())
    m = ratings_mean_count[ratings_mean_count["rating_counts"] > 50].sort_values(
        "rating", ascending=False)
    random_movie = m[m["rating"] >= 3.5]
    random_movie = random_movie.reset_index()
    int_rnd = random.randint(0, 300)
    return random_movie["title"][int_rnd]


def reccomend_movie(movie, cursor):
    if movie not in data_movie:
        data_movie[movie] = 1
    else:
        data_movie[movie] += 1

    ratings_mean_count = pd.DataFrame(
        movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(
        movie_data.groupby('title')['rating'].count())
    user_movie_rating = movie_data.pivot_table(
        index='userId', columns='title', values='rating')
    movie_ratings = user_movie_rating[movie]
    movies_like = user_movie_rating.corrwith(movie_ratings)

    corr_forrest_gump = pd.DataFrame(
        movies_like, columns=['Correlation'])
    corr_forrest_gump.dropna(inplace=True)
    corr_forrest_gump = corr_forrest_gump.join(
        ratings_mean_count['rating_counts'])
    s = corr_forrest_gump[corr_forrest_gump['rating_counts']
                          > 50].sort_values('Correlation', ascending=False)
    s = dict(s["Correlation"])
    del s[movie]
    sql_m = [line[1]
             for line in cursor.execute("SELECT * FROM movies").fetchall()]
    while True:

        if list(s.keys())[data_movie[movie]] in sql_m:
            data_movie[movie] += 1
        else:
            break

    return list(s.keys())[data_movie[movie]]
