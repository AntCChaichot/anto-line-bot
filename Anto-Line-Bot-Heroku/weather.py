import requests
from typing import List, Dict, Tuple
import datetime
import os
import sys

class weatherResult:
  def __init__(self, zipcode, input_country):
    self.zipcode = str(zipcode)
    self.input_country = input_country
    OPENWEATHERMAP_TOKEN = os.getenv("OPENWEATHERMAP_TOKEN",None)
    if OPENWEATHERMAP_TOKEN is None:
      print('Specify OPENWEATHERMAP_TOKEN as environment variable.')
      sys.exit(1)

    self.ret = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip='+ self.zipcode +','+ self.input_country + OPENWEATHERMAP_TOKEN)
    self.data = dict(self.ret.json())
    try:
      self.country = self.data['city']['country']
      self.city = self.data['city']['name']

      self.data_list = self.data['list']

      self.date_time = [self.data_list[elem]['dt_txt'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
      self.temperature = [self.data_list[elem]['main']['temp'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
      self.feels_like = [self.data_list[elem]['main']['feels_like'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
      self.humidity = [self.data_list[elem]['main']['humidity'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
      self.description = [self.data_list[elem]['weather'][0]['description'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]

      assert len(self.temperature) == len (self.date_time)
      assert len(self.feels_like) == len (self.date_time)
      assert len(self.humidity) == len (self.date_time)
      assert len(self.description) == len (self.date_time)
      self.weather = [[self.date_time[i],self.temperature[i], self.feels_like[i], self.humidity[i], self.description[i]] for i in range(len(self.date_time))]
    except KeyError: # no Data
      print("No Data Found!")

  def get_all_data(self) -> Dict[str,list]:
    #self.useful_data = {'Country': self.country, 'City': self.city, 'Date,Time': self.data_time, 'Temperature': self.temperature, 'Feels Like': self.feels_like, 'Humidity': self.humidity, 'Description': self.description}
    try:
      self.useful_data = {'Country': self.country, 'City':self.city, 'Weather': self.weather}
    except AttributeError: #no data from __init__
      return
    return self.useful_data

  def get_first_data(self) -> Dict[str,list]:
    self.first_data = {'Country': self.country, 'City': self.city, 'Date,Time': self.date_time[0], 'Temperature': self.temperature[0], 'Feels Like': self.feels_like[0], 'Humidity': self.humidity[0], 'Description': self.description[0]}
    return self.first_data

  def get_specific_date_data(self, date: str, month: str) -> Dict[str,list]:
    self.specific_date = []
    self.specific_weather = []
    if len(date) == 1:
      date = str('0'+date)
    if len(month) == 1:
      month = str('0'+month)
    for elem in range(len(self.date_time)):
      if str('-'+month+'-'+date) in self.date_time[elem]:
        self.specific_date.append(self.date_time[elem])
    self.specific_weather = [e for e in self.weather if f"-{month}-{date}" in e[0]]
    if len(self.specific_date) == 0:
      raise ValueError('No data on this date!')
    
    self.specific_data = {'Country': self.country, 'City': self.city, 'Weather': self.specific_weather}
    return self.specific_data


  def get_all_today_data(self) -> Dict[str,list]:
    today_date = self.today_date_time.split(' ')[0]
    self.today_date = [self.data_list[elem]['dt_txt'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_temperature = [self.data_list[elem]['main']['temp'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_feels_like = [self.data_list[elem]['main']['feels_like'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_humidity = [self.data_list[elem]['main']['humidity'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_description = [self.data_list[elem]['weather'][0]['description'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]

    self.today_weather = [[self.today_date[i],self.today_temperature[i], self.today_feels_like[i], self.today_humidity[i], self.today_description[i]] for i in range(len(self.today_date))]

    #self.today_all_data = {'Country':self.country, 'City': self.city, 'Date,Time':self.today_date, 'Temperature':self.today_temperature, 'Feels Like': self.today_feels_like, 'Humidity': self.today_humidity, 'Description': self.today_description}
    self.today_all_data = {'Country': self.country, 'City': self.city, 'Weather': self.today_weather}
    return self.today_all_data


  @property
  def today_date_time(self) -> str:
    raw_time = datetime.datetime.today()
    today = raw_time.strftime('%Y-%m-%d %H:%M:%S')
    return today

  def get_date_time_info(self, date_time_list: List[int]) -> Tuple[str]:
    if not isinstance(date_time_list,list):
      raise TypeError ("Input is not a list")
    split_date_time = [e.split(' ')[0] for e in date_time_list]
    date_only = [i.split('-')[2] for i in split_date_time]
    return (split_date_time, date_only,)

