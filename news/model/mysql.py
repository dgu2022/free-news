# - DB 드라이버 연결
import pymysql

class Mysql_Model :
    ### 생성자
    def __init__(self):
        self.initDBInfo()
        self.DBConnection()
        self.DBCursor()
        
        
    ### DB 접속정보 정의
    def initDBInfo(self):
        self.host = "localhost"
        self.user = "gjuser"
        self.password = "dbdb"
        self.db = "gjdb"
        # 문자 인코딩 타입
        self.charset = "utf8"
        # 조회 시 컬럼명을 동시에 보여줄지 여부 설정
        self.cursorclass = pymysql.cursors.DictCursor
        # 입력/수정/삭제 시 DB에 자동반영 여부
        self.autocommit = True
        
# - DB 접속
    def DBConnection(self):
        try :
            self.conn = pymysql.connect(
                host = self.host, user = self.user, password = self.password, 
                db = self.db, charset = self.charset, cursorclass = self.cursorclass, 
                autocommit = self.autocommit
            )
            print("DB 접속 성공 --> ", self.conn)
        except :
            print("DB 접속 정보 확인이 필요합니다")
        
# - DB로부터 cursor 받아오기
    def DBCursor(self):
        self.cur = self.conn.cursor()
        
# - 조회/입력/수정/삭제 sql을 DB 서버로 요청 및 결과 받아오기
# - cart_model.py 에서 처리

# - DB 자원 반환
    def DBClose(self):
        try :
            self.cur.close()
            self.conn.close()
            print("DB 정보 반환 완료....")
        except :
            print("이미 DB 정보가 반환되었습니다")