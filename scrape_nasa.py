from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import requests
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    # Making space soup
    browser = init_browser()
    url = 'https://www.nasa.gov/missions/'
    html = browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Stiring the soup
    links = [a for a in soup.find('div', class_="static-landing-page").find_all('a', href = True)]
  
    # Pouring out the list and title
    link_list = []
    title_list = []
    for i in range(len(links)):
        if links[i].get('href').find("mission_pages") == 1:
            link_list.append(links[i]['href'])
            title_list.append(links[i].text)
        else:
                print('No Mission Page')
    mission_dict = {}
    mission_dict["Mission"] = title_list
    mission_dict["Mission Link"] = link_list             

    url = 'https://www.cdscc.nasa.gov/Pages/trackingtoday.html'
    html = browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')       
    abv_table = pd.read_html(url)[3] 

    abv_table.columns = ['ABV', 'Name']         
    abv_dict = abv_table.to_dict("records")

    
    MADRID = {}
    GOLDSTONE = {}
    CANBERRA = {}
    browser.visit('https://eyes.jpl.nasa.gov/dsn/dsn.html')
    time.sleep(.3)
    for i in browser.find_by_tag('a'):
        if i['class']=='inactive' or None:
            pass
        elif i.text == '':
            pass
        elif i['id'] == '' or None:
            pass                
        else:
            if i['id'][:2] == 'sp':
                ABV = i.text
                if i['id'][-5] == '0':
                    MADRID[ABV] = {}
                elif i['id'][-5] == '1':
                    GOLDSTONE[ABV] = {}  
                elif i['id'][-5] == '2':
                    CANBERRA[ABV] = {}
    
    # Platting the soup            
    mission_data = {
        "Madrid" : MADRID,
        "Goldstone": GOLDSTONE,
        "Canberra": CANBERRA,
        "Mission_titles" : mission_dict,
        "Mission_Code" : abv_dict
        } 
    browser.quit()           
    return mission_data
