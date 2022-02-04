from turtle import down
from actions import download_pdf
import utils
import os


def main():
    config = utils.load_config('./config.yml')

    # download pdfs
    for industry_folder in os.listdir(config['output_path']):
        industry_folder_path = os.path.join(config['output_path'], industry_folder)
        if not os.path.isdir(industry_folder_path):
            continue
        else:
            for company_folder in os.listdir(industry_folder_path):
                company_folder_path = os.path.join(industry_folder_path, company_folder)
                if os.path.isdir(company_folder_path):
                    print(f'download PDFs into {company_folder_path}')
                    download_link_path = os.path.join(company_folder_path, 'download_links.txt')
                    with open(download_link_path, 'r') as f:
                        for line in f:
                            title, suburl = line.strip().split('\t')

                            download = True
                            for keyword in config['unwanted_keywords']:
                                if keyword in title:
                                    download = False
                                    
                            if download:                                    
                                save_path = os.path.join(company_folder_path, f'{title}.pdf')
                                download_url = f"{config['download_url_prefix']}{suburl}"
                                download_pdf(download_url, save_path)


if __name__ == '__main__':
    main()