import requests
import json
import random
import os


def get_movie(min_rating, max_rating, exceptions, liked):
    # Получаем случайный фильм из TMDB с рейтингом в заданном диапазоне

    #page = 1

    #url = f"https://api.themoviedb.org/3/discover/movie?api_key=fb3b3e4a8c47e10407fa8a54e2010d5e&language=ru-RU&sort_by=popularity.desc&include_adult=false&include_video=false&page={page}&vote_average.gte={min_rating}&vote_average.lte={max_rating}"
    url = f"https://api.themoviedb.org/3/discover/movie?api_key=fb3b3e4a8c47e10407fa8a54e2010d5e&language=ru-RU&sort_by=popularity.desc&include_adult=false&include_video=false&vote_average.gte={min_rating}&vote_average.lte={max_rating}"
    response = requests.get(url)
    data = json.loads(response.text)


    if data['total_results'] == 0:
        print("NO RESULTS")
        return None
    else:
        results = data['results']
        available_movies = [movie for movie in results if movie['title'] not in exceptions and movie['title'] not in liked and movie['overview']]
        if not available_movies:
            available_movies = [movie for movie in results if
                                movie['title'] not in exceptions and movie['title'] not in liked]

            if(not available_movies):
                return None

        random_movie = random.choice(available_movies)
        movie_id = random_movie['id']
        movie_title = random_movie['title']

        movie_overview = random_movie['overview']

        if(not random_movie['overview']):
            movie_overview = "Нет описания.."


        if(len(movie_overview) > 350):
            movie_overview = movie_overview[0:350] + "..."


        movie_rating = random_movie['vote_average']
        poster_path = random_movie['poster_path']
        return (movie_id, movie_title, movie_overview, movie_rating, poster_path)


def write_to_file(file_path, data):
    # Записываем данные в файл
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(data + "\n")


def read_from_file(file_path):
    # Читаем данные из файла и возвращаем список
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        data = [line.strip() for line in lines]
        return data


def init_movie_finder():
    # Создаем файлы исключений и понравившихся фильмов, если их еще нет
    if not os.path.exists("exceptions.txt"):
        open("exceptions.txt", "w").close()
    if not os.path.exists("liked.txt"):
        open("liked.txt", "w").close()

    # Получаем списки названий фильмов из файлов исключений и понравившихся фильмов
    exceptions = read_from_file("exceptions.txt")
    liked = read_from_file("liked.txt")



    return (exceptions, liked)


def main():
    # Создаем файлы исключений и понравившихся фильмов, если их еще нет
    if not os.path.exists("exceptions.txt"):
        open("exceptions.txt", "w").close()
    if not os.path.exists("liked.txt"):
        open("liked.txt", "w").close()

    # Получаем минимальный и максимальный рейтинг от пользователя
    min_rating = float(input("Введите минимальный рейтинг: "))
    max_rating = float(input("Введите максимальный рейтинг: "))

    # Получаем списки названий фильмов из файлов исключений и понравившихся фильмов
    exceptions = read_from_file("exceptions.txt")
    liked = read_from_file("liked.txt")

    while True:
        movie_data = get_movie(min_rating, max_rating, exceptions, liked)

        if movie_data is None:
            print("Нет фильмов в заданном диапазоне.")
            break

        movie_id, movie_title, movie_overview, movie_rating, poster_path = movie_data

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
            # Записываем понравившийся фильм в файл liked.txt
            write_to_file("liked.txt", movie_title)
            liked.append(movie_title)  # Добавляем фильм в список понравившихся
            continue_answer = input("Хотите продолжить поиск? (y/n) ")
            if continue_answer.lower() != "y":
                break

        else:
            # Записываем название фильма в файл исключений и добавляем его в список исключений
            write_to_file("exceptions.txt", movie_title)
            exceptions.append(movie_title)


if __name__ == "__main__":
    main()