# import win32evtlog 

# pHandle = win32evtlog.OpenEventLog('localhost','Microsoft-Windows-WMI')

# flag = win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_FORWARDS_READ

# evnets = win32evtlog.ReadEventLog(pHandle, flag, 0)
# total = win32evtlog.GetNumberOfEventLogRecords(pHandle)
# print(total)

# for event in evnets:
#     print(event.Data)

# win32evtlog.CloseEventLog(pHandle)

import win32evtlog as wevt
import datetime

today = datetime.datetime.now().date()
day_ago = today - datetime.timedelta(days=1)

server = 'localhost'
logtype = 'Application'
hand = wevt.OpenEventLog(server,logtype)
flags = wevt.EVENTLOG_BACKWARDS_READ|wevt.EVENTLOG_SEQUENTIAL_READ
total = wevt.GetNumberOfEventLogRecords(hand)

while True:
    events = wevt.ReadEventLog(hand, flags,0)
    if events:
        for evt in events:
            if str(evt.TimeGenerated)[:10] == str(today):
                print('Event Category:', evt.EventCategory)
                print('Time Generated:', evt.TimeGenerated)
                print('Source Name:', evt.SourceName)
                print('Event ID:', evt.EventID)
                print('Event Type:', evt.EventType)
                data = evt.StringInserts

                if data:
                    print('Event Data:')

                    for msg in data:
                        print(msg)

                print('*' * 100)
            break

           