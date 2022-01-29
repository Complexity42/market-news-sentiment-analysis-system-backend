import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FireBaseClass:

    def __init__(self):
        self.db = None
        self.setup()
    
    def setup(self):
        # Use a service account
        cred = credentials.Certificate('secret.json')
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()  

    def fetch_news(self):
        users_ref = self.db.collection('News')
        docs = users_ref.stream()

        res = []

        for doc in docs:
            id = doc.id
            doc = doc.to_dict()
            doc['id'] = id
            res.append(doc)

        # print(res)
        return res

    def save_result(self, id, score):
        # doc_ref = self.db.collection(u'users').document(u'alovelace')
        # doc_ref.set({
        #     u'first': u'Ada',
        #     u'last': u'Lovelace',
        #     u'born': 1815
        # })

        # doc_ref = self.db.collection(u'users').document(u'aturing')
        # doc_ref.set({
        #     u'first': u'Alan',
        #     u'middle': u'Mathison',
        #     u'last': u'Turing',
        #     u'born': 1912
        # })
        # print(news)
        col_ref = self.db.collection('Sentiment_Analysis_Result').document(id)
        col_ref.set(
            {
            #   sentiment_analysis_result
            # - method_name
            # - news_id
            # - score
            # - created_at
            # - updated_at
                'news_id' : id,
                'score' : score,
                'is_positive' : score>0,
            }
        )