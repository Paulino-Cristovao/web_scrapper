
# webscraper 
# Scraper for glassdoor
# Code base: https://github.com/arapfaik/scraping-glassdoor-selenium/blob/master/glassdoor%20scraping.ipynb
# Adapated for France Glassdor

import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import pandas as pd
import time

#print(selenium.__version__)

def get_jobs(keyword, num_pages, path):
    options = Options()
    options.add_argument("window-size=1920,1080")
    #Enter your chromedriver.exe path below
    driver = webdriver.Chrome(executable_path=path, options=options)
    #url = "https://www.glassdoor.com/Job/france-data-scientist-jobs-SRCH_IL.0,6_IN86_KO7,21.htm"
    #url="https://www.glassdoor.com/member/home/index.htm"
    url = "https://www.glassdoor.com/Job/france-data-scientist-jobs-SRCH_IL.0,6_IN86_KO7,21.htm"
    driver.get(url)
    #search_input = driver.find_element(By.ID,"sc.keyword")
    #search_input.send_keys(keyword)
    #search_input.send_keys(Keys.ENTER)
    time.sleep(2)
    
    
   
    
    #Set current page to 1
    current_page = 1   
    time.sleep(3)


    company_name = []
    job_title = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_revenue = []
    rating = []
    company_founded = []
    
    while current_page <= num_pages:   

        #jobs = []
        
        done = False
        while not done:
            job_cards = driver.find_elements(By.XPATH,"//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            #job_cards = driver.find_elements(By.CLASS_NAME,"react-job-listing")
            #wait = WebDriverWait(driver, 10)
            for card in job_cards:
                card.click()
                time.sleep(1)

                #Closes the signup prompt
                try:
                    driver.find_element(By.XPATH,".//span[@class='SVGInline modal_closeIcon']").click()
                    time.sleep(2)
                except NoSuchElementException:
                    time.sleep(2)
                    pass
                
                
                #Expands the Description section by clicking on Show More
                try:
                    driver.find_element(By.XPATH,"//div[@class='css-jrwyhi e856ufb5']").click()
                    time.sleep(1)
                except NoSuchElementException:
                    card.click()
                    print(str(current_page) + '#ERROR: no such element')
                    time.sleep(30)
                    driver.find_element(By.XPATH,"//div[@class='css-jrwyhi e856ufb5]").click()
                except ElementNotInteractableException:
                    card.click()
                    driver.implicitly_wait(30)
                    print(str(current_page) + '#ERROR: not interactable')
                    driver.find_element(By.XPATH,"//div[@class='css-jrwyhi e856ufb5']").click()
                
                #Scrape 
                try:
                    company_name.append(driver.find_element(By.XPATH,"//div[@class='css-87uc0g e1tk4kwz1']").text)
                except NoSuchElementException:
                    company_name.append(-1)
                try:
                    job_title.append(driver.find_element(By.XPATH,"//div[@class='css-1vg6q84 e1tk4kwz4']").text)
                except NoSuchElementException:
                    job_title.append(-1)
                try:
                    location.append(driver.find_element(By.XPATH,"//div[@class='css-56kyx5 e1tk4kwz5']").text)
                except NoSuchElementException:
                    location.append(-1)
                try:
                    job_description.append(driver.find_element(By.XPATH,"//div[@class='jobDescriptionContent desc']").text)
                except NoSuchElementException:
                    job_description.append(-1)
                try:
                    salary_estimate.append(driver.find_element(By.XPATH,"//span[@class='css-1xe2xww e1wijj242']").text)
                except NoSuchElementException:
                    salary_estimate.append(-1)
                try:
                    company_size.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text) #css-1taruhi e1pvx6aw1
                except NoSuchElementException:
                    company_size.append(-1)
                try:
                    company_type.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except NoSuchElementException:
                    company_type.append(-1) 
                try:
                    company_sector.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except NoSuchElementException:
                    company_sector.append(-1)  
                try:
                    company_industry.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except NoSuchElementException:
                    company_industry.append(-1) 
                try:
                    company_founded.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except NoSuchElementException:
                    company_founded.append(-1)
                try:
                    company_revenue.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except NoSuchElementException:
                    company_revenue.append(-1)
                try:
                    rating.append(driver.find_element(By.XPATH,'.//span[@class="css-1m5m32b e1tk4kwz2"]').text)
                except NoSuchElementException:
                    rating.append(-1) #You need to set a "not found value. It's important."  

                done = True

                """
                jobs.append({'company': company_name, 
                'job title': job_title,
                'location': location,
                'job description': job_description,
                'salary estimate': salary_estimate,
                'company_size': company_size,
                'company_type': company_type,
                'company_sector': company_sector,
                'company_industry' : company_industry, 
                'company_founded' : company_founded, 
                'company_revenue': company_revenue,
                'rating':rating,
                })
                """
                
       # Moves to the next page         
        if done:
            print(str(current_page) + ' ' + 'out of' +' '+ str(num_pages) + ' ' + 'pages done')
            driver.find_element(By.XPATH,"//span[@alt='next-icon']").click()   
            current_page = current_page + 1
            time.sleep(4)
            

    driver.close()

    df = pd.DataFrame({
    'company': company_name, 
    'job title': job_title,
    'location': location,
    'job description': job_description,
    'salary estimate': salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry, 
    'company_founded' : company_founded, 
    'company_revenue': company_revenue,
    'rating':rating,
    })
    
    #df.to_csv(keyword + '.csv')
    #df = pd.DataFrame(jobs)

    return df


# path 
path = '/Users/linoospaulinos/Paris/Data_science/chromedriver'

#This line will open a new chrome window and start the scraping.
df = get_jobs("Data Scientist",20,path)
print(df.head())
print(df.tail())
df.to_csv('data.csv')
    