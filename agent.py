from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
import subprocess

# exec_command: cmd 실행해서 파일로 저장 할꺼임
def exec_command(command:str, arg:str) -> bytes:
    command = command+' '+arg
    cmd_result = subprocess.check_output(command)
    return cmd_result

 
# save_file: 호스트에서 받아서 게스트에 저장할거임
def save_file(data:bytes, save_path:str) -> bool:
    try:
        with open(save_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f'{str(e)}')

# load_file: 게스트에서 받아서 호스트에 저장할거임
def load_file(file_path) -> str:
    with open(file_path, 'rb') as f:
        data = f.read()
        
    return data

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!')
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
       
    def do_POST(self):
        path = urlparse(self.path).path
        
        # 게스트 입장에서 업로드 == 파일 이동 게스트 -> 호스트
        if path == '/upload': 
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try: 
                data = json.loads(post_data.decode('utf-8'))
                
                file_data = load_file(data['path']).decode()
                
                file_name = data['path'].split('/')[-1:][0]

                response_data = {'message':'Data received successfully','file_data': file_data, 'file_name':file_name}
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))

            except FileNotFoundError as e:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'FileNotFoundError')
                print('파일없다')

        # 게스트 입장에서 다운로드 == 파일 이동 호스트 -> 게스트
        elif path == '/download':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                save_file(data['file_data'].encode(), './'+data['file_name'])
                

                response_data = {'message':'Data received successfully'}
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bad Request: Invalid JSON data')

        # 커맨드 명령 받아서 결과값 호스트에 저장
        elif path =='/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                cmd_result = exec_command(data['command'], data['arg']).decode('euc-kr')
                response_data =  {'message': 'Data received successfully', 'data': data, 'cmd_result': cmd_result}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))


            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bad Request: Invalid JSON data')

        # 없는 페이지 일시                                
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
        
        pass

def run_server():
    address = ('0.0.0.0', 8080)
    with HTTPServer(address, MyRequestHandler) as server:
        print('Starting server...')
        server.serve_forever()

if __name__ == "__main__":
    run_server()