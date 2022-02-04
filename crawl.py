from actions import crawl_docs
import time
import utils


def main():
    driver = utils.get_driver()
    config = utils.load_config('./config.yml')
    data = utils.parse_input_excel(config['excel_file'])

    # wait for the page to load
    driver.get(config['url'])
    time.sleep(10)

    utils.create_folder(config['output_path'])
    stats_report = open(f"{config['output_path']}/overall_stats.txt", 'w')
    failure_report = open(f"{config['output_path']}/failure.txt", 'w')

    # crawl download links
    for industry, company_info in data.items():
        for stock_id, company_name in company_info.items():
            company_folder = f"{config['output_path']}/{industry}/{company_name}-{stock_id}"
            utils.create_folder(company_folder)

            # decide path to store the pdf links
            link_file = f'{company_folder}/download_links.txt'
            results = crawl_docs(driver, config, stock_id)

            # store links into file
            with open(link_file, 'w') as f:
                for title, url in results.items():
                    f.write(f'{title}\t{url}\n')

            stats_report.write(f"{company_name}\t{stock_id}\t{len(results)}\n")
        
    driver.close()
    stats_report.close()
    failure_report.close()
            

if __name__ == '__main__':
    main()