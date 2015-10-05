import sys
import string
import re
import glob
import re

from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk import pos_tag, ne_chunk
import numpy
import nltk

movie_genre =[]
porterstemmer = PorterStemmer()
stemming = LancasterStemmer()

genres = open('moviegenre.txt', 'r')
genres_list = []
for lines in genres.readlines():
    genres_list.append(lines.decode('ascii', 'ignore').strip().lower())

producer = open('film_production_companies.txt', 'r')
producers_list = []
for lines in producer.readlines():
    producers_list.append(lines.decode('ascii', 'ignore').strip().lower())

directors = open('notable_directors.txt', 'r')
directors_list = []
for lines in directors.readlines():
    directors_list.append(lines.decode('ascii', 'ignore').strip().lower())

actors = open('actors.txt', 'r')
actors_list = []
for lines in actors.readlines():
    actors_list.append(lines.decode('ascii', 'ignore').strip().lower())
print actors_list


def name_function(baseline):
    movieline = baseline.rstrip()
    fullname = line.split('|')[0]
    name = fullname.split('(')[0]
    return name


def list_onexists(name_list, baseline):
    itemset_in_wiki = []
    try:
        for names in name_list:
            name = str(names).split()
            fname = name[0]
            lname = ""
            if len(name) > 1:
                lname = porterstemmer.stem(name[1])
            if porterstemmer.stem(fname) in baseline:
                indexofbaseline = baseline.index(porterstemmer.stem(fname))

                item_lastname = baseline[indexofbaseline + 1]
                if lname == "":
                    itemset_in_wiki.append(names)
                if lname == item_lastname:
                    itemset_in_wiki.append(names)

    except Exception, e:
        pass
    return itemset_in_wiki


def revenue_function(baseline):
    line1 = baseline.strip()
    total = []
    x = []
    y = []
    revenueline = re.findall('([^.]*?(?:intern|gross|sale|earn|worldwide)[^.]*\.)', line1)
    revenueline = filter(None, revenueline)
    if len(revenueline) > 0:
        for i in range(len(revenueline)):
            first = re.findall('\$\ ?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{1,2})?', revenueline[i])
            second = re.findall('\$\ ?[0-9]{1,3}(?:million)?', revenueline[i])
            x.extend(first)
            y.extend(second)
    elif len(revenueline) == 0:
        revenue = "null"
    if len(x) > 0:
        for i in range(len(x)):
            a = x[i]
            a = re.sub('[$,]', '', a)
            x[i] = int(float(a))
    if len(y) > 0:
        for i in range(len(y)):
            b = y[i]
            b = re.sub('[$, million]', '', b)
            c = float(b)
            d = c * 1000000
            y[i] = int(d)
    total = x + y
    if len(total) == 0:
        revenue = "null"
    elif len(total) > 0:
        revenue = max(total)
    return revenue


def opening_weekend_function(baseline):
    line1 = baseline.strip()
    total = []
    x = []
    y = []
    revenueline = re.findall('([^.]*?(?:weekend)[^.]*\.[^.]*\.[^.]*)', line1)
    revenueline = filter(None, revenueline)
    if len(revenueline) > 0:
        for i in range(len(revenueline)):
            first = re.findall('\$\ ?[0-9]{1,3}(?:,?[0-9])*(?:\.[0-9]{1,2})?', revenueline[i])
            second = re.findall('\$\ ?[0-9]{1,3}(?:million)?', revenueline[i])
            x.extend(first)
            y.extend(second)
    elif len(revenueline) == 0:
        revenue = "null"
    if len(x) > 0:
        for i in range(len(x)):
            a = x[i]
            a = re.sub('[$,]', '', a)
            x[i] = int(float(a))
    if len(y) > 0:
        for i in range(len(y)):
            b = y[i]
            b = re.sub('[$, million]', '', b)
            c = float(b)
            d = c * 1000000
            y[i] = int(d)
    total = x + y
    if len(total) == 0:
        revenue = "null"
    elif len(total) > 0:
        revenue = max(total)
    return revenue


def year_function(baseline):
    yearline1 = baseline.split('|')[2]
    year1 = re.findall('(?:\d\1)?(\d{4})', yearline1)
    if len(year1) > 0:
        year = year1[0]
    else:
        year = "null"
    return year


def director_backup_function(line1):
    line1 = line1.decode('ascii', 'ignore').strip().lower()
    words = line1.split()
    baseline = []
    director_in_wiki = []
    for word in words:
        if word not in stopwords.words('english'):
            baseword = porterstemmer.stem(word)
            baseline.append(baseword.strip())
    director_in_wiki = list_onexists(directors_list, baseline)
    if len(director_in_wiki) > 0:
        return director_in_wiki[0]
    else:
        return "null"


def director_function(baseline):
    line1 = baseline.rstrip()
    director = []
    directorbaseline = re.findall('([^.]*?(?:directed|Directed|director)[^.]*\.[^.]*\.[^.]*)', line1)
    directorline = re.findall(
        '(?:directed|Directed|director\s)(.*?)(?:\.|based|;|and|with|about|for|who|from|which|adapted)', line1)
    if len(directorline) > 0:
        director1 = directorline[0].split('by ')
        if len(director1) == 1:
            director = director1[0]
        elif len(director1) > 1:
            director = director1[1]
        elif len(director1) == 0:
            director = "null"
    if director != "null":
        if len(director) > 0:
            if len(directorbaseline) > 0:
                if len(director) > 25:
                    director = director_backup_function(directorbaseline[0])
    else:
        director = "null"
    return director


