import requests
from bs4 import BeautifulSoup

# main loop
while True:
    s = input('dict: ')
    if s == 'quit()':
        break

    parts = s.split(' ')
    if len(parts) != 2:
        print('invalid syntax\n')
        continue

    command = parts[0]
    word = parts[1]

    if command == 'def':
        raw = requests.get('https://www.dictionary.com/browse/' + word).content
        soup = BeautifulSoup(raw, 'lxml')

        wordTypeElem = soup.find_all('span', {'class':'luna-pos'})[0]
        type = wordTypeElem.text if wordTypeElem.text[-1] != ',' else wordTypeElem.text[:-1]

        contentDiv = soup.find('div', {'class':'css-1o58fj8 e1hk9ate4'})
        print(contentDiv.find('div', {'value':'1'}).find('span').text)
    elif command == 'syn':
        raw = requests.get('https://www.thesaurus.com/browse/' + word).content
        soup = BeautifulSoup(raw, 'lxml')
    else:
        print('invalid syntax')

    print()