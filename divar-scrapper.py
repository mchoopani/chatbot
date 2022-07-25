from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    base_url = 'https://divar.ir'
    page = requests.get(base_url + '/s/tehran').text
    soup = BeautifulSoup(page, 'html.parser')
    all_endpoints = []
    sections = {}
    for tag in soup.find('div', {'class': 'filter-box'}).find('section').find('ul').find_all('li'):
        endpoint = tag.find('a')['href']
        section_name = tag.contents[0].contents[1]
        sub_page = requests.get(base_url + endpoint).text
        soup = BeautifulSoup(sub_page, 'html.parser')
        first_12_articles = soup.find_all('div', {'class': 'post-card-item kt-col-6 kt-col-xxl-4'})[:12]
        for article in first_12_articles:
            sections[section_name] = sections.get(section_name, []) + [
                str(article.find('h2', {'class': 'kt-post-card__title'}).contents[0])]
    print(sections)
