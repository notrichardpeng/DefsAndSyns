import requests
from bs4 import BeautifulSoup

def Definition(word):
    raw = requests.get('https://www.dictionary.com/browse/' + word).content
    soup = BeautifulSoup(raw, 'lxml')
    targetDiv = soup.find('div', {'class': 'css-1urpfgu e16867sm0'})

    allTypes = targetDiv.find_all('span', {'class': 'luna-pos'})
    allContents = targetDiv.find_all('div', {'class': 'css-1o58fj8 e1hk9ate4'})

    for t in range(min(2, len(allTypes))):
        type = allTypes[t].text if allTypes[t].text[-1] != ',' else allTypes[t].text[:-1]
        content = allContents[t]
        defs = content.find_all('div', value=True)

        print(type)
        for n in range(min(2, len(defs))):
            print(str(n + 1) + '. ' + defs[n].find('span').text)
        print()

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
        Definition(word)
    elif command == 'syn':
        raw = requests.get('https://www.thesaurus.com/browse/' + word).content
        soup = BeautifulSoup(raw, 'lxml')
    else:
        print('invalid syntax')