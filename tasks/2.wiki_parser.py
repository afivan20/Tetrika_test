from urllib.parse import urlparse

import requests
from lxml import etree

letters = 'АБВГДЕЁЖЗИӢКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
ANIMALS_ALPHABET = dict(zip(letters, [0 for n in range(1, 34)]))
url = 'https://inlnk.ru/jElywR'
headers = {'Content-Type': 'text/html'}
response = requests.get(url, headers=headers)
domain_name = urlparse(response.url).netloc

html = response.text
with open('wiki_html', 'w') as f:
    f.write(html)
r = open('wiki_html')
htmlparser = etree.HTMLParser()
tree = etree.parse(r, htmlparser)
href = tree.xpath('//a[contains(text(), "Следующая")]/@href')[1]
next_page = f'http://{domain_name}{href}'

names = tree.xpath('//div[contains(@class, "mw-category mw-category-columns")]//text()')
for name in names:
    if name[0] in ANIMALS_ALPHABET:
        ANIMALS_ALPHABET[name[0]] += 1


def parse(link):
    response = requests.get(link, headers=headers)
    html = response.text
    with open('wiki_html', 'w') as f:
        f.write(html)
    r = open('wiki_html')
    htmlparser = etree.HTMLParser()
    tree = etree.parse(r, htmlparser)
    names = tree.xpath('//div[contains(@class, "mw-category mw-category-columns")]//text()')
    for name in names:
        if name[0] in ANIMALS_ALPHABET:
            ANIMALS_ALPHABET[name[0]] += 1
        if name[0] == 'A':  # latin 'A'
            return
    try:
        href = tree.xpath('//a[contains(text(), "Следующая")]/@href')[1]
        next_page = f'http://{domain_name}{href}'
        parse(next_page)
    except Exception:
        return


if __name__ == '__main__':
    print('Идет парсинг Wiki. Процесс займет около 1 минуты. Пожалуйста подождите...')
    parse(next_page)
    print('\nКоличество животных на каждую букву алфавита:')
    for letter in ANIMALS_ALPHABET:
        print(f'{letter}: {ANIMALS_ALPHABET[letter]}')
