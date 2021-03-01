import time
import datetime



print('-'*40)
clock = time.ctime()
print('ctime function: ',clock)
split_clock = clock.split(' ')
time_info = [tm for tm in split_clock if ':' in tm]
current_hour = [hr.split(':')[0] for hr in time_info][0]
edited_hour = int(current_hour)-2

date_string = '10/12/2020'
thing = datetime.datetime.strptime(date_string, '%d/%m/%Y')
print(thing)
#split_time_digit = time_info[0].split(':')
#hour_digit = split_time_digit[0]
#print('current hour: ',hour_digit)
#print('-'*40)



#time_local = time.localtime()
#local = time.strftime(clock)
#print(local)
#print(time_local)

#day = datetime.date(2021,2,16)
#print(day.ctime())
