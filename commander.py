import requests
import json
import base64

# Make a GET request
# ip ='222.100.59.199'
# ip='localhost'
# response = requests.get('http://localhost:8080/')
# print("GET Response:")
# print(response.text)

#Make a POST requset with JSON data

def agent_command(ip, command, arg):
    data = {'command': command, 'arg': arg}
    header = {'Content-Type': 'application/json'}
    response = requests.post('http://'+ip+':8080/command', data=json.dumps(data), headers=header)
    print(response.text)

    

# 게스트 입장에서 다운로드 == 파일 이동 호스트 -> 게스트
def agent_download(ip:str, host_path:str, guest_path:str):
    with open(host_path, 'rb') as f:
        file_data = f.read()
    file_data = base64.b64encode(file_data)
    file_data = file_data.decode()

    data = {'file_data': file_data, 'guest_path': guest_path}
    header = {'Content-Type': 'application/json'}
    response = requests.post('http://'+ip+':8080/download', data=json.dumps(data), headers=header)    
    print(response.text)

# 게스트 입장에서 업로드 == 파일 이동 게스트 -> 호스트
def agent_upload(ip, host_path, guest_path):
    #print('http://'+ip+':8080/download?'+path)
    data = {'guest_path': guest_path}
    header = {'Content-Type': 'application/json'}
    response = requests.post('http://'+ip+':8080/upload', data=json.dumps(data), headers=header)
    data = json.loads(response.text)
    with open(host_path, 'wb') as f:
        f.write(data['file_data'].encode())

    print('GET Response: ')
    print(data['message'])
    
    

if __name__ == "__main__":
    ip = '222.100.59.199'
    agent_upload(ip, './Microsoft-Windows-Sysmon%4Operational.csv', './Microsoft-Windows-Sysmon%4Operational.csv')