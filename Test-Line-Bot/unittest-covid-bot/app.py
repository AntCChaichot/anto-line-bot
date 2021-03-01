import unittest
from selenium import webdriver
import page

class covidScrape(unittest.TestCase):
  
  def setUp(self):
    self.driver = webdriver.Chrome()
    self.driver.get('https://www.worldometers.info/coronavirus/')

  def test_world_cases(self):
    covidPage = page.MainPage(self.driver)
    assert covidPage.title_match()
    print(covidPage.world_case)


  def test_thailand(self):
    thailandInfo = page.MainPage(self.driver)
    assert thailandInfo.title_match()
    print(thailandInfo.thailand_case)

  def test_usa(self):
    usaInfo = page.MainPage(self.driver)
    assert usaInfo.title_match()
    print(usaInfo.usa_case)

  def tearDown(self):
    self.driver.close()

if __name__ == '__main__':
  unittest.main()
