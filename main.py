import requests
import json
import random
import os


def get_movie(min_rating, max_rating):
    # Получаем случайный фильм из TMDB с рейтингом в заданном диапазоне
    url = f"https://api.themoviedb.org/3/discover/movie?api_key=fb3b3e4a8c47e10407fa8a54e2010d5e&language=ru-RU&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&vote_average.gte={min_rating}&vote_average.lte={max_rating}"
    response = requests.get(url)
    data = json.loads(response.text)
    if data['total_results'] == 0:
        return None
    else:
        results = data['results']
        random_movie = random.choice(results)
        movie_id = random_movie['id']
        movie_title = random_movie['title']
        movie_overview = random_movie['overview']
        movie_rating = random_movie['vote_average']
        poster_path = random_movie['poster_path']
        return (movie_id, movie_title, movie_overview, movie_rating, poster_path)


def write_to_file(movie_id):
    # Записываем ID фильма в файл исключений
    with open("exceptions.txt", "a") as file:
        file.write(str(movie_id) + "\n")


def read_from_file():
    # Читаем ID фильмов из файла исключений
    with open("exceptions.txt", "r") as file:
        lines = file.readlines()
        exceptions = [int(line.strip()) for line in lines]
        return exceptions


def main():
    # Создаем файл исключений, если его еще нет
    if not os.path.exists("exceptions.txt"):
        open("exceptions.txt", "w").close()

    # Получаем минимальный и максимальный рейтинг от пользователя
    min_rating = float(input("Введите минимальный рейтинг: "))
    max_rating = float(input("Введите максимальный рейтинг: "))

    # Получаем список ID фильмов из файла исключений
    exceptions = read_from_file()

    while True:
        # Получаем случайный фильм из TMDB с рейтингом в заданном диапазоне
        movie_data = get_movie(min_rating, max_rating)

        if movie_data is None:
            print("Нет фильмов в заданном диапазоне.")
            break

        movie_id, movie_title, movie_overview, movie_rating, poster_path = movie_data

        if movie_id in exceptions:
            continue

        print(f"Название: {movie_title}")
        print(f"Описание: {movie_overview}")
        print(f"Рейтинг: {movie_rating}")

        # Выводим постер фильма
        base_url = "https://image.tmdb.org/t/p/w500"
        poster_url = base_url + poster_path if poster_path else "https://via.placeholder.com/500x750.png?text=No+poster+available"
        print(f"Постер: {poster_url}")

        # Спрашиваем пользователя, хочет ли он посмотреть этот фильм
        answer = input("Хотите посмотреть этот фильм? (y/n) ")

        if answer.lower() == "y":
            break
        else:
            write_to_file(movie_id)


if __name__ == "__main__":
    main()
