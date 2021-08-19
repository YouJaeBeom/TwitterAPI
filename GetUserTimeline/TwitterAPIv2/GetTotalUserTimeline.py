from requests_oauthlib import OAuth1Session
import json
import time

class TwitterAPIs:

    """
    Response formats	JSON
    Requires authentication?	Yes
    Rate limited?	Yes
    Requests / 15-min window (user auth)	900
    Requests / 15-min window (app auth)	1500
    Requests / 24-hour window	100,000

    """

    def __init__(self):
        self.consumer_key = '25nwDEFygPN4JrONW52ZRpbkj'
        self.consumer_secret = '6rcUXU84Mk4Bi4Gp2HTyXR8uJOLDapkKvLvyiNCxNRP7075drq'
        self.access_token = '1067071463948148736-C3uNvuBgvZ8p83QE8hDv4kONZM593k'
        self.access_token_secret= 'jBaKhsuXhj1C3SDHFWozubyXoEDQPqw8oWFqaSD5Qi31M'

        self.twitter = OAuth1Session(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)

    def twitterapis_crawling(self):
        with open('list.txt', 'r') as f:
            accounts = f.read().split(',')
            for screen_name in accounts:
                ## timeline get
                url = 'https://api.twitter.com/1.1/statuses/user_timeline.json' #트윗
                ## parameter setting
                params = {'screen_name':screen_name, 'count':'1'}
                ## 하나의 트윗만 수집한 후 max_id get
                res = self.twitter.get(url, params = params)
                l = json.loads(res.text)
                max_id = l[0]['id']

                ## other setting
                start = time.time()
                count = 0
                tweet_list = []

                ## 트윗 저장 file setting
                file_path = "./tweet_0521/" + screen_name + ".json"
                with open(file_path, 'w') as outfile:
                    while(True):
                        ## parameter setting
                        params = {'screen_name':screen_name, 'count':'200', 'max_id':max_id}

                        ## 200개씩 트윗 수집
                        res = self.twitter.get(url, params = params)
                        time.sleep(1)
                        l = json.loads(res.text)
                        for tweet in l:
                            count = count + 1
                            id = tweet['id']
                            outfile.write(str(tweet)+"\n")
                            tweet_list.append(str(id)+str(tweet['text'])+str(tweet['created_at']))
                            print(count,"============",str(tweet['created_at']),tweet['text'])
                        ## 마지막 트윗이 이전 마지막 트윗과 다른 경우
                        ## 더 크롤링할 트윗이 존재한다. --> 한번 더
                        if(max_id != id):
                            max_id = id
                        ## 마지막 트윗이 이전 마지막 트윗과 같은경우
                        ## 더 이상 크롤링할 트윗이 존재하지 않는다. --> 종료
                        else:
                            print(len(tweet_list),"==",len(set(tweet_list)))
                            print("time :", time.time() - start)
                            break

if __name__ == '__main__':
    twitterapis = TwitterAPIs()
    twitterapis.twitterapis_crawling()
