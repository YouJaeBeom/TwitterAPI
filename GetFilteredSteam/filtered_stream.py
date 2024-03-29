import requests
import os
import json
from kafka import KafkaProducer
from urllib3.exceptions import ProtocolError
#bearer_token = os.environ.get("BEARER_TOKEN")
#bearer_token = "AAAAAAAAAAAAAAAAAAAAAIYXGwEAAAAAaUcaAMc88Bjx9WRz%2BPzYRs6Co%2Bs%3DaLg9uUg5IbJ0F3CM7ivoKacwqqBwIaIsYe5xw4qdkykGh7Tmje"
#bearer_token = "AAAAAAAAAAAAAAAAAAAAAIYXGwEAAAAA5y3mcPIze5%2BxhqNL0JwDHSUiI%2Fc%3DxSMxCUqFLcqCOYNht5PuwF6txgznmldEjaJtB7keCOZGyA5wSx"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHyhPwEAAAAALKrI0h1Ct2Cz2Zupaym%2FlW4xd6U%3D1m5Gemz9PsV2bba7CA0Pn2A2R3SpZgzGS41EMhDW63zD2Bzvz6"
#bearer_token = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

#bearer_token ="AAAAAAAAAAAAAAAAAAAAAGiFPQEAAAAAu7suubjKWeoDZ6WJnyn%2Bw%2BvzsTQ%3DOwureac7DLPKKfzomS4aIkZrvIMsiIseiYGM35NjLrG0DW908X"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = "Bearer {}".format(bearer_token)
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": 'russia -is:retweet'},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    producer = KafkaProducer(acks=0, compression_type='gzip', api_version=(0, 10, 1), bootstrap_servers=['117.17.189.205:9092','117.17.189.205:9093','117.17.189.205:9094'])

    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at&expansions=referenced_tweets.id", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            try:
                refer=json_response['data']['referenced_tweets'][0]['type']
                print(refer,type(refer))
            except Exception as ex :
                print(ex)
                pass 
            producer.send("tweet_api", json.dumps(json_response).encode('utf-8'))
            producer.flush()
            print(json_response)
            #print(json.dumps(json_response, sort_keys=True))


def main():
    while True:
        try:
            rules = get_rules()
            delete = delete_all_rules(rules)
            set = set_rules(delete)
            get_stream(set)
        except Exception as es:
            print("retry")
            continue


if __name__ == "__main__":
    main()
