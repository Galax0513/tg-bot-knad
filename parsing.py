import requests
from bs4 import BeautifulSoup


URL = f"https://www.kinoafisha.info/rating/movies/"
r = requests.get(URL).text

soup = BeautifulSoup(r, "html.parser")

information = []
reiti = []
years = []
picture = []
i = -1
a = []
for data in soup.find_all('picture', class_='movieItem_poster picture picture-poster'):
    i += 1
    pic = data.source['srcset']
    pic = '//'.join(str(pic).split('/'))[8:]
    pic = 'https:' + str(pic)
    if 'jpeg' in str(pic) and 'jpeg' in str(pic):
        a.append(i)
    else:
        picture.append(pic)

k = -1
for data in soup.find_all('div', class_="movieItem_info"):
    k += 1
    title_film = data.a.text
    if k not in a:
        information.append(title_film)

c = -1
for el in soup.find_all('span', class_='movieItem_itemRating miniRating miniRating-good'):
    c += 1
    reit = el.text
    if c not in a:
        reiti.append(reit)

e = -1
for data in soup.find_all('span', class_='movieItem_year'):
    c += 1
    year_film = data.text
    if e not in a:
        years.append(year_film)
