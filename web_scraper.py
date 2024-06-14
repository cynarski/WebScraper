from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import csv
class WebScraper:
    def __init__(self, url, selectors):
        self.url = url
        self.selectors = selectors
        self.driver = webdriver.Chrome(options=webdriver.ChromeOptions())

    def scrape(self):
        self.driver.get(self.url)
        elements = {key: self.driver.find_elements(By.XPATH, xpath) for key, (xpath, _) in self.selectors.items()}

        items_count = len(next(iter(elements.values())))

        products = []
        for i in range(items_count):
            product = {}
            for key, (xpath, attribute) in self.selectors.items():
                if attribute:
                    product[key] = elements[key][i].get_attribute(attribute).strip()
                else:
                    product[key] = elements[key][i].text.strip()
            products.append(product)

        return products

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":

    with open('selectors.json', 'r') as file:
        selectors = json.load(file)

    filename = 'products.csv'
    unique_products = set()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [column_name for column_name in selectors.keys()]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for i in range(1, 121):
        print(i)
        url = f"https://www.notino.pl/perfumy-mezczyzni/?f={i}-1-55544-55549"
        scraper = WebScraper(url, selectors)
        products = scraper.scrape()
        scraper.close_driver()

        for product in products:
            product_key = (product['Brand'], product['Name'], product['Price'])
            if product_key not in unique_products:
                unique_products.add(product_key)
                with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(product)

