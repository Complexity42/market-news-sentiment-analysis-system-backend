import requests
import json
from secret import getSecret
from firebase_connection import FireBaseClass

payload={}
headers = getSecret()

db = FireBaseClass()

def fetch_by_account(from_account):
    def fetch_by_id(id):
        ids = "ids="+id
        tweet_fields = "tweet.fields=id,text,source,created_at"
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        return parse_post(response)

    def parse_post(raw_post):
        # print('TEST',raw_post)
        post = raw_post['data'][0]
        url = 'https://twitter.com/' + from_account + '/status/1487119404382961664'
        return {
            # 'id' : post['id'],
            'title' : post['text'],
            'content' : post['text'],
            # 'source_name' : post['source'],
            'source_name' : 'Twitter',
            'keywords' : ['Twitter'],
            'source_url' : url,
            'source_date' : post['created_at'], 
        }

    base_url = "https://api.twitter.com/2/tweets/search/recent?query=from:"
    url = base_url + from_account
    response = requests.request("GET", url, headers=headers, data=payload)
    parsed_response = json.loads(response.text)
    data = parsed_response['data']
    for raw_post in data:
        id = raw_post['id']
        res = fetch_by_id(id)
        save(id,res)


def save(id,data):
    db.put_post(id,data)

if __name__ == "__main__":
    fetch_by_account('ElonMusk')