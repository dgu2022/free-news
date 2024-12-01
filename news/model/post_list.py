import pymysql
from news.model.mysql import Mysql_Model
import bcrypt
import random

class MyPost:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 자신이 쓴 기사 최신 순으로 1개 불러오기
    def get_my_post(self, current_journalist_id):
        try:
            sql = """
            SELECT articleID, title, content, created_at
            FROM ARTICLE
            WHERE journalistID = %s
            ORDER BY created_at DESC
            LIMIT 1
            """
            self.db.cur.execute(sql, (current_journalist_id,))
            article = self.db.cur.fetchone()

            if article:
                return True, article  # 최신 기사 반환
            else:
                return False, "작성한 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "최신 기사 조회 실패"
        finally:
            self.db.DBClose()
    
    #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 가장 조회수 높은 기사 불러오기
    def getMyPostMain1(self, current_reader_id):
        try:
            sql = """
            SELECT a.articleID, a.title, a.views
            FROM ARTICLE a
            JOIN SUBSCRIPTION s ON s.journalistID = a.journalistID
            LEFT JOIN ARTICLE_VIEW av ON av.articleID = a.articleID AND av.memberID = s.readerID
            WHERE s.readerID = %s AND av.viewID IS NULL
            ORDER BY a.views DESC
            LIMIT 1
            """
            self.db.cur.execute(sql, (current_reader_id,))
            article = self.db.cur.fetchone()

            if article:
                return True, article  # 조회수 높은 기사 반환
            else:
                return False, "읽지 않은 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "읽지 않은 기사 조회 실패"
        finally:
            self.db.DBClose()
        
    #구독한 기자들이 쓴 기사 중 내가 읽지 않은 기사 중 댓글이 가장 많은 포스트 불러오기
    def getMyPostMain2(self, current_reader_id):
        try:
            sql = """
            SELECT a.articleID, a.title, COUNT(c.commentID) AS commentCount
            FROM ARTICLE a
            JOIN SUBSCRIPTION s ON s.journalistID = a.journalistID
            LEFT JOIN ARTICLE_VIEW av ON av.articleID = a.articleID AND av.memberID = s.readerID
            LEFT JOIN COMMENT c ON c.articleID = a.articleID AND c.is_deleted = FALSE
            WHERE s.readerID = %s AND av.viewID IS NULL
            GROUP BY a.articleID
            ORDER BY commentCount DESC
            LIMIT 1
            """
            self.db.cur.execute(sql, (current_reader_id,))
            article = self.db.cur.fetchone()

            if article:
                return True, article  # 댓글 많은 기사 반환
            else:
                return False, "읽지 않은 댓글 많은 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "댓글 많은 기사 조회 실패"
        finally:
            self.db.DBClose()
    
    #구독한 기자들(구독을 안했을 경우 전체 기자)이 쓴 기사 중 최신 작성 순으로 10개 뽑아 그중 랜덤으로 4개 뽑고 + 전체 기자들이 쓴 기사 중 오늘 올라온 기사 조회수 높은 순으로 3개 불러오기
    # getMyPostMain3 => 이거는 분리가 필요해서 나눌게
    # 1. 최신 10개 중 랜덤 4개 기사 조회
    def get_random_articles_from_latest(self, current_reader_id):
        try:
            # 최신 10개 기사를 가져오는 쿼리
            sql = """
            SELECT articleID, title, created_at
            FROM ARTICLE
            WHERE journalistID IN (
                SELECT journalistID
                FROM SUBSCRIPTION
                WHERE readerID = %s
            ) OR NOT EXISTS (
                SELECT 1 FROM SUBSCRIPTION WHERE readerID = %s
            )
            ORDER BY created_at DESC
            LIMIT 10
            """
            self.db.cur.execute(sql, (current_reader_id, current_reader_id))
            articles = self.db.cur.fetchall()

            if not articles:
                return False, "최신 기사가 없습니다."

            # 10개 중 랜덤으로 4개 선택
            random_articles = random.sample(articles, min(4, len(articles)))
            return True, random_articles
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "랜덤 기사 조회 실패"
        finally:
            self.db.DBClose()

    # 2. 오늘 올라온 조회수 높은 3개 기사 조회
    def get_top_articles_today(self):
        try:
            sql = """
            SELECT articleID, title, views
            FROM ARTICLE
            WHERE DATE(created_at) = CURDATE()
            ORDER BY views DESC
            LIMIT 3
            """
            self.db.cur.execute(sql)
            articles = self.db.cur.fetchall()

            if not articles:
                return False, "오늘 올라온 기사가 없습니다."

            return True, articles
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "오늘 기사 조회 실패"
        finally:
            self.db.DBClose()
    
    # 분야별로 전체 기자들이 쓴 기사 중 최신 기사 3개를 뽑고 + 분야별로 전체 기자들이 쓴 기사 중 오늘 올라운 기사 중 내가 읽지 않은 기사 중 조회수 높은 순으로 3개 불러오기 
    # getNewPost => 이거는 분리가 필요해서 나눌게
    # 1. 분야별 전체 기자들이 쓴 최신 기사 3개 조회
    def get_latest_articles_by_category(self):
        try:
            sql = """
            SELECT category, articleID, title, created_at
            FROM (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY created_at DESC) AS row_num
                FROM ARTICLE
            ) t
            WHERE row_num <= 3
            """
            self.db.cur.execute(sql)
            articles = self.db.cur.fetchall()

            if articles:
                return True, articles  # 분야별 최신 기사 반환
            else:
                return False, "분야별 최신 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "분야별 최신 기사 조회 실패"
        finally:
            self.db.DBClose()

    # 2. 분야별 내가 읽지 않은 오늘 올라온 조회수 높은 기사 3개 조회
    def get_unread_top_articles_today_by_category(self, current_reader_id):
        try:
            sql = """
            SELECT category, articleID, title, views
            FROM (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY views DESC) AS row_num
                FROM ARTICLE a
                LEFT JOIN ARTICLE_VIEW av ON av.articleID = a.articleID AND av.memberID = %s
                WHERE DATE(a.created_at) = CURDATE() AND av.viewID IS NULL
            ) t
            WHERE row_num <= 3
            """
            self.db.cur.execute(sql, (current_reader_id,))
            articles = self.db.cur.fetchall()

            if articles:
                return True, articles  # 분야별 오늘의 읽지 않은 인기 기사 반환
            else:
                return False, "오늘 올라온 읽지 않은 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "오늘 읽지 않은 기사 조회 실패"
        finally:
            self.db.DBClose()
    
    # 전체 기자들이 쓴 기사 중 작성일이 하루가 지나지 않은 기사 중 조회수 가장 높은 기사 불러오기
    def getHotPostToday(self):
        try:
            sql = """
            SELECT articleID, title, views
            FROM ARTICLE
            WHERE created_at >= NOW() - INTERVAL 1 DAY
            ORDER BY views DESC
            LIMIT 1
            """
            self.db.cur.execute(sql)
            article = self.db.cur.fetchone()

            if article:
                return True, article  # 가장 조회수가 높은 기사 반환
            else:
                return False, "하루 이내 작성된 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "기사 조회 실패"
        finally:
            self.db.DBClose()
    
    # 전체 기자들이 쓴 기사 중 작성일이 일주일이 지나지 않은 기사 중 조회수 높은 순으로 2개 불러오기
    def getHotPostWeek(self):
        try:
            sql = """
            SELECT articleID, title, views
            FROM ARTICLE
            WHERE created_at >= NOW() - INTERVAL 7 DAY
            ORDER BY views DESC
            LIMIT 2
            """
            self.db.cur.execute(sql)
            articles = self.db.cur.fetchall()

            if articles:
                return True, articles  # 조회수 높은 기사 반환
            else:
                return False, "일주일 이내 작성된 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "기사 조회 실패"
        finally:
            self.db.DBClose()

    # 구독한 기자들의 읽지 않은 조회수 높은 기사
    def get_unread_popular_article(self, reader_id):
        try:
            sql = """
            SELECT 
                a.articleID, a.title, a.views
            FROM 
                ARTICLE a
            JOIN 
                SUBSCRIPTION s ON s.journalistID = a.journalistID
            LEFT JOIN 
                ARTICLE_VIEW av ON av.articleID = a.articleID AND av.memberID = s.readerID
            WHERE 
                s.readerID = %s
                AND av.viewID IS NULL
            ORDER BY 
                a.views DESC
            LIMIT 1
            """
            self.db.cur.execute(sql, (reader_id,))
            article = self.db.cur.fetchone()
            
            if article:
                return True, article  # 읽지 않은 기사 반환
            else:
                return False, "읽지 않은 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "읽지 않은 기사 조회 실패"
        finally:
            self.db.DBClose()
    
