import pymysql

class Mysql_Model :
    ### 생성자
    def __init__(self):
        self.connect_to_db()
        self.DBCursor()
        
# - DB 접속
    def connect_to_db(self):
        try:
            self.conn = pymysql.connect(
                host='3.38.241.137',
                user='backend',
                password='lkb2021',
                database='newnewsdb',
                port=3306,
                ssl={'ssl': {'ca': 'C:/Users/user/news/news/static/new-news.pem'}}
            )
            print("Database connection successful!")
            self.conn.close()
        except Exception as e:
            print(f"Error: {e}")
        
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