from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


def enter_stock_name(driver: Chrome, stock_id):
    # find the input box and enter the stock name
    input_box = driver.find_element(By.ID, 'input_code')
    input_box.send_keys(stock_id)
    time.sleep(2)

    dropdown_menu = driver.find_element(By.ID, 'c-typeahead-menu-1')
    dropdown_button = dropdown_menu.find_element(By.TAG_NAME, 'a')
    dropdown_button.click()
    input_box.send_keys(Keys.ENTER)
    time.sleep(2)

def choose_annual_report(driver: Chrome, report_ordinal):
    report_type_button = driver.find_elements(By.CLASS_NAME, 'c-selectex-btn-text')[2]
    report_type_button.click()

    report_type_list = driver.find_element(By.ID, 'c-selectex-menus-3')
    report_type_button = report_type_list.find_elements(By.TAG_NAME, 'a')[report_ordinal]
    report_type_button.click()
    time.sleep(2)

def get_pagniator(driver: Chrome):
    pagniators = driver.find_elements(By.ID, 'paginator')
    if len(pagniators) == 1:
        return pagniators[0]
    else:
        return None

def go_to_next_page(driver: Chrome):
    paginator = get_pagniator(driver)
    if paginator:
        button_list = paginator.find_elements(By.TAG_NAME, 'li')

        for i in range(len(button_list)):
            button = button_list[i]
            classes = button.get_attribute('class')
            if 'active' in classes:
                if i == len(button_list) - 1:
                    return False
                else:
                    page_link = button_list[i+1].find_element(By.TAG_NAME, 'a')
                    page_link.click()
                    time.sleep(2)
                    return True
            return False
    else:
        return False


def get_doc_title_and_path(driver: Chrome, start_year, end_year):
    table_column = driver.find_elements(By.CLASS_NAME, 'annon-title-link')
    report_time = driver.find_elements(By.CLASS_NAME, 'text-time')

    results = dict()
    unwanted_doc_appear = False

    for doc, _time in zip(table_column, report_time):
        file_path = doc.get_attribute('attachpath')
        title = doc.text.split('\n')[0]
        year = int(_time.text.split('-')[0])

        if year >= start_year and year <= end_year:
            results[title] = file_path
        else:
            unwanted_doc_appear = True
    
    return results, unwanted_doc_appear

def clear_all_filters(driver: Chrome):
    clear_all_button = driver.find_element(By.CLASS_NAME, 'btn-clearall')
    clear_all_button.click()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-clearall"))).click()
    time.sleep(2)


def crawl_docs(driver: Chrome, config, stock_id):
    enter_stock_name(driver, stock_id)
    choose_annual_report(driver, config['report_ordinal'])
    collated_results = dict()
    keep_crawl = True

    while keep_crawl:
        partial_results, unwanted_doc_appear = get_doc_title_and_path(driver, config['start_year'], config['end_year'])
        keep_crawl = not unwanted_doc_appear
        collated_results.update(partial_results)

        if keep_crawl:
            success = go_to_next_page(driver)
            keep_crawl = success
    
    clear_all_filters(driver)

    return collated_results


def download_pdf(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)


