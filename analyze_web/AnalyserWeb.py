import requests
from bs4 import BeautifulSoup
import argparse

def fetch_page_content(url):
    """
    Получает HTML-контент веб-страницы по её URL.
    
    :param url: URL веб-страницы для анализа.
    :return: HTML-контент страницы в виде строки.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяет, успешен ли запрос
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении страницы: {e}")
        return None

def parse_page_content(html_content):
    """
    Анализирует HTML-контент веб-страницы и возвращает объект BeautifulSoup.
    
    :param html_content: HTML-контент страницы.
    :return: Объект BeautifulSoup для навигации по HTML-документу.
    """
    if html_content:
        return BeautifulSoup(html_content, 'html.parser')
    return None

def extract_title(soup):
    """
    Извлекает заголовок страницы.
    
    :param soup: Объект BeautifulSoup, представляющий HTML-документ.
    :return: Заголовок страницы или "Нет заголовка", если он отсутствует или пустой.
    """
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Нет заголовка"

def extract_links(soup):
    """
    Извлекает все ссылки (теги <a>) из страницы.
    
    :param soup: Объект BeautifulSoup, представляющий HTML-документ.
    :return: Список словарей с текстом и URL ссылок.
    """
    links = []
    for link in soup.find_all('a', href=True):
        links.append({
            'text': link.text.strip(),
            'href': link['href']
        })
    return links

def extract_paragraphs(soup):
    """
    Извлекает все параграфы (теги <p>) из страницы.
    
    :param soup: Объект BeautifulSoup, представляющий HTML-документ.
    :return: Список текстов параграфов.
    """
    paragraphs = [p.text.strip() for p in soup.find_all('p')]
    return paragraphs

def extract_images(soup):
    """
    Извлекает все изображения (теги <img>) из страницы.
    
    :param soup: Объект BeautifulSoup, представляющий HTML-документ.
    :return: Список словарей с источником и текстом alt изображений.
    """
    images = []
    for img in soup.find_all('img'):
        images.append({
            'src': img.get('src', ''),
            'alt': img.get('alt', '')
        })
    return images

def extract_common_elements(soup):
    """
    Извлекает все общие элементы (заголовок, ссылки, параграфы, изображения) из страницы.
    
    :param soup: Объект BeautifulSoup, представляющий HTML-документ.
    :return: Словарь с извлечёнными элементами.
    """
    return {
        'title': extract_title(soup),
        'links': extract_links(soup),
        'paragraphs': extract_paragraphs(soup),
        'images': extract_images(soup)
    }

def analyze_web_page(url):
    """
    Анализирует веб-страницу и возвращает извлечённые элементы.
    
    :param url: URL веб-страницы для анализа.
    :return: Словарь с извлечёнными элементами.
    """
    html_content = fetch_page_content(url)
    soup = parse_page_content(html_content)
    return extract_common_elements(soup)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Анализ веб-страницы по указанному URL.')
    parser.add_argument('url', type=str, help='URL веб-страницы для анализа')

    args = parser.parse_args()
    
    url = args.url
    result = analyze_web_page(url)
    
    print(f"Заголовок страницы: {result['title']}\n")
    
    print("Найденные ссылки:")
    for link in result['links']:
        print(f"- {link['text']} : {link['href']}")
    
    print("\nНайденные параграфы:")
    for paragraph in result['paragraphs']:
        print(f"- {paragraph}")
    
    print("\nНайденные изображения:")
    for img in result['images']:
        print(f"- Источник: {img['src']}, Alt: {img['alt']}")