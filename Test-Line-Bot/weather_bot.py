import requests
from typing import List, Dict, Tuple
import datetime


#weather = {'Country':info[0], 'Name':info[1],'2':info[2],'3':info[3],'4':info[4],'5':info[5],'6':info[6]}
#	TextSendMessage(text="Country: " + str(weather['Country']) + "\nName: " + str(weather['Name'])),
#	TextSendMessage(text="Date/Time: " + str(weather['2'][0]) + "\nTemperature: " + str(weather['2'][1]) + "\nHumidity: " + str(weather['2'][2]) + "\nDescription: " + str(weather['2'][3])),		TextSendMessage(text="Date/Time: " + str(weather['3'][0]) + "\nTemperature: " + str(weather['3'][1]) + "\nHumidity: " + str(weather['3'][2]) + "\nDescription: " + str(weather['3'][3])),		TextSendMessage(text="Date/Time: " + str(weather['4'][0]) + "\nTemperature: " + str(weather['4'][1]) + "\nHumidity: " + str(weather['4'][2]) + "\nDescription: " + str(weather['4'][3])),		TextSendMessage(text="Date/Time: " + str(weather['5'][0]) + "\nTemperature: " + str(weather['5'][1]) + "\nHumidity: " + str(weather['5'][2]) + "\nDescription: " + str(weather['5'][3]))

class weatherResult:
  def __init__(self):
    self.ret = requests.get('http://api.openweathermap.org/data/2.5/forecast?zip=10540,th&APPID=7743f38ce634083abe786e2d679955e3&units=metric')
    self.data = dict(self.ret.json())
    self.country = self.data['city']['country']
    self.city = self.data['city']['name']

    self.data_list = self.data['list']

    self.date_time = [self.data_list[elem]['dt_txt'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
    self.temperature = [self.data_list[elem]['main']['temp'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
    self.feels_like = [self.data_list[elem]['main']['feels_like'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
    self.humidity = [self.data_list[elem]['main']['humidity'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]
    self.description = [self.data_list[elem]['weather'][0]['description'] for elem in range(len(self.data_list)) if self.today_date_time <= self.data_list[elem]['dt_txt']]


  def get_all_data(self) -> Dict[str,list]:
    self.useful_data = {'Country': self.country, 'City':self.city,  'Date,Time':self.date_time, 'Temperature': self.temperature, 'Feels Like': self.feels_like, 'Humidity': self.humidity, 'Description': self.description}
    assert len(self.temperature) == len (self.date_time)
    assert len(self.feels_like) == len (self.date_time)
    assert len(self.humidity) == len (self.date_time)
    assert len(self.description) == len (self.date_time)
    return self.useful_data

  def get_latest_data(self) -> Dict[str,list]:
    self.latest_data = {'Country': self.country, 'City': self.city, 'Date,Time': self.date_time[0], 'Temperature': self.temperature[0], 'Feels Like': self.feels_like[0], 'Humidity': self.humidity[0], 'Description': self.description[0]}
    return self.latest_data

  def get_specific_date_data(self, date: str, month: str) -> Dict[str,list]:
    self.specific_date = []
    self.specific_temp = []
    self.specific_feels = []
    self.specific_humidity = []
    self.specific_description = []
    if date == 'today':
      _, today_date_list = self.get_date_time_info([self.today_date_time])
      date = today_date_list[0]
    elif len(date) == 1 and len(month) == 1:
      month = str('0'+month)
      date = str('0'+date)
    for elem in range(len(self.date_time)):
      if str('-'+month+'-'+date) in self.date_time[elem]:
        self.specific_date.append(self.date_time[elem])
        self.specific_temp.append(self.temperature[elem])
        self.specific_feels.append(self.feels_like[elem])
        self.specific_humidity.append(self.humidity[elem])
        self.specific_description.append(self.description[elem])
    if len(self.specific_date) == 0:
      raise ValueError('No data on this date!')
    assert len(self.specific_temp) == len (self.specific_date)
    assert len(self.specific_feels) == len (self.specific_date)
    assert len(self.specific_humidity) == len (self.specific_date)
    assert len(self.specific_description) == len (self.specific_date)

    self.specific_data = {'Country': self.country, 'City': self.city, 'Date,Time': self.specific_date, 'Temperature': self.specific_temp, 'Feels Like': self.specific_feels, 'Humidity': self.specific_humidity, 'Description': self.specific_description}
    return self.specific_data


  def get_all_today_data(self) -> Dict[str,list]:
    today_date = self.today_date_time.split(' ')[0]
    self.today_date = [self.data_list[elem]['dt_txt'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_temperature = [self.data_list[elem]['main']['temp'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_feels_like = [self.data_list[elem]['main']['feels_like'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_humidity = [self.data_list[elem]['main']['humidity'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]
    self.today_description = [self.data_list[elem]['weather'][0]['description'] for elem in range(len(self.data_list)) if today_date in self.data_list[elem]['dt_txt']]

    self.today_all_data = {'Country':self.country, 'City': self.city, 'Date,Time':self.today_date, 'Temperature':self.today_temperature, 'Feels Like': self.today_feels_like, 'Humidity': self.today_humidity, 'Description': self.today_description}
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


something = weatherResult()
try:
  print(something.get_specific_date_data('10','03'))
except ValueError:
  print("No data on this date!")
except TypeError:
  print("Wrong Input")