class FullPost:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 전체 포스트 중 조회수 높은 포스트 불러오기
    # 조회수 높은 기사
    def get_top_articles_by_views(self):
        try:
            sql = """
            SELECT articleID, title, views
            FROM ARTICLE
            ORDER BY views DESC
            LIMIT 10
            """
            self.db.cur.execute(sql)
            articles = self.db.cur.fetchall()

            if articles:
                return True, articles  # 상위 기사 목록 반환
            else:
                return False, "조회수 높은 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "조회수 높은 기사 조회 실패"
        finally:
            self.db.DBClose()
    
    # 전체 포스트 중 댓글 많은 포스트 불러오기
    def get_most_commented_article(self):
        try:
            sql = """
            SELECT a.articleID, a.title, COUNT(c.commentID) AS commentCount
            FROM ARTICLE a
            LEFT JOIN COMMENT c ON c.articleID = a.articleID AND c.is_deleted = FALSE
            GROUP BY a.articleID
            ORDER BY commentCount DESC
            LIMIT 1
            """
            self.db.cur.execute(sql)
            article = self.db.cur.fetchone()

            if article:
                return True, article  # 댓글 많은 기사 반환
            else:
                return False, "댓글이 많은 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "댓글 많은 기사 조회 실패"
        finally:
            self.db.DBClose()

    # 키워드로 기사 검색
    def search_articles_by_keyword(self, keyword):
        try:
            sql = """
            SELECT articleID, title, content, category, views
            FROM ARTICLE
            WHERE title LIKE CONCAT('%', %s, '%') OR content LIKE CONCAT('%', %s, '%')
            ORDER BY views DESC
            """
            self.db.cur.execute(sql, (keyword, keyword))
            articles = self.db.cur.fetchall()
            if articles:
                return True, articles  # 검색 결과 반환
            else:
                return False, "검색 결과가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "기사 검색 실패"
        finally:
            self.db.DBClose()

    # 구독자 많은 기자의 기사
    def get_top_articles_by_subscriptions(self):
        try:
            sql = """
            SELECT a.articleID, a.title, COUNT(s.subscriptionID) AS totalSubscriptions
            FROM ARTICLE a
            JOIN SUBSCRIPTION s ON s.journalistID = a.journalistID
            GROUP BY a.articleID
            ORDER BY totalSubscriptions DESC, a.views DESC
            LIMIT 10
            """
            self.db.cur.execute(sql)
            articles = self.db.cur.fetchall()

            if articles:
                return True, articles  # 상위 기사 목록 반환
            else:
                return False, "구독자 많은 기자의 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "구독자 많은 기자의 기사 조회 실패"
        finally:
            self.db.DBClose()
            """
            from post_list import FullPost

            # FullPost 클래스 인스턴스 생성
            fullpost = FullPost()

            # 조회수 높은 기사
            success, result = fullpost.get_top_articles_by_views()
            if success:
                print("조회수 높은 기사:")
                for article in result:
                    print(f"기사 ID: {article['articleID']}, 제목: {article['title']}, 조회수: {article['views']}")
            else:
                print(result)

            # 구독자 많은 기자의 기사
            success, result = fullpost.get_top_articles_by_subscriptions()
            if success:
                print("구독자 많은 기자의 기사:")
                for article in result:
                    print(f"기사 ID: {article['articleID']}, 제목: {article['title']}, 총 구독자 수: {article['totalSubscriptions']}")
            else:
                print(result)
            """
    
