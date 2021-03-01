from selenium import webdriver
import page
import os

class Scrapetest:

  def __init__(self):
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--no-sandbox")
    op.add_argument("--headless")
    op.add_argument("--disable-dev-sh-usage")
    self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options = op)

  def __enter__(self):
    self.driver.get('https://www.worldometers.info/coronavirus/')
    return self

  def __exit__(self, type, value, traeback):
    self.driver.close()

  def get_world_cases(self):
    covidPage = page.MainPage(self.driver)
    assert covidPage.title_match()
    return covidPage.world_case

  def get_thailand_cases(self):
    thailandInfo = page.MainPage(self.driver)
    assert thailandInfo.title_match()
    return thailandInfo.thailand_case

  def get_usa_cases(self):
    usaInfo = page.MainPage(self.driver)
    assert usaInfo.title_match()
    return usaInfo.usa_case


