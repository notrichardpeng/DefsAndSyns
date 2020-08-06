import requests
import time
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver

driver = None

def definition(w, max_type_count, max_def_count):
    ret = []
    raw = requests.get('https://www.dictionary.com/browse/' + w).content
    soup = BeautifulSoup(raw, 'lxml')
    target_div = soup.find('div', {'class': 'css-1urpfgu e16867sm0'})

    if not target_div:
        ret.append('no results found for ' + w)
        return ret

    all_types = target_div.find_all('span', {'class': 'luna-pos'})
    all_contents = target_div.find_all('div', {'class': 'css-1o58fj8 e1hk9ate4'})

    if not all_types:
        ret.append('no results found for ' + w)
        return ret

    n = min(max_type_count, len(all_types))
    for t in range(n):
        type = all_types[t].text if all_types[t].text[-1] != ',' else all_types[t].text[:-1]
        content = all_contents[t]
        defs = content.find_all('div', value=True)

        ret.append(type)
        for d in range(min(max_def_count, len(defs))):
            spans = defs[d].find_all('span', {'class' : 'one-click-content css-1p89gle e1q3nk1v4'})
            this_span = ''
            for s in spans:
                this_span += s.text + ' '
            ret.append(str(d + 1) + '. '+ this_span)

        if t < n-1:
            ret.append('')

    return ret

def synonym(w, max_syn_count):
    ret = []
    driver.get('https://www.thesaurus.com/browse/' + w)
    next_button = None

    #Closes ad pop ups
    try:
        close_ad = driver.find_element_by_css_selector("button[aria-label='Dismiss Banner']")
        close_ad.click()
    except Exception:
        pass

    try:
        next_button = driver.find_element_by_css_selector("button[href='#']")
    except Exception:
        pass

    if next_button:
        counter = 1
        while next_button:
            soup = BeautifulSoup(driver.page_source, 'lxml')            
            current_active = soup.find('li', {'class':'active-postab css-auzxq6-PosTab ew5makj0'})            

            curr_res = str(counter) + '. ['+ current_active.find('em').text + '] ' + current_active.find('strong').text + ': '
            list_of_syn = soup.find('ul', {'class':'css-17d6qyx-WordGridLayoutBox et6tpn80'}).find_all('li')

            n = min(max_syn_count, len(list_of_syn))
            for i in range(n):
                if i < n-1: curr_res += list_of_syn[i].find('a').text + " | "
                else: curr_res += list_of_syn[i].find('a').text

            counter += 1
            ret.append(curr_res + '\n')

            try:
                next_button.click()
            except Exception:
                break
    else:
        try:
            variations = driver.find_element_by_css_selector("ul[class='css-z1dbbs-TabList e9i53te2']")
            variations = variations.find_elements_by_tag_name('li')
        except Exception:
            ret.append('there are no synonyms for this word')
            ret.append('')
            return ret

        counter = 1
        for v in variations:
            reason = v.find_element_by_tag_name('em').text
            meaning = v.find_element_by_tag_name('strong').text
            v.click()

            list_of_syn = driver.find_element_by_css_selector("ul[class='css-17d6qyx-WordGridLayoutBox et6tpn80']")
            list_of_syn = list_of_syn.find_elements_by_tag_name('li')

            curr_res = str(counter) + '. [' + reason + '] ' + meaning + ': '
            n = min(max_syn_count, len(list_of_syn))
            for i in range(n):
                if i < n-1: curr_res += list_of_syn[i].find_element_by_tag_name('a').text + ' | '
                else: curr_res += list_of_syn[i].find_element_by_tag_name('a').text
            counter += 1
            ret.append(curr_res + '\n')

    return ret

def initialize():
    driver_opt = webdriver.ChromeOptions()
    driver_opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_opt.add_argument('--headless')
    driver_opt.add_argument("--proxy-server='direct://'")
    driver_opt.add_argument("--proxy-bypass-list=*")
    driver_opt.add_argument('--no-proxy-server')

    try:
        global driver
        driver = webdriver.Chrome(os.path.dirname(__file__) + '\\chromedriver.exe', options=driver_opt)
    except Exception:
        print('Cannot locate chromedriver.exe in the directory of this file')
        sys.exit(0)

def quit_browser():
    global driver
    driver.quit()