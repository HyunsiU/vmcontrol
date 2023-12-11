import requests
import json

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

    file_data = json.loads(response.text)
    
    with open('./cmd_reulst.txt', 'wb') as f:
        f.write(file_data['cmd_result'].encode())

    print("\nPOST Response")
    print(file_data['message'])

# 게스트 입장에서 다운로드 == 파일 이동 호스트 -> 게스트
def agent_download(ip, path:str):
    with open(path, 'rb') as f:
        file_data = f.read().decode()
    file_name = path.split('/')[-1:][0]
    data = {'file_data': file_data, 'file_name': file_name}
    header = {'Content-Type': 'application/json'}
    response = requests.post('http://'+ip+':8080/download', data=json.dumps(data), headers=header)    
    print(response.text)

# 게스트 입장에서 업로드 == 파일 이동 게스트 -> 호스트
def agent_upload(ip, path):
    #print('http://'+ip+':8080/download?'+path)
    data = {'path': path}
    header = {'Content-Type': 'application/json'}
    response = requests.post('http://'+ip+':8080/upload', data=json.dumps(data), headers=header)
    data = json.loads(response.text)
    with open('./test_'+data['file_name'], 'wb') as f:
        f.write(data['file_data'].encode())

    print('GET Response: ')
    print(data['message'])
    
    

if __name__ == "__main__":
    ip = '222.100.59.199'
    path = 'C:/Users/admin/Desktop/floder/cmd_reulst.txt'
    #ip = 'localhost'
    #agent_command(ip, 'ipconfig', '/all')
    #agent_download(ip ,'C:/Users/User/Desktop/kdt/project/vmcontrol/cmd_reulst.txt')
    agent_upload(ip, path)