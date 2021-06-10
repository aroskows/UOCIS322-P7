'''
Unit Testing for acp_testing.py
'''

import nose
import arrow
from acp_times import open_time, close_time

start = arrow.get("2021-01-01 00:00")

print("s =", start)


def test_normal_open():
    assert open_time(70, 200, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T02:04' 
    assert open_time(150, 200, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T04:25'

    temp = open_time(500, 600, start).format('YYYY-MM-DDTHH:mm')
    #print("temp = ", temp)
    assert temp ==  '2021-01-01T15:28'

def test_normal_close():
    assert close_time(70,200, start).format('YYYY-MM-DDTHH:mm') ==  '2021-01-01T04:40'
    assert close_time(150,200, start).format('YYYY-MM-DDTHH:mm') ==  '2021-01-01T10:00'
    temp =  close_time(500,600, start).format('YYYY-MM-DDTHH:mm') 
    #print(temp)
    assert temp ==  '2021-01-02T9:20'

def test_small_open():
    assert open_time(0, 600, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T00:00'
    assert open_time(10,1000, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T00:18' 
    assert open_time(60,400, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T01:46' 

def test_small_close():
    assert close_time(0, 600, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T01:00'
    t = close_time(10,1000, start).format('YYYY-MM-DDTHH:mm') 
    #print(t)
    assert t == '2021-01-01T01:30' 
    assert close_time(60,400, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T04:00' 

def test_big_open():
    assert open_time(235, 200, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T05:53'
    temp = open_time(609, 600, start).format('YYYY-MM-DDTHH:mm')
    #print(temp)
    assert temp ==  '2021-01-01T18:48'
    assert open_time(1200, 1000, start).format('YYYY-MM-DDTHH:mm') == '2021-01-02T09:05'

def test_big_close():
    assert close_time(235, 200, start).format('YYYY-MM-DDTHH:mm') == '2021-01-01T13:30'
    temp = close_time(609, 600, start).format('YYYY-MM-DDTHH:mm')
    #print(temp)
    assert temp ==  '2021-01-02T16:00'
    assert close_time(1200, 1000, start).format('YYYY-MM-DDTHH:mm') == '2021-01-04T03:00'

#rslt = nose.run()
print(nose.run())
