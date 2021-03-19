from selenium.webdriver.common.by import By
from typing import Tuple

class MainCases:
  MainCounter = (By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div[4]/div')
  DeathCounter = (By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div[6]/div')
  RecoveredCounter = (By.XPATH, '/html/body/div[3]/div[2]/div[1]/div/div[7]/div')



class CountryCases:

  @classmethod
  def get_country_info(cls,
     title : Tuple[str], 
     population : Tuple[str], 
     total_cases : Tuple[str],
     new_cases : Tuple[str],
     deaths : Tuple[str],
     recovered : Tuple[str],
     new_deaths : Tuple[str],
     active_cases : Tuple[str],
     critical_cases : Tuple[str]) -> Tuple[str]:
    country_info = (title, population, total_cases, new_cases, deaths, recovered, new_deaths, active_cases, critical_cases)
    return country_info

  @classmethod
  def get_thailand_info(cls) -> Tuple[str]:
    Thailand_Title = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[2]')
    Thailand_Population = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[14]')
    Thailand_Total_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[3]')
    Thailand_New_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[4]')
    Thailand_Deaths = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[5]')
    Thailand_Recovered = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[7]')
    Thailand_New_Deaths = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[6]')
    Thailand_Active_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[8]')
    Thailand_Critical_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[123]/td[9]')
    thailand_info = (Thailand_Title, Thailand_Population, Thailand_Total_Cases, Thailand_New_Cases, Thailand_Deaths, Thailand_Recovered, Thailand_New_Deaths, Thailand_Active_Cases, Thailand_Critical_Cases)
    return thailand_info

  @classmethod
  def get_usa_info(cls) -> Tuple[str]:
    USA_Title = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[2]')
    USA_Population = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[14]')
    USA_Total_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[3]')
    USA_New_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[4]')
    USA_Deaths = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[5]')
    USA_Recovered = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[7]')
    USA_New_Deaths = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[6]')
    USA_Active_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[8]')
    USA_Critical_Cases = (By.XPATH, '/html/body/div[3]/div[3]/div/div[4]/div[1]/div/table/tbody[1]/tr[4]/td[9]')
    USA_info = (USA_Title, USA_Population, USA_Total_Cases, USA_New_Cases, USA_Deaths, USA_Recovered, USA_New_Deaths, USA_Active_Cases, USA_Critical_Cases)
    return USA_info
