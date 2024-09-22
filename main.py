import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
from translate import translate 


if __name__=='__main__':
    
    ##################################### Scraper for inss war data #######################################
    url_inss = f'https://e.infogram.com/59405860-724c-4860-af6d-b265a61f42ea?src=embed'

    # chrome_driver_path = f'C:/Users/user/OneDrive - Bar-Ilan University/chromedriver-win64/chromedriver.exe'
    chrome_driver_path = f'chromedriver-linux64/chromedriver'
    service = Service(chrome_driver_path)
    # options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = 'chromium/chrome-linux/chrome'
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
    
    with open('output.html', 'w', encoding='utf-8') as file:
       file.write(html_content)
    
#    # Parse the HTML content using BeautifulSoup
#    soup = BeautifulSoup(html_content, 'html.parser')
#    
#    # Find the span containing the date text
#    date_span = soup.find_all('span', {'data-text': 'true'})
#
#
#    if date_span:
#        # Extract the text from the span
#        date_text = date_span[1].text
#        date_text = date_text[-17:]
#        # Extract the dates from the text
#        last_date = date_text.split('-')[0]
#        print(f"Extracted dates: {last_date}")
#        
#    # Get DF
#    attacks_israel = {}
#    attacks_hesbolla = {}
#    data = html_content.split('<script>')[1]
#    attacks_data = data.split('"data":[[[')[2:]
#    # data_dic["attacks_israel"] = attcks_data[0]
#    # data_dic["attacks_hesbolla"] = attcks_data[1]
#    for idx, dataset in enumerate(attacks_data):
#        data = dataset.split('"value":"')
#        desc = []
#        locs = []
#        for val in data:
#            if val[:2] == "On" or val[:12]=='Interception' or val[:7] == "Defusal" or val[:5] == "Other":
#                desc.append(val.replace)
#                location = data[data.index(val)-1].replace('"},null,{','')
#                locs.append(location)
#        if idx == 0:
#            attacks_israel["description"] = desc
#            attacks_israel["location"] = locs
#        else:
#            attacks_hesbolla["description"] = desc
#            attacks_hesbolla["location"] = locs
#            
#    # print(len(attacks_israel["location"]),len(attacks_israel["description"]) )
#    # print(len(attacks_hesbolla["location"]),len(attacks_hesbolla["description"]) )
#    
#    ##################################### Scraper for IDF war-logs #######################################
#    
#    last_date = datetime.strptime(last_date, '%d/%m/%y')
#
#    # Get the current date
#    current_date = datetime.now()
#
#    war_log_data = {}
#    time_in_day = []
#    war_log_desc = []
#    war_log_date = []
#    logs_list = []
#    for i in range((current_date - last_date).days + 1):
#        full_date = (last_date + timedelta(days=i)).strftime('%d-%m-%y')
#        date = full_date[:-3]
#        # print(date)
#        idf_url = f'https://www.idf.il/%D7%90%D7%AA%D7%A8%D7%99-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94-%D7%AA%D7%9E%D7%95%D7%A0%D7%AA-%D7%94%D7%9E%D7%A6%D7%91-%D7%9C%D7%90%D7%95%D7%A8%D7%9A-%D7%94%D7%99%D7%9E%D7%99%D7%9D/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94-{date}/'
#        
#        # Send a GET request to the URL
#        driver_idf = webdriver.Chrome(service=service, options=options)
#        driver_idf.get(idf_url)
#        html_idf = driver_idf.page_source
#        soup_idf = BeautifulSoup(html_idf, 'html.parser')
#
#        page_not_found = False
#        message_tag = soup_idf.find('h3', class_='heading-default h3-heading')
#        if message_tag and 'אין מה לראות כאן' in message_tag.get_text():
#            date_obj = datetime.strptime(date, '%d-%m')
#            day = date_obj.day
#            month = date_obj.month
#            idf_url = f'https://www.idf.il/%D7%90%D7%AA%D7%A8%D7%99-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94-%D7%AA%D7%9E%D7%95%D7%A0%D7%AA-%D7%94%D7%9E%D7%A6%D7%91-%D7%9C%D7%90%D7%95%D7%A8%D7%9A-%D7%94%D7%99%D7%9E%D7%99%D7%9D/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94-{day}-%D7%91%D7%90%D7%95%D7%92%D7%95%D7%A1%D7%9{month}-2024/'
#            driver_idf = webdriver.Chrome(service=service, options=options)
#            driver_idf.get(idf_url)
#            html_idf = driver_idf.page_source
#            soup_idf = BeautifulSoup(html_idf, 'html.parser')
#        
#        
#        message_tag = soup_idf.find('h3', class_='heading-default h3-heading')
#        if message_tag and 'אין מה לראות כאן' in message_tag.get_text():
#            idf_url = f'https://www.idf.il/%D7%90%D7%AA%D7%A8%D7%99-%D7%99%D7%97%D7%99%D7%93%D7%95%D7%AA/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94-%D7%AA%D7%9E%D7%95%D7%A0%D7%AA-%D7%94%D7%9E%D7%A6%D7%91-%D7%9C%D7%90%D7%95%D7%A8%D7%9A-%D7%94%D7%99%D7%9E%D7%99%D7%9D/%D7%99%D7%95%D7%9E%D7%9F-%D7%94%D7%9E%D7%9C%D7%97%D7%9E%D7%94-%D7%9B%D7%9C-%D7%94%D7%A2%D7%93%D7%9B%D7%95%D7%A0%D7%99%D7%9D-%D7%95%D7%94%D7%AA%D7%99%D7%A2%D7%95%D7%93%D7%99%D7%9D-%D7%94%D7%90%D7%97%D7%A8%D7%95%D7%A0%D7%99%D7%9D-{date}/'
#            driver_idf = webdriver.Chrome(service=service, options=options)
#            driver_idf.get(idf_url)
#            html_idf = driver_idf.page_source
#            soup_idf = BeautifulSoup(html_idf, 'html.parser')
#            
#            
#        message_tag = soup_idf.find('h3', class_='heading-default h3-heading') 
#        if message_tag and 'אין מה לראות כאן' in message_tag.get_text():
#            logs = ["page not found"]
#            page_not_found = True
#        # Example: Extract the title of the webpage
#        # title = soup_idf.title.string
#        # print('Page Title:', title)
#        time.sleep(5)
#        # Example: Extract all links from the webpage
#        if page_not_found == False:
#            logs = soup_idf.find_all('p')
#        
#        logs_list.append(f"########################{full_date}#####################################")
#        for log in logs:
#            if type(log) is str:
#                logs_list.append(log)
#            else:
#                logs_list.append(log.get_text())
#            if page_not_found == False:
#                if '|' in log.get_text():
#                    log_split = log.get_text().split('|')
#                    #print(log_split)
#                    time_in_day.append(log_split[0])
#                    war_log_desc.append(log_split[1])
#                    war_log_date.append(date)
#                else:
#                    # print(war_log_desc)
#                    war_log_desc[-1] = war_log_desc[-1] + " " + log.get_text()
#                
#    war_log_desc = translate(war_log_desc)
#    war_log_data["time_in_day"] = time_in_day
#    war_log_data["war_log_desc"] = war_log_desc
#    war_log_data["war_log_date"] = war_log_date 
#    
#    print(len(time_in_day))
#    print(len(war_log_desc))
#    print(len(war_log_date))
#    
#    war_log_df = pd.DataFrame.from_dict(war_log_data)
#    print(war_log_df.head())
#    
#    os.remove('IDF_war_logs.txt') 
#    with open('IDF_war_logs.txt', 'a', encoding='utf-8') as file:
#            for log in logs_list:
#                file.write(log + '\n')

    