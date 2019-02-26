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

    url = 'https://www.cdscc.nasa.gov/Pages/trackingtoday.html'
    html = browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')       
    tables = pd.read_html(url) 
    abv_tables = pd.DataFrame(tables[3])
    abv_tables.columns = ['ABV', 'Name']         
    # Platting the soup            
    mission_data = {
        "links" : link_list,
        "titles" : title_list,
        "ABV" : abv_tables['ABV'],
        "Name" : abv_tables['Name']
        }        
    return print(mission_data)