class WritePost:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기사 작성하기 (create_article)
    def WritePost(self, journalist_id, title, content, category):
        try:
            sql = """
            INSERT INTO ARTICLE (journalistID, title, content, category, likes, dislikes, views, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 0, 0, 0, NOW(), NOW())
            """
            
            # 쿼리 실행
            self.db.cur.execute(sql, (journalist_id, title, content, category))
            # 변경 사항 저장
            self.db.conn.commit()
            return True  # 작성 성공
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()  # 에러 발생 시 롤백
            return False  # 작성 실패
        finally:
            self.db.DBClose()

    # 기사 수정하기 (update_article)
    def updatePost(self, article_id, journalist_id, title, content, category):
        try:
            sql = """
            UPDATE ARTICLE
            SET title = %s, content = %s, category = %s, updated_at = NOW()
            WHERE articleID = %s AND journalistID = %s
            """
            
            # 쿼리 실행
            rows_affected = self.db.cur.execute(sql, (title, content, category, article_id, journalist_id))
            # 변경 사항 저장
            self.db.conn.commit()
            
            if rows_affected > 0:
                return True  # 수정 성공
            else:
                return False  # 수정할 기사 없음
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()  # 에러 발생 시 롤백
            return False
        finally:
            self.db.DBClose()

    # 기사 삭제하기 (delete_article)
    def deletePost(self, article_id, journalist_id):
        try:
            sql = """
            DELETE FROM ARTICLE
            WHERE articleID = %s AND journalistID = %s
            """
            
            # 쿼리 실행
            rows_affected = self.db.cur.execute(sql, (article_id, journalist_id))
            # 변경 사항 저장
            self.db.conn.commit()
            
            if rows_affected > 0:
                return True  # 삭제 성공
            else:
                return False  # 삭제할 기사 없음
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()  # 에러 발생 시 롤백
            return False
        finally:
            self.db.DBClose()

    # 기사 조회수 증가
    def increase_views(self, article_id):
        try:
            sql = """
            UPDATE ARTICLE
            SET views = views + 1
            WHERE articleID = %s
            """
            rows_affected = self.db.cur.execute(sql, (article_id,))
            self.db.conn.commit()
            return rows_affected > 0  # 업데이트 성공 여부 반환
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False
        finally:
            self.db.DBClose()

    # 기사 조회 기록 저장(중복 방지 및 업데이트 처리)
    def save_article_view(self, member_id, article_id):
        try:
            # 중복 방지 및 업데이트 처리
            sql = """
            INSERT INTO ARTICLE_VIEW (memberID, articleID, view_date)
            VALUES (%s, %s, NOW())
            ON DUPLICATE KEY UPDATE view_date = NOW()
            """
            self.db.cur.execute(sql, (member_id, article_id))
            self.db.conn.commit()
            return True, "기사 조회 기록 저장 성공"
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False, "기사 조회 기록 저장 실패"
        finally:
            self.db.DBClose()

    # 특정 Article ID로 기사 정보 조회
    def get_article_by_id(self, article_id):
        try:
            sql = """
            SELECT articleID, title, content, category, likes, dislikes, views, created_at, updated_at
            FROM ARTICLE
            WHERE articleID = %s
            """
            self.db.cur.execute(sql, (article_id,))
            article = self.db.cur.fetchone()

            if article:
                return True, article  # 기사 정보 반환
            else:
                return False, "해당 Article ID에 해당하는 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "기사 조회 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()
    
