from selenium import webdriver
import page

class Scrapetest:

  def __init__(self):
       self.driver = webdriver.Chrome()

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


