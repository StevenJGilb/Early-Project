"""

EXTRACT H1B DATA BASED ON OCCUPATION

This program extracts a list of sponsors (employers) based on the occupations that have applied for H1B visas. 
The output will consist of a list of sponsors, the number of applicants, average salary, 
and the corresponding occupation for which the application was made. 
The resulting output will be saved as approximately 31,116 rows in a CSV file. 
This program utilizes the Selenium package for data extraction and navigation across multiple web pages.

The program performs the following steps:

1. Extracts a list of occupations from 'h1b-occupation.csv' file into a [list].
2. Clicks on occupation links in the website table, determined by the row number.
3. After clicking an occupation link, the program displays a list of sponsors who have applied for H1B visas under that specific occupation.
4. Extracts data from the sponsor table (sponsors, number of applicants, and average salary).
5. After extracting data from the sponsor table, the code navigates back to the occupation page and clicks on the next row.
6. This looping process continues until data has been extracted for every occupation and sponsor.

"""

import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException

#global
#occ_page is list of possible occupation pages to be clicked [26 - 50, 51 - 75, 76 - 100]
occ_page = 2   #adjustable. if reset, occ_page =  2

#spon_page is list of possible sponsor pages to be clicked [51 - 100, 101 - 150, 151 - 200]
spon_page = -1  #adjustable. if reset, spon_page =  -1

#number of occupation row, it determines which occupation to be extracted (max 199)
occ_row = 0   #adjustable. if reset, occ_row =  0

#implement adblocker
path = 'C:/Users/steve/Downloads/extension_5_8_1_0.crx'

#list of pages in the website. index 0 - 2 are the occupation page and index 3 - 5 are the sponsor page 
page_to_click = ['26 - 50', '51 - 75', '76-100', '51 - 100', '101 - 150', '151 - 200']

#return to this page in case of error
error_page = '1 - 25'

#the website to be extracted
service = Service()
options = webdriver.ChromeOptions()
options.add_extension(path)
url = "https://www.myvisajobs.com/Reports/2023-H1B-Visa-Category.aspx?T=OC"
page_to_scrape = webdriver.Chrome(service=service, options=options)

#to quit the loop
stay_loop = True

#function
#to navigate the occupation page
def click_page_occ():
    global occ_page, spon_page, occ_row, stay_loop, table, url
    
    #if occ_row >= 50, it will loop to click page 51 - 100
    if occ_row == 50:
        occ_page += 1
    
    #if 51 <= occ_row <= 100, it will loop to click page 101 - 150
    elif occ_row == 100:
        occ_page += 1
    #if 101 <= occ_ro <= 200, it will loop to click page 151 - 200
    elif occ_row == 150:
        occ_page += 1
    
    #click the page based on the number of occupation extracted
    click = page_to_click[occ_page]
    page_to_scrape.find_element(By.LINK_TEXT, click).click() 


def click_page_spon():
    global occ_page, spon_page, occ_row, stay_loop, table, url
    
    #b is to determine which sponsor page to click
    spon_page += 1
    
    #if b is still lower or equal than 2, it will click the page based on the index number
    if spon_page <= 2:
        click = page_to_click[spon_page]
        page_to_scrape.find_element(By.LINK_TEXT, click).click()  

def click_page_error():
    global occ_page, spon_page, occ_row, stay_loop, table, url
    #some pages have error, such as no data listed, or wrong page number. This function is to go back to page '1 - 25' in sponsor page and find the correct page
    click = error_page
    page_to_scrape.find_element(By.PARTIAL_LINK_TEXT, click).click()

def back_main_page():
    global occ_page, spon_page, occ_row, stay_loop, table, url
    #this function is to mitigate error if it encounters unexpected error
    page_to_scrape.get(url)

def extract_data():
    #the function to extract data
    global occ_page, spon_page, occ_row, stay_loop, table, url
    #table and row need to be reassigned everytime the code change page
    table1 = page_to_scrape.find_element(By.CLASS_NAME, 'tbl')
    rows1 = table1.find_elements(By.TAG_NAME, 'tr')
    #to loop and extract data from the table
    for row in rows1[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]
        #some row do not have data, if any(row data) allows the code to skip the empty row
        if any(row_data):
            #to match list of occupation from separate csv and the data table in the website
            occ = list_of_occupation[occ_row]
            #to add the occupation for every sponsor extracted
            row_data.append(occ)
            writer.writerow(row_data)
            print(row_data)

