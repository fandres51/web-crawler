import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import re

def fetch_news_entries():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    entries = []
    articles = soup.find_all('tr', class_='athing', limit=30)

    for article in articles:
        # Extae el título
        titleline_span = article.find('span', class_='titleline')
        title_tag = titleline_span.find('a') if titleline_span else None
        title = title_tag.get_text() if title_tag else 'No Title'

        # Extrae el número de publicación
        title_id_tag = article.find('span', class_='rank')
        title_id = int(title_id_tag.get_text().replace('.', '')) if title_id_tag else 0

        # Extrae el número de puntos
        score_span = article.find_next('span', class_='score')
        score = int(score_span.get_text().replace(' points', '')) if score_span else 0
                
        # Extrae el número de comentarios
        comments_tag = article.find_next_sibling('tr').find('a', string=lambda text: 'comments' in text)
        if comments_tag:
            comments_text = comments_tag.get_text().replace('\xa0', ' ').replace(' comments', '')
            comments = int(comments_text)
        else:
            comments = 0

        entries.append({
            'number': title_id,
            'title': title,
            'points': score,
            'comments': comments
        })

    return entries

def count_words(title):
    title_clean = re.sub(r'[^\w\s]', ' ', title)
    return len(title_clean.split())

def filter_entries(entries):
    long_titles = [entry for entry in entries if count_words(entry['title']) > 5]
    short_titles = [entry for entry in entries if count_words(entry['title']) <= 5]

    long_titles_sorted = sorted(long_titles, key=lambda x: x['comments'], reverse=True)
    short_titles_sorted = sorted(short_titles, key=lambda x: x['points'], reverse=True)

    return long_titles_sorted, short_titles_sorted

def news_entries_view(request):
    entries = fetch_news_entries()
    long_titles_sorted, short_titles_sorted = filter_entries(entries)
    
    response_data = {
        'long_titles_sorted': long_titles_sorted,
        'short_titles_sorted': short_titles_sorted
    }

    return JsonResponse(response_data)
