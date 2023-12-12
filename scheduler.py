import commander
import vbox

# 분석대상 파일을 real 머신에서 가상머신으로 업로드
def uploadfile_to_vm(vm_ip:str, host_path:str, guest_path:str): 
    commander.agent_download(vm_ip, host_path, guest_path)
    pass

# 업로드 분석대상 파일 실행
def exec_remote_path(vm_ip:str, remote_path:str, argument:str, timeout:int): 
    commander.agent_command(vm_ip, remote_path, argument)
    pass

# windows sysmon 실행 결과 이벤트 로그를 csv로 expoert(가상머신 내부에 결과 생성)
def exec_event_export(vm_ip:str, command, arg):
    commander.agent_command(vm_ip, command, arg)
    pass

# 가상머신 내부에 존재하는 이벤트 로그 csv 파일을 Real머신 환경으로 다운로드
def download_remote_file(vm_ip:str, host_path:str, guest_path:str):
    commander.agent_upload(vm_ip, host_path, guest_path)
    pass

# 다운로드 받은 이벤트 로그를 이벤트 로그 저장소에 업로드
def connect_db(db_address: str):
    pass

def close_db(db_handle):
    pass

def upload_to_db(csv_path: str, indeex_name:str, db_handle):
    pass

def start_analyze(vm_name:str, file_path:str, argument:str, timeout:int):
    pass

if __name__ == '__main__':
    ip = '222.100.59.199'
    download_remote_file(ip, './Microsoft-Windows-Sysmon%4Operational.csv', './Microsoft-Windows-Sysmon%4Operational.csv')
    #exec_remote_path(ip, './HeidiSQL_12.6.0.6765_Setup.exe', '', 0)
    # command ='Get-WinEvent -Path "C:/Windows/System32/winevt/Logs/Microsoft-Windows-Sysmon%4Operational.evtx" | Export-CSV "./Microsoft-Windows-Sysmon%4Operational.csv"'
    # exec_event_export(ip, command, '')