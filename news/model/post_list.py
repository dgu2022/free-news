import pymysql
from mysqlapp.model.mysql import Mysql_Model

class MyPost :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 자신이 쓴 기사 최신 순으로 1개 불러오기
    def getMyPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 가장 조회수 높은 기사 불러오기
    def getMyPostMain1(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
        
    #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 댓글이 가장 많은 포스트 불러오기
    def getMyPostMain2(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    #구독한 기자들(구독을 안했을 경우 전체 기자)이 쓴 기사 중 최신 작성 순으로 10개 뽑아 그중 랜덤으로 4개 뽑고 + 전체 기자들이 쓴 기사 중 오늘 올라온 기사 조회수 높은 순으로 3개 불러오기
    def getMyPostMain3(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    # 분야별로 전체 기자들이 쓴 기사 중 최신 기사 3개를 뽑고 + 분야별로 전체 기자들이 쓴 기사 중 오늘 올라운 기사 중 내가 읽지 않은 기사 중 조회수 높은 순으로 3개 불러오기 
    def getNewPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    # 전체 기자들이 쓴 기사 중 작성일이 하루가 지나지 않은 기사 중 조회수 가장 높은 기사 불러오기
    def getHotPostToday(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    # 전체 기자들이 쓴 기사 중 작성일이 일주일이 지나지 않은 기사 중 조회수 높은 순으로 2개 불러오기
    def getHotPostWeek(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
class FullPost :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 전체 포스트 중 조회수 높은 포스트 불러오기
    def getPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    # 전체 포스트 중 댓글 많은 포스트 불러오기
    def getPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
class WritePost :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기사 작성하기
    def writePost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
class Donate:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기사 작성하기
    def donate(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows

class Register :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 아이디, 비밀번호, 이름 저장하기
    def getMyPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
class Login :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 아이디와 비밀번호와 일치하는 user가 있는지 확인하고, 있으면 user 정보 반환
    def getMyPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
class Subscribe :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 특정 user를 구독하기 (어떻게 구현?)
    def getMyPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
    # 특정 user를 구독 취소하기 (어떻게 구현?)
    def getMyPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows
    
class Search :
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기사 제목을 입력해 입력한 내용이 제목에 포함된 기사 반환
    def searchPost(self):
        sql = """
        Select cart_member, cart_no    
        From cart   
        Order By cart_member,cart_no
        """
        ### DB에 요청하기 : cursor에 담기
        # rs_cnt : 실행 결과의 건수
        rs_cnt = self.db.cur.execute(sql)
        # 실행 결과 데이터
        rows = self.db.cur.fetchall()
        # DB 정보 반환
        self.db.DBClose()
        return rs_cnt, rows