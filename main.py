import requests
from bs4 import BeautifulSoup as BS



char = 'а'
cities = []
for number_char in range(33):

    symbol = chr(ord(char) + number_char)
    if symbol == 'ь' or symbol == 'ъ':
        continue

    url = f'https://geodzen.com/cities/{symbol}'


    number_page = 0

    while True:
        if number_page != 0:
            url = f'https://geodzen.com/cities/{symbol}?part={number_page}'

        response = requests.get(url)
        bs = BS(response.text, 'lxml')
        active_page = bs.select_one('div.parts')
        if active_page:
            data = active_page.select_one('a.active')
            if not data:
                break
        else:
            if number_page == 1:
                break


        cities_for_this_page = bs.find_all('tr', class_='city no-top-border')

        for elem in cities_for_this_page:
            city = elem.find('a').text
            cities.append(city)
            print(city)


        number_page += 1


cities = [city + '\n' for city in cities]

with open('cities.txt', 'w', encoding='utf-8') as f:
    f.writelines(cities)


'''
with open('cities.txt', encoding='utf-8') as f:
    cities = f.readlines()

cities = [city[:-1] for city in cities]
'''



def get_city(char, cities):
    empty = True
    if char.isalpha():
        char = char.upper()
        for city in cities:
            if city.startswith(char):
                print(city)
                empty = False
                cities.remove(city)
                break

        if empty:
            print(f'Города на букву {char} закончились')


    else:
        print('Введена не буква')



while len(cities) != 0:
    char = input('Буква: ')
    get_city(char, cities)

