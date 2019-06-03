import sys
from bs4 import BeautifulSoup
import requests
import re

url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

imdb = []
actor_movies_mapping ={}
n_of_movies = raw_input("How many number of movies, do you want to search ? ")
movies = movies[:int(n_of_movies)]

for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]

    year = re.search('\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index))-(len(movie))]
    star_cast = crew[index].split(',')

    for actor in star_cast:
      if actor_movies_mapping.get(actor):
        actor_movies_mapping[actor].append(movie_title)
      else:
        actor_movies_mapping[actor.strip()] = [movie_title]

    data = {"movie_title": movie_title,
            "place": place,
            "star_cast": crew[index]}
    imdb.append(data)

for item in imdb:
    print item['place'], '-', item['movie_title'], 'Starring:', item['star_cast']

actor_name = raw_input("Please enter actor's name :")
n_top_movies = raw_input("Please enter M :")

actor_movies = actor_movies_mapping.get(actor_name)

if not actor_movies:
   print 'Actor did not act in top %s movies' %n_of_movies
   sys.exit()

length = int(n_top_movies)
if n_top_movies > len(actor_movies):
   length = len(actor_movies)

print '%s top %s movies are:' %(actor_name,n_top_movies)
for i in range(0,length):
   print str(i+1) + '. '+actor_movies[i]
   


