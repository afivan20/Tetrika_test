from urllib.parse import urlparse

import requests
from lxml import html

LETTERS = 'АБВГДЕЁЖЗИӢКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
ANIMALS_ALPHABET = dict(zip(LETTERS, [0 for n in range(1, 34)]))

def parse(link):
    response = requests.get(link)
    text = response.text
    tree = html.document_fromstring(text)

    names = tree.xpath('//div[contains(@class, "mw-category mw-category-columns")]//text()')
    for name in names:
        if name[0] in ANIMALS_ALPHABET:
            ANIMALS_ALPHABET[name[0]] += 1
        if name[0] == 'A':  # latin 'A'
            return

    try:
        href = tree.xpath('//a[contains(text(), "Следующая")]/@href')[1]
        domain_name = urlparse(response.url).netloc
        next_page = f'http://{domain_name}{href}'
        parse(next_page)
    except Exception:
        return


if __name__ == '__main__':
    print('\nИдет парсинг Wiki, мы собираем десятки тысяч названий животных.\nПроцесс займет не более 1 минуты. Пожалуйста подождите...')
    url = 'https://inlnk.ru/jElywR'
    parse(url)
    print('\nКоличество животных на каждую букву алфавита:')
    for letter in ANIMALS_ALPHABET:
        print(f'{letter}: {ANIMALS_ALPHABET[letter]}')
