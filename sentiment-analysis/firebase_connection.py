import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from classification import classify_topic
class FireBaseClass:

    def __init__(self):
        self.db = None
        self.setup()
    
    def setup(self):
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

        return res

    def save_result(self, id, score):
        doc_ref = self.db.collection('Sentiment_Analysis_Result').document(id)
        doc_ref.set(
            {
                'news_id' : id,
                'score' : score,
                'is_positive' : score>0,
            }
        )

    def update_classification(self):
        col_ref = self.db.collection('News')
        for doc_ref in col_ref.get():
            id = doc_ref.id
            doc = doc_ref.to_dict()
            if len(doc['keywords']) == 0:
                doc['keywords'] = [classify_topic(doc['content'])]
            # col_ref.document(id).set(doc)
