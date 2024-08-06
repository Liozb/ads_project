import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



if __name__=='__main__':
    # url_inss = f'https://www.inss.org.il/he/publication/war-data/'
    url_inss = f'https://e.infogram.com/59405860-724c-4860-af6d-b265a61f42ea?src=embed'

    chrome_driver_path = f'C:/Users/user/OneDrive - Bar-Ilan University/chromedriver-win64/chromedriver.exe'
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for no GUI
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url_inss)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@data-text='true']")))
    except Exception as e:
        print(f"Error waiting for the page to load: {e}")
        driver.quit()
        exit()

    html_content = driver.page_source

    driver.quit()
    
    # with open('output.html', 'w', encoding='utf-8') as file:
    #    file.write(html_content)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the span containing the date text
    date_span = soup.find_all('span', {'data-text': 'true'})


    if date_span:
        # Extract the text from the span
        date_text = date_span[1].text
        date_text = date_text[-17:]
        # Extract the dates from the text
        last_date = date_text.split('-')[0]
        print(f"Extracted dates: {last_date}")
        
    # Get DF
    attacks_israel = {}
    attacks_hesbolla = {}
    data = html_content.split('<script>')[1]
    attacks_data = data.split('"data":[[[')[2:]
    # data_dic["attacks_israel"] = attcks_data[0]
    # data_dic["attacks_hesbolla"] = attcks_data[1]
    for idx, dataset in enumerate(attacks_data):
        data = dataset.split('"value":"')
        desc = []
        locs = []
        for val in data:
            if val[:2] == "On" or val[:12]=='Interception' or val[:7] == "Defusal" or val[:5] == "Other":
                desc.append(val.replace)
                location = data[data.index(val)-1].replace('"},null,{','')
                locs.append(location)
        if idx == 0:
            attacks_israel["description"] = desc
            attacks_israel["location"] = locs
        else:
            attacks_hesbolla["description"] = desc
            attacks_hesbolla["location"] = locs
            
    print(len(attacks_israel["location"]),len(attacks_israel["description"]) )
    print(len(attacks_hesbolla["location"]),len(attacks_hesbolla["description"]) )
    
