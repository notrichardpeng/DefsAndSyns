import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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



def Synonym(word, maxSynCount):
    driverOpt = webdriver.ChromeOptions()
    driverOpt.add_experimental_option('excludeSwitches', ['enable-logging'])
    driverOpt.add_argument('--headless')
    driverOpt.add_argument("--proxy-server='direct://'")
    driverOpt.add_argument("--proxy-bypass-list=*")

    driverPath = 'C:\\Users\\notri\\Downloads\\chromedriver.exe'
    try:
        driver = webdriver.Chrome(os.path.dirname(__file__) + '\\chromedriver.exe', options=driverOpt)
    except:
        try:
            driver = webdriver.Chrome(driverPath, options=driverOpt)
        except:
            print('Cannot locate chromdriver.exe')
            return

    driver.get('https://www.thesaurus.com/browse/' + word)
    nextButton = None

    try:
        nextButton = driver.find_element_by_css_selector("button[href='#']")
    except:
        pass

    if(nextButton):
        counter = 1
        while(nextButton):
            soup = BeautifulSoup(driver.page_source, 'lxml')

            currentActive = soup.find('li', {'class':'active-postab css-auzxq6-PosTab e9i53te0'})
            print(str(counter) + '. ['+ currentActive.find('em').text + '] ' + currentActive.find('strong').text, end=':')
            listOfSyn = soup.find('ul', {'class':'css-17d6qyx-WordGridLayoutBox et6tpn80'}).find_all('li')

            for i in range(min(maxSynCount, len(listOfSyn))):
                print(' ' + listOfSyn[i].find('a').text, end="")
            print('\n')

            counter += 1
            try:
                nextButton.click()
            except:
                break
    else:
        variations = None
        try:
            variations = driver.find_element_by_css_selector("ul[class='css-z1dbbs-TabList e9i53te2']")
            variations = variations.find_elements_by_tag_name('li')
        except:
            print('There are no synonyms for this word')
            print('\n')
            return

        counter = 1
        for v in variations:
            reason = v.find_element_by_tag_name('em').text
            meaning = v.find_element_by_tag_name('strong').text
            v.click()

            listOfSyn = driver.find_element_by_css_selector("ul[class='css-17d6qyx-WordGridLayoutBox et6tpn80']")
            listOfSyn = listOfSyn.find_elements_by_tag_name('li')

            print(str(counter) + '. [' + reason + '] ' + meaning, end=':')
            for i in range(min(maxSynCount, len(listOfSyn))):
                print(' ' + listOfSyn[i].find_element_by_tag_name('a').text, end='')
            counter += 1

        print('\n')




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
        Synonym(word, 2)
    else:
        print('invalid syntax')