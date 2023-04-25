import random
import textwrap

import requests
from bs4 import BeautifulSoup

while True:
    min_rating = float(input("Введите минимальный рейтинг (от 0 до 10): "))
    if min_rating < 0 or min_rating > 10:
        print("Пожалуйста, введите число от 0 до 10.")
    else:
        break

url = "https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series&user_rating=" + str(min_rating) + "," + str(min_rating+0.1)


response = requests.get(url)

soup_first = BeautifulSoup(response.text, "html.parser")
desc_div = soup_first.select_one(".desc span:nth-of-type(1)")
available_movies_text = desc_div.text
available_movies = int(available_movies_text.split()[-2].replace(',', ''))
print(available_movies)

url_precise = "https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series&user_rating=" \
        + str(min_rating) + "," + str(min_rating+0.1) \
        + "&start=" + str((random.randint(1, available_movies // 50) * random.randint(1, 50)) + 1) + "&ref_=adv_nxt"

response_precise = requests.get(url_precise)

soup = BeautifulSoup(response_precise.text, "html.parser")

movies = soup.select(".lister-item-header a")
ratings = soup.select(".ratings-imdb-rating")

years = soup.select(".lister-item-year.text-muted.unbold")
descriptions = soup.select(".lister-item-content p:nth-of-type(2)")


movies_ratings = []
for movie, rating, year, description in zip(movies, ratings, years, descriptions):
    title = movie.text
    rating_value = float(rating.strong.text)
    year_value = year.text.strip("()")
    description_value = description.text.strip()

    if not description_value or description_value == "Add a Plot":
        description_value = "No description"

    movies_ratings.append((title, rating_value, year_value, description_value))

random_entry = random.choice(movies_ratings)
movie, rating, year, description = random_entry

wrapped_description = textwrap.wrap(description, width=50)

with open("movies.txt", "r", encoding="utf-8") as f:
    printed_movies = [line.strip().split(",")[0] for line in f]
    if movie not in printed_movies:
        print(f"{movie} ({year}), {rating}")
        for line in wrapped_description:
            print(line)
        with open("movies.txt", "a", encoding="utf-8") as file:
            file.write(f"{movie}, {year}\n")


    # while True:
    #     for i in range(len(movies)):
    #         with open('movies.txt', 'r', encoding='utf-8', errors='ignore') as f:
    #             if movies[i].text in f.read():
    #                 continue
    #         print(movies[i].text + " - " + ratings[i].text.strip())
    #         while True:
    #             choice = input("Вам нравится фильм? (да/нет): ")
    #             if choice.lower() == 'да' or choice.lower() == 'нет':
    #                 break
    #             else:
    #                 print("Пожалуйста, введите 'да' или 'нет'.")
    #         if choice.lower() == 'да':
    #             print("Отлично! Наслаждайтесь просмотром!")
    #             break
    #         else:
    #             file.write(movies[i].text + " - " + ratings[i].text.strip() + "\n")
    #     if choice.lower() == 'да':
    #         break
    #     next_url = soup.select(".desc a")[-1]['href']
    #     next_response = requests.get("https://www.imdb.com" + next_url)
    #     soup = BeautifulSoup(next_response.text, "html.parser")
    #     movies = soup.select(".lister-item-header a")
    #     ratings = soup.select(".ratings-imdb-rating")
    #     if not movies:
    #         break
