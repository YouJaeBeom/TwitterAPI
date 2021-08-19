import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
#bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = "AAAAAAAAAAAAAAAAAAAAAIYXGwEAAAAAaUcaAMc88Bjx9WRz%2BPzYRs6Co%2Bs%3DaLg9uUg5IbJ0F3CM7ivoKacwqqBwIaIsYe5xw4qdkykGh7Tmje"

def create_getuserid_url(user_name):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=TwitterDev,TwitterAPI"
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

def connect_to_getuserid_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_userid(user_name):
    user_name = user_name
    url = create_getuserid_url(user_name)
    json_response = connect_to_getuserid_endpoint(url)

    user_id = json_response['user_id']
    return user_id

def create_url(user_id):
    # Replace with user ID below
    user_id = user_id
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = "Bearer {}".format(bearer_token)
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    
    with open('list.txt', 'r') as f:
        userlist = f.read().split(',')
        for user_name in userlist:
            user_id = get_userid(user_name)
            url = create_url(user_id)
            params = get_params()
            json_response = connect_to_endpoint(url, params)
            print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
