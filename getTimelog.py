import requests
import json
from datetime import date, timedelta, datetime
import openpyxl

studentID = '' #Your student ID
userID = '' #Your user ID
startDate='2021/09/27' #input your start date
endDate='2021/09/27' #input your end date

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = studentID 
row = [['Date', 'StartTime', 'EndTime', 'Hours', 'Type', 'Title']]

timelogHistory = 'https://ssl-timelog.csie.ntut.edu.tw/api/log/history'

payload = {'endDate': endDate,'startDate': startDate,'userID': userID}
getHistory = requests.post(timelogHistory, data=json.dumps(payload), headers={"Content-Type":"application/json"})
history = json.loads(getHistory.text)
print(getHistory.status_code)

def byteify(input, encoding='utf-8'):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode(encoding)
    else:
        return input

history = byteify(history)
history['logItemList'] = sorted(history['logItemList'], key=lambda k: k['startTime'])
for hisLog in history['logItemList'] :
  if 'LabProject' == hisLog['activityTypeName']: #you can changed the type you want to out put at here
    dateString = hisLog['startTime']
    dateString2 = hisLog['endTime']
    dateFormatter = "%Y/%m/%d %H:%M"
    x = datetime.strptime(dateString, dateFormatter)
    y = datetime.strptime(dateString2, dateFormatter)
    row.append([x.strftime('%Y/%m/%d'), x.strftime('%Y/%m/%d %H:%M:%S'), y.strftime('%Y/%m/%d %H:%M:%S'), (y-x).total_seconds()/3600, hisLog['activityTypeName'],hisLog['title']])
for info in row:
    sheet.append(info)
wb.save(studentID+'.xlsx') 