class Donate:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기자 후원
    def donate(self, reader_id, journalist_id, amount):
        try:
            # 명시적으로 트랜잭션 시작
            self.db.conn.begin()

            # 1. 대상(기자)의 상태를 잠금
            lock_journalist_sql = """
            SELECT points
            FROM MEMBER
            WHERE memberID = %s
            FOR UPDATE
            """
            self.db.cur.execute(lock_journalist_sql, (journalist_id,))
            journalist_data = self.db.cur.fetchone()

            if not journalist_data:
                return False, "후원 대상 기자를 찾을 수 없습니다."

            # 2. 후원자(`독자`)의 포인트 확인
            check_points_sql = """
            SELECT points 
            FROM MEMBER 
            WHERE memberID = %s 
            FOR UPDATE
            """
            self.db.cur.execute(check_points_sql, (reader_id,))
            result = self.db.cur.fetchone()

            if not result:
                return False, "사용자를 찾을 수 없습니다."

            current_points = result["points"]
            if current_points < amount:
                return False, "포인트가 부족합니다."

            # 3. 후원 정보 삽입
            donation_sql = """
            INSERT INTO DONATION (readerID, journalistID, amount, donation_date)
            VALUES (%s, %s, %s, NOW())
            """
            self.db.cur.execute(donation_sql, (reader_id, journalist_id, amount))

            # 4. 후원자(`a유저`)의 포인트 차감
            points_update_sql = """
            UPDATE MEMBER
            SET points = points - %s
            WHERE memberID = %s
            """
            self.db.cur.execute(points_update_sql, (amount, reader_id))

            # 5. 트랜잭션 확정
            self.db.conn.commit()
            return True, "후원에 성공했습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()  # 오류 발생 시 트랜잭션 롤백
            return False, "후원 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()

    # 특정 사용자가 후원한 기록 조회
    def get_donation_history(self, reader_id):
        try:
            sql = """
            SELECT 
                d.donationID, 
                d.journalistID, 
                m.username AS journalistName, 
                d.amount, 
                d.donation_date
            FROM 
                DONATION d
            JOIN 
                MEMBER m ON d.journalistID = m.memberID
            WHERE 
                d.readerID = %s
            ORDER BY 
                d.donation_date DESC
            """
            self.db.cur.execute(sql, (reader_id,))
            donations = self.db.cur.fetchall()

            if donations:
                return True, donations  # 후원 기록 반환
            else:
                return False, "후원 기록이 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "후원 기록 조회 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()

    # 특정 기자가 후원받은 기록 조회
    def get_received_donations(self, journalist_id):
        try:
            sql = """
            SELECT 
                d.donationID, 
                d.readerID, 
                m.username AS readerName, 
                d.amount, 
                d.donation_date
            FROM 
                DONATION d
            JOIN 
                MEMBER m ON d.readerID = m.memberID
            WHERE 
                d.journalistID = %s
            ORDER BY 
                d.donation_date DESC
            """
            self.db.cur.execute(sql, (journalist_id,))
            donations = self.db.cur.fetchall()

            if donations:
                return True, donations  # 후원받은 기록 반환
            else:
                return False, "후원받은 기록이 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "후원받은 기록 조회 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()

