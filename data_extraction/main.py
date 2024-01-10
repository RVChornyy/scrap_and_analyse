from selenium.webdriver.chrome import webdriver

from data_extraction.drivers import ChromeDriver
from selenium.webdriver.common.by import By
from data_extraction.parsers import VacancyParser
from data_extraction.utils import BASE_URL, FileWriter


def get_search_data() -> str:
    speciality = input("Enter your job position: ")
    return speciality


def get_initial_page(driver: webdriver, search_data: str) -> str:
    input_speciality = driver.find_element(By.CSS_SELECTOR, "div.input-search-job > input")
    input_area = driver.find_element(By.CSS_SELECTOR, "div.input-search-city > input")
    input_area.clear()
    search_button = driver.find_element(By.CLASS_NAME, "btn-search")
    input_speciality.send_keys(search_data)
    input_area.send_keys("Вся Україна")
    search_button.click()
    return driver.current_url


def get_vacancies() -> None:
    search_data = get_search_data()
    driver = ChromeDriver()
    parser = VacancyParser(driver.driver)
    file_writer = FileWriter()
    driver.driver.get(BASE_URL)
    initial_page_url = get_initial_page(driver.driver, search_data)
    vacancies = parser.get_job_vacancies(url=initial_page_url)
    file_writer.write_to_csv(filename=search_data, data=vacancies)
    driver.driver.quit()


if __name__ == "__main__":
    get_vacancies()
