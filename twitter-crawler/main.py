import requests
import json
from secret import getSecret
from firebase_connection import FireBaseClass

payload={}
headers = getSecret()

db = FireBaseClass()

def fetch_by_id(id,savePost=False):
    ids = "ids="+id
    tweet_fields = "tweet.fields=id,author_id,text,source,created_at"
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)
    if savePost:
        save(id,parse_post(response))
    return parse_post(response)

def parse_post(raw_post):
    # print('TEST',raw_post)
    post = raw_post['data'][0]
    url = 'https://twitter.com/' + post['author_id'] + '/status/' + post['id']
    return {
        # 'id' : post['id'],
        'title' : 'Elon Musk on Twitter',
        'content' : post['text'],
        # 'source_name' : post['source'],
        'source_name' : 'Twitter',
        'keywords' : ['Twitter'],
        'source_url' : url,
        'source_date' : post['created_at'], 
    }

def fetch_by_account(from_account):

    base_url = "https://api.twitter.com/2/tweets/search/recent?max_results=100&query=from:"
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
    # fetch_by_account('ElonMusk')
    list = [
        1382552587099062272,
        1382858937792307202,1382879908645392384,
        1382539825421582339,
        1382540937700671488,
        1383103246470811652,
        1284291528328790016,
        1383177151541743621,
        1410529698497630212,
        1410519466518233089,
    ]
    for id in list:
        fetch_by_id(str(id),True)