class Register:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 아이디, 비밀번호, 이름 저장하기
    # 회원가입
    def insert_member(self, username, password, email, role):
        try:
            # 비밀번호 해시화
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # SQL 쿼리
            sql = """
            INSERT INTO MEMBER (username, password, email, role, points)
            VALUES (%s, %s, %s, %s, 5000);
            """
            
            # 실행
            self.db.cur.execute(sql, (username, hashed_password.decode('utf-8'), email, role))
            # 변경 사항 저장
            self.db.conn.commit()
            return True  # 성공 시 True 반환
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False  # 실패 시 False 반환
        finally:
            self.db.DBClose()
    
class Login:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 아이디와 비밀번호와 일치하는 user가 있는지 확인하고, 있으면 user 정보 반환
    # 로그인시 비밀번호 검증
    def authenticate_member(self, email, password):
        try:
            # SQL 쿼리: username으로만 사용자 정보 가져오기
            sql = """
            SELECT memberID, username, email, role, points, password
            FROM MEMBER
            WHERE email = %s
            """
            
            # 데이터베이스에서 email로 사용자 정보 조회
            self.db.cur.execute(sql, (email,))
            user = self.db.cur.fetchone()

            # 사용자 존재 여부 확인
            if user is None:
                return False, "User not found"

            # 비밀번호 검증
            stored_password = user[5]  # DB에 저장된 해시된 비밀번호
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True, user  # 성공 시 True와 사용자 정보 반환
            else:
                return False, "Incorrect password"
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "Error occurred during authentication"
        finally:
            self.db.DBClose()
            '''
            호출 예시
            from post_list import Login;

            username = "test_user"
            password = "mypassword"

            login = Login()
            is_authenticated, result = login.authenticate_member(username, password)

            if is_authenticated:
            print("Authentication successful!") # 성공
            print("User Info:", result) # result에 user에 관한 정보 들어있어
            else:
            print("Authentication failed:", result) # 실패
            '''
    