def main():
    #function to execute the main code
    global occ_page, spon_page, occ_row, stay_loop, table, url
    
    #identify the table and row
    table = page_to_scrape.find_element(By.CLASS_NAME, 'tbl')
    
    #assign occ to the occupation that we want to extract on the table based on c value
    occ = list_of_occupation[occ_row]
    
    #once assigned, it will click the occupation link, to list out all the sponsors who applied H1B for that occupation
    try:
        employer = table.find_element(By.LINK_TEXT, occ)
        employer.click()
    #in case there's an error in finding occ, it will go back to the occupation main page
    except NoSuchElementException:
        print('Error found, trying something else...')
        back_main_page()
        click_page_occ()
        table = page_to_scrape.find_element(By.CLASS_NAME, 'tbl')
        occ = list_of_occupation[occ_row]
        employer = table.find_element(By.LINK_TEXT, occ)
        employer.click()
    #loop to extract data
    while stay_loop:
        
        #element found is to identify if there's any error regarding element not found while extracting data
        element_found = False
        
        #error try is to identify if there's any element exception error while extracting data
        error_try = False
        
        #until the sponsor page reach 76 - 100, it will keep extracting data
        if spon_page <= 2:
            time.sleep(2)
            try:
                extract_data()
            except NoSuchElementException:
                print(f'Error found, trying something else...')
            
            #If there's an element exception error (no table to extract), it will try to click the next sponsor page
            try:
                click_page_spon()
                element_found = True
            except NoSuchElementException:
                print(f'Error found, trying something else...')

            #if element exception error found, it will go back to page 1- 25 in sponsor page and continue to extract data
            if element_found == False:
                try:
                    #go back to page 1 - 25
                    click_page_error()
                    spon_page -= 1
                    click_page_spon()
                
                #if the whole page is error, it will go back to main page and skip to the next occupation row
                except NoSuchElementException:
                    print(f'Error found, trying something else...')
                    error_try = True
                if error_try == True:
                    try:
                        #go back to the main page
                        back_main_page()
                        occ_row += 1
                        occ = list_of_occupation[occ_row]
                        try:
                            click_page_occ()
                        except NoSuchElementException:
                            print(f'Error found, trying something else...')
                        table = page_to_scrape.find_element(By.CLASS_NAME, 'tbl')
                        employer = table.find_element(By.PARTIAL_LINK_TEXT, occ)
                        employer.click()
                    except NoSuchElementException:
                        print(f'Error found, trying something else...')
            time.sleep(1)
        
        #if sponsor page reaches the end (page 76 - 100), it will go back to the main occupation page and click the next row and repeat the process
        elif spon_page >= 3:
            occ_row += 1
            
            #if occupation has not reach the end (there are 199 occupations)
            if occ_row < 199:
                
                #to avoid out of range page error
                spon_page = -1
                
                #click the next occupation row
                main_page = page_to_scrape.find_element(By.LINK_TEXT, "Occupation")
                main_page.click()
                if 50 <= occ_row < 199:
                    click_page_occ()
                occ = list_of_occupation[occ_row]
                time.sleep(1)
                table = page_to_scrape.find_element(By.CLASS_NAME, 'tbl')
                employer = table.find_element(By.PARTIAL_LINK_TEXT, occ)
                employer.click()
            
            #to quit if the code has clicked all rows in occupation
            elif occ_row >= 199:
                stay_loop = False
            
#main

#to store list of occupation from csv file, which is used to determine which link to click
list_of_occupation = []
with open('h1b-occupation.csv', newline='') as csv_file:
    in_list = csv.reader(csv_file)
    next(in_list, None)
    for line in in_list:
        
        #the occupation is in index 1
        occupation = line[1]
        list_of_occupation.append(occupation)

#to save the extracted data to csv file
#csv automatically add extra row for every data read. need to add newline='' to remove it
with open('h1b-occupation-employer-test.csv', 'a', encoding="utf-8", newline='') as csv_file:
    writer = csv.writer(csv_file,delimiter=',')
    writer.writerow(["RANK", "SPONSOR", "NUMBER OF LCA", "AVERAGE SALARY","OCCUPATION"])
    time.sleep(12) #took about 12 seconds to implement the adblocker
    page_to_scrape.get(url)
    table = page_to_scrape.find_element(By.CLASS_NAME, 'tbl')
    main()
    
page_to_scrape.quit