import requests
from bs4 import BeautifulSoup
from aiogram.utils.markdown import hlink
import random


# Возвращает текст html страницы, находящейся по адресу, указанном в url
def get_html(url):
    response = requests.get(url)

    if response.ok:
        return response.text
    else:
        return None


# Возвращает топ-10 аниме (сериалы, фильмы, OVA или ONA в зависимости от запроса)
def get_top(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all('tr', class_='ranking-list')
    response_text = ''

    for i in range(0, 10):
        title_name = titles[i].find('td', class_='title al va-t word-break').find('div', class_='di-ib clearfix').find('h3').text
        title_link = titles[i].find('td', class_='title al va-t word-break').find('div', class_='di-ib clearfix').find('a').get('href')
        title_score = titles[i].find('td', class_='score ac fs14').find('span').text

        htext =  hlink(title_name, title_link)
        response_text += '{}) '.format(i+1) + htext + '\nScore: {}\n'.format(title_score)

    return response_text


# Возвращает рандомный список с информацией о десяти аниме текущего сезона
def get_seasonal_anime(html):
    soup = BeautifulSoup(html, 'lxml')
    new_tv = soup.find('div', class_='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1 clearfix')\
        .find_all('div', class_='seasonal-anime js-seasonal-anime')
    new_ona = soup.find('div', class_='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-5 clearfix')\
        .find_all('div', class_='seasonal-anime js-seasonal-anime')
    new_ova = soup.find('div', class_='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-2 clearfix')\
        .find_all('div', class_='seasonal-anime js-seasonal-anime')
    new_movie = soup.find('div', class_='seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-3 clearfix')\
        .find_all('div', class_='seasonal-anime js-seasonal-anime')

    # Список с информацией об аниме
    new_anime = []
    # Добавляется информация о новых аниме сериалах
    new_anime.extend(process_tag_array(new_tv))
    # Добавляется информация о новых ONA
    new_anime.extend(process_tag_array(new_ona))
    # Добавляется информация о новых OVA
    new_anime.extend(process_tag_array(new_ova))
    # Добавляется информация о новых аниме фильмах
    new_anime.extend(process_tag_array(new_movie))
    # Список с аниме рандомно сортируется 
    random.shuffle(new_anime)

    # Из списка выбирается десять первых аниме
    random_new_anime = new_anime[:10]

    response_text = ''
    
    for i in range(0,10):
        title = random_new_anime[i]['title']
        link = random_new_anime[i]['link']
        genre = random_new_anime[i]['genre']
        score = random_new_anime[i]['score']

        htext =  hlink(title, link)
        response_text += '{}) '.format(i+1) + htext + '\nGenre: {}'.format(genre) + '\nScore: {}\n'.format(score)

    return response_text
    

# Возвращает список со словарями, в которых содержится информация об аниме (название, ссылка на страницу 
# на сайте MAL, жанр, пользовательская оценка)
def process_tag_array(tag_array):
    new_anime_array = []

    for element in tag_array:
        anime_title = element.find('a', class_='link-title').text
        anime_link = element.find('a', class_='link-title').get('href')
        anime_genre = get_anime_genre(element.find('div', class_='genres-inner js-genre-inner').find_all('span', class_='genre'))
        anime_score = element.find('span', title = 'Score').text.strip()

        new_anime_array.append({
            'title': anime_title,
            'link': anime_link,
            'genre': anime_genre,
            'score': anime_score
        })
    
    return new_anime_array


# Возвращает текстовую переменную, в которой перечислены жанры аниме
def get_anime_genre(genre_tag_array):
    genres = ''

    for genre in genre_tag_array:
        genres += genre.find('a').text + ', '

    if genres:
        return genres[:-2]
    else:
        return 'Unknown'


# В зависимости от вида запроса определяет, какую функцию парсинга следует вызвать
def process_query(q_type, url):
    html =  get_html(url)
    if html:
        if q_type == 1:
            return get_top(html)
        elif q_type == 2:
            return get_seasonal_anime(html)
    else:
        return None
 

# Возвращает текст ответа в зависимости от вида запроса
def get_response(item):
    q_type = 1

    if item == 1:
        url = 'https://myanimelist.net/topanime.php?type=tv'
        response_text = 'Top 10 anime TV series:\n\n'
    elif item == 2:
        url = 'https://myanimelist.net/topanime.php?type=movie'
        response_text = 'Top 10 anime movies:\n\n'
    elif item == 3:
        url = 'https://myanimelist.net/topanime.php?type=ova'
        response_text = "Top 10 OVA's:\n\n"
    elif item == 4:
        url = 'https://myanimelist.net/topanime.php?type=ona'
        response_text = "Top 10 ONA's:\n\n"
    elif item == 5:
        url = 'https://myanimelist.net/anime/season'
        response_text = "List of 10 random seasonal anime:\n\n"
        q_type = 2
    
    response = process_query(q_type, url)
    
    if response:
        return response_text + response
    else:
        return 'The request cannot be processed at the moment.'
