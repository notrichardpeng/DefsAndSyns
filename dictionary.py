import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver

def Definition(word, maxTypeCount, maxDefCount):
    raw = requests.get('https://www.dictionary.com/browse/' + word).content
    soup = BeautifulSoup(raw, 'lxml')
    targetDiv = soup.find('div', {'class': 'css-1urpfgu e16867sm0'})

    allTypes = targetDiv.find_all('span', {'class': 'luna-pos'})
    allContents = targetDiv.find_all('div', {'class': 'css-1o58fj8 e1hk9ate4'})

    for t in range(min(maxTypeCount, len(allTypes))):
        type = allTypes[t].text if allTypes[t].text[-1] != ',' else allTypes[t].text[:-1]
        content = allContents[t]
        defs = content.find_all('div', value=True)

        print(type)
        for n in range(min(maxDefCount, len(defs))):
            print(str(n + 1) + '. ' + defs[n].find('span').text)
        print()



def Synonym(word):
    driverOpt = webdriver.ChromeOptions()
    driverOpt.add_experimental_option('excludeSwitches', ['enable-logging'])
    driverOpt.add_argument('--headless')
    driver = webdriver.Chrome(os.path.dirname(os.path.realpath('dictionary.py')) + '\\chromedriver.exe', options=driverOpt)
    driver.get('https://www.thesaurus.com/browse/' + word)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    listOfVariations = soup.find('ul', {'class':'css-1wm7jhc e9i53te2'}).find_all('li')
    print(listOfVariations)

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
        Definition(word, 2, 2)
    elif command == 'syn':
        Synonym(word)
    else:
        print('invalid syntax')