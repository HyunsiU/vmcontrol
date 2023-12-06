import virtualbox

class vbox_control:

    def __init__(self, vm_name):
        self.vbox = virtualbox.VirtualBox()
        self.session = virtualbox.Session()
        self.vm_name = vm_name
        self.machine = self.vbox.find_machine(self.vm_name)
        

    def start_vm(self) -> bool:
        progress = self.machine.launch_vm_process(self.session, "gui", [])
        progress.wait_for_completion()
        print(self.vm_name+" 실행완료")
        
        pass

    def stop_vm(self) -> bool:
        re_session = self.machine.create_session()
        re_session.console.power_button()
        print(self.vm_name+" 종료완료")
        
        pass

    def list_vm(self) -> list:
        machine = list()
        for m in self.vbox.machines:
            machine.append(m)
        
        return machine
        pass
        

    def snpapshot_create_vm(self, snapshot:str, description:str) -> bool:
        re_session = self.machine.create_session()
        re_session.machine.take_snapshot(snapshot, description, True)
        print(snapshot+" 이름으로 스냅샷 생성완료")
        
        pass

    def snpapshot_remove_vm(self, snapshot:str) -> bool :
        re_session = self.machine.create_session()
        uuid = re_session.machine.find_snapshot(snapshot)
        re_session.machine.delete_snapshot(uuid.id_p)

        print(snapshot+" 이름의 스냅샷 삭제완료")
        
        pass

    def snpapshot_rollback_vm(self, snapshot:str) -> bool :
        re_session = self.machine.create_session()
        if(str(re_session.machine.state) != 'Paused'):
            uuid2 = re_session.machine.current_snapshot
            uuid = re_session.machine.find_snapshot(snapshot)

            if( uuid2.name == uuid.name):
                print("동일한 스냅샷으로 변경할 것이 없습니다.")
                pass
            re_session.machine.restore_snapshot(uuid)
            print(self.vm_name,"이",snapshot,"으로 변경되었습니다")   

        else:
            print(self.vm_name+"이 실행중입니다.")     
        
        pass

    

if __name__ == "__main__":
    vc = vbox_control('window')
    
    
    #vc.stop_vm()
    #vc.snpapshot_create_vm("tq", "맛있다")
    #vc.snpapshot_rollback_vm('식빵')
    vc.start_vm()
    # vbox list
    # machines = vc.list_vm()
    # for i in machines:
    #     print(i)