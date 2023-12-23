# 만나서 반가워요! 저는 이 간단한 파이썬 코드를 만든 네이티브에요.
# 저는 포인트리스에 서식하고있어요. https://pointless.chat/@Native

# 이 코드는 Creative Commons CC-BY-SA-NC 4.0 라이선스를 따라요.
# 라이선스에 대한 자세한 정보는 다음 링크에서 찾아보실 수 있어요.
# https://creativecommons.org/licenses/by-nc-sa/4.0/

# 그럼, 즐거운 삐삐쀼쀼 시간을 가져볼까요?
# 이 코드는 RSS 피드를 가져와서 Mastodon 인스턴스에 게시해요.

# 시작해봅시다! 먼저 필요한 라이브러리를 가져올게요. 슝~
import requests
from bs4 import BeautifulSoup
from mastodon import Mastodon
import time
import json
import lxml

# 뉴스를 퍼오는 곳을 여기에 적어주세요. RSS 피드를 사용할 수 있어요.
rss_url = "YOUR_RSS_URL_HERE"

# Mastodon 인스턴스에 로그인할게요.
# mastodon_url 에 인스턴스 주소를 적어주세요! 예를들어, Pointless.chat 같이..
# client_id 에 Mastodon 개발자 설정에서 만든 값을 적어주세요.
# client_secret 에 Mastodon 개발자 설정에서 만든 값을 적어주세요. 쉿! 이건 비밀이니 공유하지 마세요!
# 실수로 공유했다가는 대참사가 벌어질 것이에요.
# access_token 에 Mastodon 개발자 설정에서 만든 값을 적어주세요. 이것도 비밀이니 공유하지 마세요!
# 이것도 실수로 공유했다가는 대참사가 벌어질 것이에요. 알겠죠?
mastodon_url = "https://pointless.chat"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
access_token = "YOUR_ACCESS_TOKEN"

# URL 단축 API 의 엔드포인트에요! 이 코드에서는 krll.me 를 사용해요.
shorten_url_api = "https://krll.me/api/urls"

# 우리는 중복으로 툿을 날리는 것을 방지하기 위해 간단한 json 파일에 발송한 툿 내용을 기록할거에요.
# 시스템의 json 파일 경로를 posts.json에 적어주세요!
# 만약 json 파일이 없다면 오류를 뱉어낼 것이에요. 하지만 괜찮아요. nano 같은 에디터로 빈 json 파일을 만들어주세요.
# 이걸 읽고 있으면 그정도는 할 수 있겠죠?
json_file = "posts.json"

# URL을 단축해볼게요. krll.me 를 사용할거에요.
# krll.me 의 API 문서는 다음 링크를 참고해주세요: https://krll.me/docs
def shorten_url(url):
    response = requests.post(shorten_url_api, json={"url": url})
    if response.status_code == 200:
        key = response.json()["key"]
        return f"https://krll.me/{key}"
    else:
        return url

# RSS 피드를 긁어긁어 긁어볼까요?
# 이 코드는 RSS 피드의 URL을 가져와서 제목과 링크를 가져와요.
response = requests.get(rss_url)
soup = BeautifulSoup(response.content, "lxml-xml")
items = soup.find_all("item")

# Mastodon 서버에 로그인할게요. 위에서 적어둔 정보를 사용할거에요.
mastodon = Mastodon(
    client_id = client_id,
    client_secret = client_secret,
    access_token = access_token,
    api_base_url = mastodon_url
)

# 중복 툿 방지를 위해 json 파일을 읽어올게요.
try:
    with open(json_file, "r") as f:
        posts = json.load(f)
except FileNotFoundError:
    posts = []

# RSS 피드를 가공해볼까요? 여기는 포인트리스 뻘글 공장이니까요.
for item in items:
    title = item.title.text
    link = item.link.text

    # 링크만 가져올꺼니 SSL 인증을 비활성화 할게요.
    session = requests.Session()
    session.verify = False

    # 최종 목적지 URL을 가져올게요.
    try:
        response = session.get(link, allow_redirects=True)
        redirected_url = response.url
    except requests.exceptions.SSLError:
        print("SSL 검증에 실패했어요.")
        redirected_url = link

    # 최종 목적지 URL을 단축해볼게요.
    shortened_url = shorten_url(redirected_url)

    # 게시글을 보낼까요?
if shortened_url not in posts:
    # Mastodon 에 공개범위 미등재로 게시할게요.
    mastodon.status_post(f"{title}\n{shortened_url}", visibility='unlisted')
    posts.append(shortened_url)

    # JSON 파일이 무한 증식하는 것을 방지하기 위해, 3000개 이상의 게시글을 기록하면 가장 오래된 게시글을 지울게요.
    if len(posts) > 3000:
        posts.pop(0)

    # 게시글 URL을 JSON 파일에 저장해요.
    with open(json_file, "w") as f:
        json.dump(posts, f)
        
# 끝났어요! 마지막으로 봇이 (거의) 실시간으로 정보를 마스토돈으로 보내기 위해 crontab 을 설정하는것을 잊지 말아주세요.
# 제 부족한 코드를 봐주셔서 감사해요!
