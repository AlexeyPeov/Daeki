import os

import requests
from bs4 import BeautifulSoup


def get_movie_rating():
    if not os.path.exists("rejected_movies.txt"):
        with open("rejected_movies.txt", "w") as f:
            pass

    while True:
        try:
            user_rating = float(input("Введите рейтинг фильма: "))
            if user_rating < 0 or user_rating > 10:
                print("Рейтинг должен быть в диапазоне от 0 до 10")
                continue
            break
        except ValueError:
            print("Введите число")

    with open("rejected_movies.txt", "r") as f:
        rejected_movies = f.read().splitlines()

    while True:
        url = f"https://www.imdb.com/chart/top?ref_=nv_mv_250"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_tags = soup.select("td.titleColumn a")
        ratings_tags = soup.select("td.posterColumn span[name='ir']")

        for i in range(len(movie_tags)):
            movie = movie_tags[i].text.strip()
            year = movie_tags[i]["title"].split()[-1]
            movie_rating = float(ratings_tags[i]["data-value"])
            if movie_rating >= user_rating and movie not in rejected_movies:
                print(f"Фильм: {movie} ({year}) Рейтинг: {movie_rating}")
                choice = input("Хотите посмотреть этот фильм? (y/n): ")
                if choice == "y":
                    return movie
                elif choice == "n":
                    with open("rejected_movies.txt", "a") as f:
                        f.write(f"{movie}\n")
                    continue

        print("Нет фильмов с таким рейтингом")
        break

get_movie_rating()