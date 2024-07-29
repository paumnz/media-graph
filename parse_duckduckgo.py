import argparse
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains.ActionChains

class JournalistScraper:
    def __init__(self, driver_path, input_file, output_file):
        self.driver_path = driver_path
        self.input_file = input_file
        self.output_file = output_file
        self.journalists_dict = {}

    def load_journalists(self):
        with open(self.input_file, "r") as file:
            file_content = file.read()
        self.journalists = file_content.split("\n")

    def setup_driver(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.maximize_window()
        self.action_chains = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 25)

    def search_journalist(self, journalist):
        self.driver.get("http://duckduckgo.com")
        self.driver.implicitly_wait(2)
        input_element = self.driver.find_element(By.ID, 'search_form_input_homepage')
        input_element.send_keys(journalist)
        input_element.submit()
        time.sleep(1)

    def click_more_results(self):
        try:
            more_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="result result--more"]')))
            more_button.click()
            time.sleep(2)
            more_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="result result--more"]')))
            more_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking more results: {e}")

    def extract_results(self):
        RESULTS_LOCATOR = '//span[@class="result__url__domain"]'
        results = self.driver.find_elements(By.XPATH, RESULTS_LOCATOR)
        return [result.text for result in results]

    def save_results(self):
        with open(self.output_file, 'w') as fp:
            json.dump(self.journalists_dict, fp)

    def run(self):
        self.load_journalists()
        for journalist in self.journalists:
            self.setup_driver()
            try:
                self.search_journalist(journalist)
                self.click_more_results()
                self.journalists_dict[journalist] = self.extract_results()
                print(f"Results for {journalist}: {self.journalists_dict[journalist]}")
            except Exception as e:
                print(f"Error processing {journalist}: {e}")
                self.save_results()
            finally:
                self.driver.quit()
        self.save_results()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape journalist URLs from DuckDuckGo")
    parser.add_argument('--driver_path', type=str, default='/home/lab/chromedriver', help='Path to the chromedriver executable')
    parser.add_argument('--input_file', type=str, default='XXXX.csv', help='Path to the input CSV file')
    parser.add_argument('--output_file', type=str, default='journalist_graph.json', help='Path to the output JSON file')

    args = parser.parse_args()

    scraper = JournalistScraper(args.driver_path, args.input_file, args.output_file)
    scraper.run()

