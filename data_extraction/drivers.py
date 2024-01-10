from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeDriver:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def quit_driver(self) -> None:
        if self.driver:
            self.driver.quit()
