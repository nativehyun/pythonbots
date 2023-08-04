import mastodon as Mastodon #마스토돈 모듈을 임포트해요
import json #json 파일로 중복 부스트를 방지할게요

def load_boosted_toots():
    try:
        with open("boosted_toots.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_boosted_toots(boosted_toots):
    with open("/home/json 파일 경로", "w") as file:
        json.dump(boosted_toots, file)

def boost_new_toots(api, boosted_toots):
    timeline = api.timeline_hashtag("툿친소")
    for toot in timeline:
        if toot["id"] not in boosted_toots:
            api.status_reblog(toot["id"]) #API에서는 부스트가 아닌 리블로그임에 주의하세요
            boosted_toots.append(toot["id"])

    # 데이터가 무한 증식하지 않도록 json 파일에 저장하는 툿 개수를 100개로 제한할게요.
    boosted_toots = boosted_toots[-100:]
    save_boosted_toots(boosted_toots)

def main():
    instance_url = "https://pointless.chat"  # 인스턴스 주소로 바꿔주세요
    access_token = "YOUR-ACCESS-TOKEN-HERE"  # 엑세스 토큰을 넣어주세요

    mastodon = Mastodon.Mastodon(
        access_token=access_token,
        api_base_url=instance_url
    )

    boosted_toots = load_boosted_toots()
    boost_new_toots(mastodon, boosted_toots)

if __name__ == "__main__":
    main()
