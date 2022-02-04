import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import yaml


def parse_input_excel(file_path):
    df = pd.read_excel(file_path, header=None)

    # the results are ordered by
    # industry - company
    results = dict()

    for idx, row in df.iterrows():
        stock_id = row[0].split('.')[0]
        company_name = row[1]
        industry = row[2]

        if industry not in results:
            results[industry] = dict()

        results[industry][stock_id] = company_name

    return results


def create_folder(path):
    os.makedirs(path, exist_ok=True)

def get_driver():
    #Install Driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config