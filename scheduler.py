import commander
import vbox
import event_uploader
import time

# 분석대상 파일을 real 머신에서 가상머신으로 업로드
def uploadfile_to_vm(vm_ip:str, host_path:str, guest_path:str): 
    commander.agent_download(vm_ip, host_path, guest_path)
    pass

# 업로드 분석대상 파일 실행
def exec_remote_path(vm_ip:str, remote_path:str, argument:str): 
    commander.agent_command(vm_ip, remote_path, argument)
    pass

# windows sysmon 실행 결과 이벤트 로그를 csv로 expoert(가상머신 내부에 결과 생성)
def exec_event_export(vm_ip:str):
    command ='Get-WinEvent -Path "C:/Windows/System32/winevt/Logs/Microsoft-Windows-Sysmon%4Operational.evtx" | Export-CSV "./Microsoft-Windows-Sysmon%4Operational.csv"'
    arg = ''
    commander.agent_command(vm_ip, command, arg)
    pass

# 가상머신 내부에 존재하는 이벤트 로그 csv 파일을 Real머신 환경으로 다운로드
def download_remote_file(vm_ip:str, host_path:str, guest_path:str):
    commander.agent_upload(vm_ip, host_path, guest_path)
    pass

# 다운로드 받은 이벤트 로그를 이벤트 로그 저장소에 업로드
def connect_db(db_address: str):
    return event_uploader.connetc_db(db_address)

    pass

def close_db(db_handle):
    event_uploader.close_db(db_handle)
    pass

def upload_to_db(csv_path: str, index_name:str, db_handle):
    event_uploader.upload_to_db(csv_path, index_name, db_handle)
    pass

def start_analyze(vm_name:str, file_path:str, vm_ip:str):
    # 가상머신 시작
    vb = vbox.vbox_control(vm_name)
    vb.start_vm()

    # 분석대상 파일을 Real 머신에서 가상머신으로 업로드
    remote_path = file_path
    uploadfile_to_vm(vm_ip, remote_path, remote_path)

    # 업로드 분석대상 파일 실행
    exec_remote_path(vm_ip, remote_path, '')
    
    # 실행되는시간 기다림 1분
    print('설치중입니다. 1분후 작동합니다.')
    time.sleep(60)

    # windows sysmon 실행결과 이벤트 로그를 csv로 export
    exec_event_export(vm_ip)
    print('guest_event_log to csv complete')

    # 가상머신 내부에 존재하는 이벤트 로그 csv 파일을 Real머신 환경으로 다운로드
    download_remote_file(vm_ip, './Microsoft-Windows-Sysmon%4Operational.csv', './Microsoft-Windows-Sysmon%4Operational.csv')
    print('csv 파일 다운로드 완료')

    # 가상머신 중지 및 원래 상태로 rollback
    vb.stop_vm()
    time.sleep(30)
    vb.snpapshot_rollback_vm('rollback')

    # 다운로드 받은 이벤트 로그를 이벤트 로그 저장소에 업로드
    db_handle = event_uploader.connect_db('localhost')
    event_uploader.upload_to_db('./Microsoft-Windows-Sysmon%4Operational.csv', '2023_12_13', db_handle)
    event_uploader.close_db(db_handle)

    pass

if __name__ == '__main__':
    ip = '221.154.230.16'
    analyze_target_path = './HeidiSQL_12.6.0.6765_Setup.exe'
    vm_name = 'analyze_window'
    
    start_analyze(vm_name, analyze_target_path, ip)
    # download_remote_file(ip, './Microsoft-Windows-Sysmon%4Operational.csv', './Microsoft-Windows-Sysmon%4Operational.csv')
    # exec_remote_path(ip, './HeidiSQL_12.6.0.6765_Setup.exe', '', 0)
    # command ='Get-WinEvent -Path "C:/Windows/System32/winevt/Logs/Microsoft-Windows-Sysmon%4Operational.evtx" | Export-CSV "./Microsoft-Windows-Sysmon%4Operational.csv"'
    # exec_event_export(ip, command, '')