def production_company(line1):
    line1 = line1.decode('ascii', 'ignore').strip().lower()
    words = line1.split()
    baseline = []
    production_company_ = []
    for word in words:
        if word not in stopwords.words('english'):
            baseword = porterstemmer.stem(word)
            baseline.append(baseword.strip())
    production_company_ = list_onexists(producers_list, baseline)
    if len(production_company_) > 0:
        return production_company_[0]
    else:
        return "null"


def actor_function(line1):
    line2 = line1[:750]
    line3 = line2.decode('ascii', 'ignore').strip().lower()
    words = line3.split()
    baseline = []
    for word in words:
        if word not in stopwords.words('english'):
            baseword = porterstemmer.stem(word)
            baseline.append(baseword.strip())
    actorsname = list_onexists(actors_list, baseline)
    if len(actorsname) > 0:
        actors_names = ','.join(actorsname)
        return actors_names
    else:
        return "null"

"""
genre = open('moviegenre.txt', 'r')
genre_list = {}
action_list = []
comedy_list = []
drama_list = []
horror_list = []
scifi_list = []
thriller_list = []
documentary_list = []
for lines in genre.readlines():
    line = lines.split()
    if line[0].lower() == 'action':
        action_list.append(line[1].lower())
    if line[0].lower() == 'comedy':
        comedy_list.append(line[1].lower())
    if line[0].lower() == 'drama':
        drama_list.append(line[1].lower())
    if line[0].lower() == 'horror':
        horror_list.append(line[1].lower())
    if line[0].lower() == 'scifi':
        scifi_list.append(line[1].lower())
    if line[0].lower() == 'thriller':
        thriller_list.append(line[1].lower())
    if line[0].lower() == 'documentary':
        documentary_list.append(line[1].lower())


def genre_function(baseline):
    line1 = baseline.decode('ascii', 'ignore').strip().lower()  # Ignore all the non-ascii values in a string
    words = line1.split()
    baseline = []
    for word in words:
        if word not in stopwords.words('english'):
            baseword = porterstemmer.stem(word)
        else:
            baseline.append(baseword.strip())
    genre_type = ['action', 'comedy', 'drama', 'horror', 'scifi', 'thriller', 'documentary']
    genre_list = [0, 0, 0, 0, 0, 0, 0]
    movie_type = []

    for word in baseline:
        if word in action_list:
            genre_list[0] = genre_list[0] + 1
        if word in comedy_list:
            genre_list[1] = genre_list[1] + 1

        if word in drama_list:
            genre_list[2] = genre_list[2] + 1

        if word in horror_list:
            genre_list[3] = genre_list[3] + 1
        if word in scifi_list:
           genre_list[4] = genre_list[4] + 1

        if word in thriller_list:
            genre_list[5] = genre_list[5] + 1

        if word in documentary_list:
            genre_list[5] = genre_list[5] + 1

    if max(genre_list) > 1:
        indices = [i for i, x in enumerate(genre_list) if x == max(genre_list)]

        for index in indices:
            movie_type.append(genre_type[index])
        return ','.join(movie_type)
    else:
        return ''
"""
"""
def genre_function(baseline):
    movie_genre =[]
    line_1 = baseline.decode('ascii', 'ignore').strip().lower()
    genre_line = line_1.split('|')[2]
    movie_genre_line = genre_line.split('.')[0]
    for genre_name in genres_list:
        if genre_name in movie_genre_line:
            print movie_genre_line
            movie_genre.append(genre_name)
    string = ', '
    movie_genre_list = string.join(movie_genre)
    if len(movie_genre) > 0:
        return movie_genre_list
    else:
        return "null" """

def genre_function(genre_line1):
    genre_line2 = genre_line1[:200]
    print genre_line2
    genre_line3 = genre_line2.decode('ascii', 'ignore').strip().lower()
    #print line3
    words = genre_line3.split()
    baseline = []
    for word in words:
        if word not in stopwords.words('english'):
            baseword = porterstemmer.stem(word)
            baseline.append(baseword.strip())
    movie_genres = list_onexists(genres_list, baseline)
    if len(movie_genres) > 0:
        genre_names = ','.join(movie_genres)
        return genre_names
    else:
        return "null"




hand = open('title_output_again.txt')
wfile = open('movieoutput.txt', 'a')
for line in hand:
    baseline = line
    year = str(year_function(baseline))
    revenue = str(revenue_function(baseline))
    opening_weekend = str(opening_weekend_function(baseline))
    name = str(name_function(baseline))
    genre = str(genre_function(baseline))
    production = str(production_company(baseline))
    director = str(director_function(baseline))
    actors = str(actor_function(baseline))
    # print name_function(baseline),"|",year_function(baseline),"|",revenue_function(baseline),"|",opening_weekend_function(baseline),"|",director_function(baseline),"|",genre_function(baseline),"|",production_company(baseline)
    printline = name + '|' + year + '|' + revenue + '|' + opening_weekend + '|' + director + '|' + genre + '|' + production + '|' + actors + '\n'
    print printline
    wfile.write(printline)
wfile.close()