class Subscribe:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기자 구독
    def subscribe_journalist(self, reader_id, journalist_id):
        try:
            sql = """
            INSERT INTO SUBSCRIPTION (readerID, journalistID)
            VALUES (%s, %s)
            """
            self.db.cur.execute(sql, (reader_id, journalist_id))
            self.db.conn.commit()
            return True  # 구독 성공
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()  # 에러 발생 시 롤백
            return False
        finally:
            self.db.DBClose()
    
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
    
    # 특정 사용자의 구독자 수 조회
    def get_subscriber_count(self, user_id):
        try:
            sql = """
            SELECT COUNT(subscriptionID) AS subscriberCount
            FROM SUBSCRIPTION
            WHERE journalistID = %s
            """
            self.db.cur.execute(sql, (user_id,))
            result = self.db.cur.fetchone()

            if result:
                return True, result["subscriberCount"]  # 구독자 수 반환
            else:
                return False, "해당 사용자의 구독자 수를 조회할 수 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "구독자 수 조회 실패"
        finally:
            self.db.DBClose()
    
    # 특정 사용자 구독 취소
    def cancel_subscription(self, reader_id, journalist_id):
        try:
            sql = """
            DELETE FROM SUBSCRIPTION
            WHERE readerID = %s AND journalistID = %s
            """
            # 구독 취소 실행
            rows_affected = self.db.cur.execute(sql, (reader_id, journalist_id))
            self.db.conn.commit()

            if rows_affected > 0:
                return True, "구독이 성공적으로 취소되었습니다."
            else:
                return False, "구독 취소 대상이 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()  # 오류 발생 시 트랜잭션 롤백
            return False, "구독 취소 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()

    # 특정 사용자가 구독한 사람 목록 조회
    def get_subscribed_users(self, user_id):
        try:
            sql = """
            SELECT m.memberID, m.username, m.email
            FROM MEMBER m
            JOIN SUBSCRIPTION s ON m.memberID = s.journalistID
            WHERE s.readerID = %s
            """
            self.db.cur.execute(sql, (user_id,))
            subscribed_users = self.db.cur.fetchall()

            if subscribed_users:
                return True, subscribed_users  # 구독한 사람 목록 반환
            else:
                return False, "구독한 사람이 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "구독 목록 조회 실패"
        finally:
            self.db.DBClose()

    # 특정 독자가 특정 기자를 구독했는지 여부 확인
    def is_subscribed(self, reader_id, journalist_id):
        try:
            sql = """
            SELECT COUNT(subscriptionID) AS isSubscribed
            FROM SUBSCRIPTION
            WHERE readerID = %s AND journalistID = %s
            """
            self.db.cur.execute(sql, (reader_id, journalist_id))
            result = self.db.cur.fetchone()

            if result and result["isSubscribed"] > 0:
                return True, "구독한 상태입니다."  # 구독 중
            else:
                return False, "구독하지 않았습니다."  # 미구독 상태
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "구독 여부 확인 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()
    
class Search:
    # 생성자'
    def __init__(self):
        self.db = Mysql_Model()
        
    # 기사 제목을 입력해 입력한 내용이 제목에 포함된 기사 반환
    def searchPost(self, input_title):
        try:
            sql = """
            SELECT articleID, title, content, category, created_at, views
            FROM ARTICLE
            WHERE title LIKE CONCAT('%', %s, '%')
            ORDER BY created_at DESC
            """
            self.db.cur.execute(sql, (input_title,))
            articles = self.db.cur.fetchall()

            if articles:
                return True, articles  # 검색된 기사 반환
            else:
                return False, "해당 제목을 포함한 기사가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "기사 검색 실패"
        finally:
            self.db.DBClose()

class Member:
    def __init__(self):
        self.db = Mysql_Model()

    #소셜 로그인 연결 (기존계정, 계정이 없다면 insert_member(self, username, password, email, role)로 먼저 백엔드에서 계정 만들고 연결지어줘야함)
    def save_social_login(self, member_id, provider, provider_id):
        try:
            # SQL 쿼리
            sql = """
            INSERT INTO SOCIAL_LOGIN (memberID, provider, providerID)
            VALUES (%s, %s, %s)
            """
            
            # 쿼리 실행
            self.db.cur.execute(sql, (member_id, provider, provider_id))
            # 변경 사항 저장
            self.db.conn.commit()
            return True  # 저장 성공 시 True 반환
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False  # 저장 실패 시 False 반환
        finally:
            self.db.DBClose()

    # 소셜로그인으로 member ID 조회
    def get_social_user(self, provider, provider_id):
        try:
            # SQL 쿼리
            sql = """
            SELECT memberID
            FROM SOCIAL_LOGIN
            WHERE provider = %s AND providerID = %s
            """
            
            # 쿼리 실행
            self.db.cur.execute(sql, (provider, provider_id))
            user = self.db.cur.fetchone()
            
            # 사용자 확인
            if user is not None:
                return True, user["memberID"]  # 사용자 존재 시 True와 memberID 반환
            else:
                return False, None  # 사용자 존재하지 않음
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, None  # 오류 발생 시 False 반환
        finally:
            self.db.DBClose()

    # 특정 User ID로 사용자 정보 조회
    def get_user_by_id(self, user_id):
        try:
            sql = """
            SELECT memberID, username, email, role, points
            FROM MEMBER
            WHERE memberID = %s
            """
            self.db.cur.execute(sql, (user_id,))
            user = self.db.cur.fetchone()

            if user:
                return True, user  # 사용자 정보 반환
            else:
                return False, "해당 User ID에 해당하는 사용자가 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "사용자 조회 중 오류가 발생했습니다."
        finally:
            self.db.DBClose()

