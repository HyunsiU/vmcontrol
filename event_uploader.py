import pymysql
import shutil
import os

def connetc_db(db_address:str):
    db_con = pymysql.connect(
        user = 'root',
        passwd = 'kdt_test',
        host = db_address,
        charset = 'utf8',
        db= 'sysmon_event'
    )


    return db_con
    pass

def upload_to_db(csv_path:str, index_name:str, db_handle):

    cursor = db_handle.cursor(pymysql.cursors.DictCursor)

    sql = 'show variables LIKE "SECURE_FILE_PRIV"' # lode_file 사용하기 위한 폴더
    cursor.execute(sql)
    result = cursor.fetchall()
    upload_path = result[0]['Value'].replace('\\','/') # \\ 를 / 로 변경
    file_name = csv_path.split('/')[-1:][0]
    shutil.copy(csv_path, upload_path+file_name)        # lode_file 폴더에 파일 업로드
        
    sql = f'insert into csv_upload(id, csv_file) values ("{index_name}", load_file("{upload_path+file_name}"))' # 파일 업로드
    cursor.execute(sql)
    db_handle.commit() # sql문 올린거 확정

    os.remove(upload_path+file_name) #업로드 이후 파일 삭제
    
    

    # sql = 'select * from csv_upload'
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # for i in result:
    #     print(i)


if __name__ == '__main__':
    upload_to_db('./2023_12_12_sysmon.csv', '2023_12_12.csv', connetc_db('localhost'))
    #connetc_db('localhost')
