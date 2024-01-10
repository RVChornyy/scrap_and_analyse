from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from data_extraction.drivers import ChromeDriver
from data_extraction.utils import PreCleanData, BASE_URL, Vacancy


class VacancyParser:
    def __init__(self, veb_driver: webdriver):
        self.driver = veb_driver

    def parse_single_vacancy(self, link: str) -> Vacancy:
        self.driver.get(urljoin(BASE_URL, link))
        cleaner = PreCleanData()
        page_to_parse = self.driver.page_source
        soup = BeautifulSoup(page_to_parse, "html.parser")
        date_data = soup.select_one(".add-top .add-bottom-sm").text
        date = cleaner.clean_date(date_data)
        title = soup.select_one("#h1-name").text
        salary_data = soup.select_one(".add-top-sm span[title='Зарплата']+span")
        if salary_data:
            salary_margin = cleaner.clean_salary_margin(salary_data.text)
        else:
            salary_margin = "Unknown"
        if isinstance(salary_margin, list):
            salary = sum(salary_margin) / len(salary_margin)
        else:
            salary = None
        technology_data = soup.select_one("#job-description")
        technology_stack = cleaner.clean_technology_stack(technology_data.text)
        required_experience_data = soup.select_one(".add-top-sm>span[title='Умови й вимоги']").find_previous()
        required_experience = cleaner.clean_experience(required_experience_data.text)
        if not required_experience:
            required_experience = 0
        try:
            company = soup.select_one("a.hovered>span").text
        except AttributeError:
            company = "Unknown"
        return Vacancy(
            date=date,
            title=title,
            site_id=link,
            company=company,
            technology_stack=technology_stack,
            salary_margin=salary_margin,
            salary=salary,
            required_experience=required_experience
        )

    @staticmethod
    def get_page_vacancies_links(soup: BeautifulSoup):
        vacancies_links_soup = soup.select("h2.cut-bottom a")
        vacancies_links = []
        for link in vacancies_links_soup:
            vacancies_links.append(link["href"])
        return vacancies_links

    def get_job_vacancies(
            self,
            url: str,
    ) -> list[Vacancy]:
        self.driver.get(url)
        all_vacancies_links = []

        while True:
            page_to_parse = self.driver.page_source
            soup = BeautifulSoup(page_to_parse, "html.parser")
            page_vacancies_links = self.get_page_vacancies_links(soup)
            all_vacancies_links += page_vacancies_links
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, ".add-left-sm a")
                self.driver.execute_script("arguments[0].click();", next_button)
            except NoSuchElementException:
                break
        vacancies = []
        all_vacancies_links = set(all_vacancies_links)

        for link in all_vacancies_links:
            vacancies.append(self.parse_single_vacancy(link))

        return vacancies


if __name__ == "__main__":
    driver = ChromeDriver()
    parser = VacancyParser(driver.driver)
    parser.parse_single_vacancy("https://www.work.ua/jobs/5459142/")