class Comment:
    def __init__(self):
        self.db = Mysql_Model()  # 데이터베이스 연결 초기화

    #댓글 추가
    def add_comment(self, article_id, member_id, content):
        try:
            sql = """
            INSERT INTO COMMENT (articleID, memberID, content)
            VALUES (%s, %s, %s)
            """
            self.db.cur.execute(sql, (article_id, member_id, content))
            self.db.conn.commit()
            return True, "댓글 작성 성공"
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False, "댓글 작성 실패"
        finally:
            self.db.DBClose()


    # 댓글 삭제
    def delete_comment(self, comment_id, member_id):
        try:
            sql = """
            UPDATE COMMENT
            SET is_deleted = TRUE
            WHERE commentID = %s AND memberID = %s
            """
            rows_affected = self.db.cur.execute(sql, (comment_id, member_id))
            self.db.conn.commit()
            if rows_affected > 0:
                return True, "댓글 삭제 성공"
            else:
                return False, "댓글 삭제 실패: 권한 없음 또는 댓글 없음"
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False, "댓글 삭제 중 오류 발생"
        finally:
            self.db.DBClose()

    # 댓글 조회 (삭제된 댓글 표시)
    def get_comments_by_article(self, article_id):
        try:
            sql = """
            SELECT 
                c.commentID, 
                c.memberID, 
                c.content, 
                c.likes, 
                c.dislikes, 
                c.is_deleted, 
                c.created_at
            FROM 
                COMMENT c
            WHERE 
                c.articleID = %s
            ORDER BY 
                c.created_at ASC
            """
            self.db.cur.execute(sql, (article_id,))
            comments = self.db.cur.fetchall()

            # 삭제된 댓글을 처리하여 결과를 정리
            result = []
            for comment in comments:
                if comment['is_deleted']:
                    comment['content'] = "삭제된 댓글입니다."
                result.append(comment)

            if result:
                return True, result  # 댓글 목록 반환
            else:
                return False, "댓글이 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            return False, "댓글 조회 실패"
        finally:
            self.db.DBClose()

