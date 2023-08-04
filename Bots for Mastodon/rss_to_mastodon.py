import feedparser #피드파서 모듈을 임포트해요
from mastodon import Mastodon #마스토돈 모듈을 임포트해요
import pymysql #MySQL 에 접속할 수 있도록 해줘요.

# Mastodon 을 설정해볼게요.
mastodon_base_url = 'https://pointless.chat' #인스턴스 URL을 적어주세요
mastodon_access_token = 'ACCESS_TOKEN_HERE' #엑세스 토큰을 넣어주세요
mastodon = Mastodon(access_token=mastodon_access_token, api_base_url=mastodon_base_url)

# MySQL 데이터베이스를 연결해볼께요
db_config = {
    'host': 'YOUR-DATABASE-HOST-HERE', #디비 호스트..
    'port': 5432, #디비 포트..
    'user': 'YOUR-MYSQL-USERNAME-HERE', #디비 유저네임..
    'password': 'YOUR-MYSQL-PASSWORD-HERE', #디비 패스워드..
    'database': 'YOUR-DB-NAME-HERE',  #디비 이름
}
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 테이블을 뿅 하고 만들어볼게요
create_table_query = """
CREATE TABLE IF NOT EXISTS 테이블이름 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    posted_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
cursor.execute(create_table_query)

# RSS 피드 URL을 설정해볼게요.
rss_feed_url = 'http://example.com'

# 피드를 읽어들여볼게요.
feed = feedparser.parse(rss_feed_url)

# 마스토돈에 올려볼게요.
def post_to_mastodon(title, url):
    try:
        # 먼저 중복 포스팅인지 아닌지 확인을 해봐야겠죠?
        query = "SELECT * FROM 테이블이름 WHERE title = %s"
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        
        if not result:
            # 중복이 아니라면 Mastodon에 포스팅 (공개범위: 미등재)
            mastodon.status_post(f"{title}\n{url}", visibility="unlisted")
            
            # 포스팅한 항목 데이터베이스에 추가
            insert_query = "INSERT INTO 테이블이름 (title, url) VALUES (%s, %s)"
            cursor.execute(insert_query, (title, url))
            conn.commit()
    except Exception as e:
        print(f"오류! 오늘 약 드셨어요? : {e}")

#피드에서 제목과 링크를 뽑아볼게요
for entry in feed.entries:
    title = entry.get('title')
    url = entry.get('link')
    
    # 올려볼게요
    post_to_mastodon(title, url)

#MySQL 데이터베이스와의 연결을 종료할게요
cursor.close()
conn.close()