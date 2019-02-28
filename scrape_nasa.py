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
    
    # Platting the soup            
    mission_data = {
        "Mission_titles" : mission_dict,
        "Mission_Code" : abv_dict
        } 
    browser.quit()           
    return mission_data
