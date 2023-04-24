import requests
from bs4 import BeautifulSoup

while True:
    min_rating = float(input("Введите минимальный рейтинг (от 0 до 10): "))
    if min_rating < 0 or min_rating > 10:
        print("Пожалуйста, введите число от 0 до 10.")
    else:
        break

while True:

    max_rating = float(input("Введите максимальный рейтинг (от 0 до 10): "))
    if max_rating < 0 or max_rating > 10:
        print("Пожалуйста, введите число от 0 до 10.")
    else:
        break

url = "https://www.imdb.com/search/title?user_rating=" + str(min_rating) + "," + str(max_rating)
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select(".lister-item-header a")
ratings = soup.select(".ratings-imdb-rating")

with open('movies.txt', 'a', encoding='utf-8', errors='ignore') as file:
    while True:
        for i in range(len(movies)):
            with open('movies.txt', 'r', encoding='utf-8', errors='ignore') as f:
                if movies[i].text in f.read():
                    continue
            print(movies[i].text + " - " + ratings[i].text.strip())
            while True:
                choice = input("Вам нравится фильм? (да/нет): ")
                if choice.lower() == 'да' or choice.lower() == 'нет':
                    break
                else:
                    print("Пожалуйста, введите 'да' или 'нет'.")
            if choice.lower() == 'да':
                print("Отлично! Наслаждайтесь просмотром!")
                break
            else:
                file.write(movies[i].text + " - " + ratings[i].text.strip() + "\n")
        if choice.lower() == 'да':
            break
        next_url = soup.select(".desc a")[-1]['href']
        next_response = requests.get("https://www.imdb.com" + next_url)
        soup = BeautifulSoup(next_response.text, "html.parser")
        movies = soup.select(".lister-item-header a")
        ratings = soup.select(".ratings-imdb-rating")
        if not movies:
            break
