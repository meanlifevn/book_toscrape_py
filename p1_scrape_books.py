import os
import re
import time
import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = "https://books.toscrape.com/"
BASE_URL_BOOK = "https://books.toscrape.com/catalogue/"
W_TO_D = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5}
BOOKS_ALL = []
# SCRAPING_DATE = time.strftime("%Y-%m-%d", time.localtime())
URL_SELECT = "https://books.toscrape.com/catalogue/category/books/self-help_41/index.html"
CATAGORY_NAME = "Self Help"
QTY_BOOKS = 3
BOOKS_FOLDER = "./raw_books"
HTML_BACKUP_FOLDER = "./html_backup"


def driversetup():
    options = webdriver.ChromeOptions()
    # run Selenium in headless mode
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # overcome limited resource problems
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    # open Browser in maximized mode
    options.add_argument("start-maximized")
    # disable infobars
    options.add_argument("disable-infobars")
    # disable extension
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    return driver


def pagesource(url, driver, back_up=False):
    # Create another safe_url
    safe_url = url
    # Set up driver
    driver = driver
    driver.get(safe_url)
    # Wait for the page to load (adjust as needed)
    time.sleep(3)
    # Save raw HTML for backup
    # Get the raw HTML source
    html_content = driver.page_source
    if back_up != False:
        # Define the path and filename for saving the HTML
        html_file_name = f"{url.split('/')[-2]}.html"
        html_file_path = os.path.join(HTML_BACKUP_FOLDER, html_file_name)
        # Save the HTML content to a file
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\nHTML source saved to {html_file_name}\n")
    drv_soup = soup(html_content, "html.parser")
    driver.close()
    return drv_soup


def find_categories(soup):
    # Find all the categories
    categories = soup.find('ul', {'class': 'nav nav-list'}).find('li').find('ul').find_all('li')
    return categories


def fetch_all_books(soup):
    # Fetch all the books information
    # Return books_all, a list of dictionary that contains all the extracted data
    # Find all the categories by running find_categories() function
    categories = find_categories(soup)
    # Loop through categories
    for category in categories:
        # Fetch product by category
        # Within the fetch_books_by_category function, we will scrape products page by page
        category_name = category.find('a').text.strip()
        fetch_books_by_category(category_name, category)
    return BOOKS_ALL


def fetch_books_by_category(category_name, category):
    # Fetch books by category
    # Scrape all the books listed on one page
    # Go to next page if current page is not the last page
    # Break the loop at the last page
    # Get category URL, i.e., the link to the first page of books under the category
    books_page_url = BASE_URL + category.find('a').get('href')
    # Scape books page by page only when the next page is available
    while True:
        # Create a beautiful soup object for the current page
        driver = driversetup()
        current_page_soup = pagesource(driver)
        # Run fetch_current_page_books function to get all the products listed on the current page
        fetch_current_page_books(category_name, current_page_soup)
        # Search for the next page's URL
        # Get the next page's URL if the current page is not the last page
        try:
            find_next_page_url = current_page_soup.find('li', {'class': 'next'}).find('a').get('href')
            # Find the index of the last '/'
            index = books_page_url.rfind('/')
            # Skip the string after the last '/' and add the next page url
            books_page_url = books_page_url[:index + 1].strip() + find_next_page_url
        except:
            break


def fetch_current_page_books(category_name, current_page_soup, qty_books=0):
    # Fetch all the books listed on the current page
    # Build a dictionary to store extracted data
    # Append book information to the books_all list
    # Find all products listed on the current page
    current_page_books = current_page_soup.find('ol', {'class': 'row'}).find_all('li')
    # Check amount of books is needed
    if qty_books == 0: qty_books = len(current_page_books)
    # Loop through the products
    for book in tqdm(current_page_books[:qty_books]):
        try:
            # Extract book info of interest
            # Get book title
            # Replace get('title') with text to see what will happen
            title = book.find('h3').find('a').get('title').strip()
            # Get book price
            price = book.find('p', {'class': 'price_color'}).text.strip()
            # Get in stock info
            instock = book.find('p', {'class': 'instock availability'}).text.strip()
            # Get rating
            rating_in_words = book.find('p').get('class')[1]
            rating = W_TO_D[rating_in_words]
            # Get link
            link = book.find('h3').find('a').get('href').strip()
            link = BASE_URL_BOOK + link.replace('../../../', '')
            # Get more info about a book by running fetch_more_info function
            product_info = fetch_more_info(link)
            # Create a book dictionary to store the book’s info
            book = {
                # 'scraping_date': SCRAPING_DATE,
                'book_title': title,
                # 'category': category_name,
                'price': price,
                # 'instock': instock,
                'availability': product_info['Availability'],
                # 'UPC': product_info['UPC'],
                'link': link,
                'rating': rating
            }
        except:
            continue
        time.sleep(1)
        # Append book dictionary to books_all list
        BOOKS_ALL.append(book)


def fetch_more_info(link):
    # Go to the single product page to get more info
    # Get url of the web page
    # Create a beautiful soup object for the book
    driver = driversetup()
    book_soup = pagesource(link, driver, back_up=True)
    # Find the product information table
    book_table = book_soup.find('table', {'class': 'table table-striped'}).find_all('tr')
    # Build a dictionary to store the information in the table
    product_info = {}
    # Loop through the table
    for info in book_table:
        # Use header cell as key
        key = info.find('th').text.strip()
        # Use cell as value
        value = info.find('td').text.strip()
        product_info[key] = value
    # Extract number from availability using Regular Expressions
    text = product_info['Availability']
    # reassign the number to availability
    product_info['Availability'] = re.findall(r'(\d+)', text)[0]
    return product_info


def main():
    # Create folders if it doesn't exist
    os.makedirs(BOOKS_FOLDER, exist_ok=True)
    os.makedirs(HTML_BACKUP_FOLDER, exist_ok=True)

    # # Set drive to fetch all the books
    # driver = driversetup()
    # books_soup = pagesource(BASE_URL, driver)
    # books_list = fetch_all_books(books_soup)

    # Set drive to fetch at least 3 books in the selected category.
    driver = driversetup()
    books_soup = pagesource(URL_SELECT, driver)

    print('=============== Starting crawl\n')
    fetch_current_page_books(CATAGORY_NAME, books_soup, QTY_BOOKS)
    print('\n=============== Scraping complete!')

    # Convert the list to a data frame, drop the duplicates
    books_df = pd.DataFrame(BOOKS_ALL).drop_duplicates()
    print(f'There are totally {len(books_df)} books in the {CATAGORY_NAME}.')

    # Define the path and filename for saving file
    df_name = f"{CATAGORY_NAME}_{QTY_BOOKS}_books.csv"
    df_path = os.path.join(BOOKS_FOLDER, df_name)

    # Save the output as a csv file
    books_df.to_csv(df_path, index=False, encoding='utf-8')
    print(f"Saving complete! {len(books_df)} books saved to \'{df_name}\'")


if __name__ == "__main__":
    main()