class LikeDislike:
    def __init__(self):
        self.db = Mysql_Model()

    # 1. 특정 유저가 특정 기사 좋아요 추가
    def add_article_like(self, article_id, member_id):
        return self._execute_reaction(
            table="ARTICLE_REACTION",
            target_id="articleID",
            id_value=article_id,
            member_id=member_id,
            is_like=True
        )

    # 2. 특정 유저가 특정 기사 싫어요 추가
    def add_article_dislike(self, article_id, member_id):
        return self._execute_reaction(
            table="ARTICLE_REACTION",
            target_id="articleID",
            id_value=article_id,
            member_id=member_id,
            is_like=False
        )

    # 3. 특정 유저가 특정 댓글 좋아요 추가
    def add_comment_like(self, comment_id, member_id):
        return self._execute_reaction(
            table="COMMENT_REACTION",
            target_id="commentID",
            id_value=comment_id,
            member_id=member_id,
            is_like=True
        )

    # 4. 특정 유저가 특정 댓글 싫어요 추가
    def add_comment_dislike(self, comment_id, member_id):
        return self._execute_reaction(
            table="COMMENT_REACTION",
            target_id="commentID",
            id_value=comment_id,
            member_id=member_id,
            is_like=False
        )

    # 5. 특정 유저가 특정 기사 좋아요 취소
    def remove_article_like(self, article_id, member_id):
        return self._remove_reaction(
            table="ARTICLE_REACTION",
            target_id="articleID",
            id_value=article_id,
            member_id=member_id,
            is_like=True
        )

    # 6. 특정 유저가 특정 기사 싫어요 취소
    def remove_article_dislike(self, article_id, member_id):
        return self._remove_reaction(
            table="ARTICLE_REACTION",
            target_id="articleID",
            id_value=article_id,
            member_id=member_id,
            is_like=False
        )

    # 7. 특정 유저가 특정 댓글 좋아요 취소
    def remove_comment_like(self, comment_id, member_id):
        return self._remove_reaction(
            table="COMMENT_REACTION",
            target_id="commentID",
            id_value=comment_id,
            member_id=member_id,
            is_like=True
        )

    # 8. 특정 유저가 특정 댓글 싫어요 취소
    def remove_comment_dislike(self, comment_id, member_id):
        return self._remove_reaction(
            table="COMMENT_REACTION",
            target_id="commentID",
            id_value=comment_id,
            member_id=member_id,
            is_like=False
        )

    # 내부: 좋아요/싫어요 추가 실행 (동시성 방지)
    def _execute_reaction(self, table, target_id, id_value, member_id, is_like, reaction_table):
        try:
            # 트랜잭션 시작
            self.db.conn.begin()

            # 1. 대상 행 잠금 (FOR UPDATE)
            lock_sql = f"""
            SELECT likes, dislikes
            FROM {table}
            WHERE {target_id} = %s
            FOR UPDATE
            """
            self.db.cur.execute(lock_sql, (id_value,))
            target = self.db.cur.fetchone()
            if not target:
                self.db.conn.rollback()
                return False, f"{table}에 해당하는 {target_id}가 존재하지 않습니다."

            # 2. 반응 추가 또는 업데이트
            reaction_sql = f"""
            INSERT INTO {reaction_table} ({target_id}, memberID, is_like, reaction_date)
            VALUES (%s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE is_like = %s, reaction_date = NOW()
            """
            self.db.cur.execute(reaction_sql, (id_value, member_id, is_like, is_like))

            # 3. 좋아요/싫어요 카운트 업데이트
            field = "likes" if is_like else "dislikes"
            update_sql = f"""
            UPDATE {table}
            SET {field} = {field} + 1
            WHERE {target_id} = %s
            """
            self.db.cur.execute(update_sql, (id_value,))

            # 트랜잭션 커밋
            self.db.conn.commit()
            return True, f"{'좋아요' if is_like else '싫어요'}가 성공적으로 추가되었습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False, "반응 추가 중 오류가 발생했습니다."

    # 내부: 좋아요/싫어요 취소 실행 (동시성 방지)
    def _remove_reaction(self, table, target_id, id_value, member_id, is_like, reaction_table):
        try:
            # 트랜잭션 시작
            self.db.conn.begin()

            # 1. 대상 행 잠금 (FOR UPDATE)
            lock_sql = f"""
            SELECT likes, dislikes
            FROM {table}
            WHERE {target_id} = %s
            FOR UPDATE
            """
            self.db.cur.execute(lock_sql, (id_value,))
            target = self.db.cur.fetchone()
            if not target:
                self.db.conn.rollback()
                return False, f"{table}에 해당하는 {target_id}가 존재하지 않습니다."

            # 2. 반응 삭제
            delete_sql = f"""
            DELETE FROM {reaction_table}
            WHERE {target_id} = %s AND memberID = %s AND is_like = %s
            """
            rows_affected = self.db.cur.execute(delete_sql, (id_value, member_id, is_like))

            if rows_affected > 0:
                # 3. 좋아요/싫어요 카운트 감소
                field = "likes" if is_like else "dislikes"
                update_sql = f"""
                UPDATE {table}
                SET {field} = {field} - 1
                WHERE {target_id} = %s
                """
                self.db.cur.execute(update_sql, (id_value,))

                # 트랜잭션 커밋
                self.db.conn.commit()
                return True, f"{'좋아요' if is_like else '싫어요'}가 성공적으로 취소되었습니다."
            else:
                self.db.conn.rollback()
                return False, "취소할 반응이 없습니다."
        except Exception as e:
            print(f"Error occurred: {e}")
            self.db.conn.rollback()
            return False, "반응 취소 중 오류가 발생했습니다."




            
