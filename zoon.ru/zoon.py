import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains



def get_source_html(url):
    driver = webdriver.Firefox(
        executable_path="geckodriver.exe"
    )
    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(30)

        while True:
            find_more_element = driver.find_element_by_class_name('catalog-button-showMore')
            if driver.find_elements_by_class_name('minicard-item__address'):
                with open("source-page.html", "w") as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(30)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

def get_items_urls(url):
    pass

def main():
    get_source_html(url="https://spb.zoon.ru/beauty/type/manikyur/")


if __name__ == '__main__':
    main()