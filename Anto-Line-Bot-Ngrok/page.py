from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from locators import *

class BasePage:
  def __init__(self,driver):
    self.driver = driver

class MainPage(BasePage):

  @property
  def world_case(self) -> str:
    driver = self.driver
    WebDriverWait(driver,10).until(
      lambda driver: driver.find_element_by_class_name('maincounter-number')
        )
    raw_info = storeData(driver)
    info = raw_info.main_data()
    readable_info = self.print_main_text(info)
    #readable_info = self.print_text(*info)
    return readable_info
  
  @property
  def thailand_case(self) -> str:
    driver = self.driver
    #WebDriverWait(driver,10).until(
    #    lambda driver: driver.find_element_by_class_name('maincounter-number')
    #    )
    thailand_elements = CountryCases.get_thailand_info() #import from locators
    thailand_xpaths_info = CountryCases.get_country_info(*thailand_elements)
    thailand_raw_info = storeData(driver)
    thailand_info = thailand_raw_info.country_data(thailand_xpaths_info)
    thailand_readable_info = self.print_country_text(thailand_info)
    return thailand_readable_info

  @property
  def usa_case(self) -> str:
    driver = self.driver
    #WebDriverWait(driver,10).until(
    #  lambda driver: driver.find_element_by_class_name('maincounter-number')
    #    )
    usa_elements = CountryCases.get_usa_info()
    usa_xpaths_info = CountryCases.get_country_info(*usa_elements)
    usa_raw_info = storeData(driver)
    usa_info = usa_raw_info.country_data(usa_xpaths_info)
    usa_readable_info = self.print_country_text(usa_info)
    return usa_readable_info


  def print_main_text(self, cases_info: Tuple[str]) -> str:
    total_cases, dead_cases, recovered_cases = cases_info
    rv = f"""Total Cases around the World: {total_cases}
Deaths around the World: {dead_cases}
Recovered Cases around the World: {recovered_cases}"""
    return rv

  def print_country_text(self, country_info: Tuple[str]) -> None:
    filtering_data = [(*country_info)]
    filtered_data = tuple( map(lambda x: 'Not Updated' if x == '' else x ,filtering_data))
    title, population, total_cases, new_cases, deaths, recovered, new_deaths, active_cases, critical_cases = filtered_data
    rv = f"""Country: {title}
Population: {population}
Total Cases: {total_cases}
New Cases: {new_cases}
Total Deaths: {deaths}
Recovered Cases: {recovered}
New Deaths: {new_deaths}
Active Cases: {active_cases}
Critical Cases: {critical_cases}"""

    return rv
   
  #Alternative Printing Function 
  #def print_text(self,total, dead, recovered):
  #  print('Total Cases around the World: ', total)
  #  print('Deaths around the World: ', dead)
  #  print('Recovered Cases around the World: ', recovered)

  def title_match(self) -> bool:
    return 'covid live update' in self.driver.title.strip().lower()

  def click_sort_country(self) -> None:
      driver = self.driver
      accept_cookie = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/a')))
      accept_cookie.click()
      sort_button = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/thead/tr/th[2]')))
      sort_button.click()

class storeData(BasePage):

  def main_data(self) -> Tuple[str]:
    totalCases = self.driver.find_element(*MainCases.MainCounter)
    deadCases = self.driver.find_element(*MainCases.DeathCounter)
    recoveredCases = self.driver.find_element(*MainCases.RecoveredCounter)
    return (totalCases.text, deadCases.text, recoveredCases.text)


  def country_data(self, country_info: Tuple[str]) -> Tuple['webDriver_element']:
    title, population, total_cases, new_cases, deaths, recovered, new_deaths, active_cases, critical_cases = country_info
    Country_Title = self.driver.find_element(*title)
    Country_Population = self.driver.find_element(*population)
    Country_Total = self.driver.find_element(*total_cases)
    Country_New_Cases = self.driver.find_element(*new_cases)
    Country_Deaths = self.driver.find_element(*deaths)
    Country_Recovered = self.driver.find_element(*recovered)
    Country_New_Deaths = self.driver.find_element(*new_deaths)
    Country_Active_Cases = self.driver.find_element(*active_cases)
    Country_Critical_Cases = self.driver.find_element(*critical_cases)
    return (Country_Title.text, Country_Population.text, Country_Total.text, Country_New_Cases.text, Country_Deaths.text, Country_Recovered.text, Country_New_Deaths.text, Country_Active_Cases.text, Country_Critical_Cases.text)
