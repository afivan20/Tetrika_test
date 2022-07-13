from urllib.parse import urlparse

import requests
from lxml import html

LETTERS = 'АБВГДЕЁЖЗИӢКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
ANIMALS_ALPHABET = dict(zip(LETTERS, [0 for n in range(1, 34)]))

def parse(link):
    try:
        response = requests.get(link)
        text = response.text
        tree = html.document_fromstring(text)
        names = tree.xpath('//div[contains(@class, "mw-category mw-category-columns")]//text()')
        
    except Exception as error:
        print(f'Упс... Что-то пошло не так: {error}')
        return
    
    if len(names) != 0:
        for name in names:
            if name[0] in ANIMALS_ALPHABET:
                ANIMALS_ALPHABET[name[0]] += 1
            if name[0] == 'A':  # latin 'A'
                return

    href = tree.xpath('//a[contains(text(), "Следующая")]/@href')
    if len(href) != 0:
        domain_name = urlparse(response.url).netloc
        next_page = f'http://{domain_name}{href[0]}'
        parse(next_page)
    return 


if __name__ == '__main__':
    print('\nЗапущен процесс парсинга Wiki, мы собираем десятки тысяч названий животных.\nПроцесс займет около 1 минуты. Пожалуйста подождите...\n')
    url = 'https://inlnk.ru/jElywR'
    parse(url)
    print('Количество животных на каждую букву алфавита:')
    for letter in ANIMALS_ALPHABET:
        print(f'{letter}: {ANIMALS_ALPHABET[letter]}')
