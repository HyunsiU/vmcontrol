import csv

count = 0
with open('./Microsoft-Windows-Sysmon%4Operational.csv', 'r') as f:
    data= csv.reader(f)
    for line in data:
        
        if(count == 2):
            print(line)
            print(line[4])
            break
        
        count +=1
        
    
        



