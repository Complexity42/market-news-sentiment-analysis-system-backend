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

    # def save_stock(self):
    #     doc_ref = self.db.collection(u'users').document(u'alovelace')
    #     doc_ref.set({
    #         u'first': u'Ada',
    #         u'last': u'Lovelace',
    #         u'born': 1815
    #     })

    #     doc_ref = self.db.collection(u'users').document(u'aturing')
    #     doc_ref.set({
    #         u'first': u'Alan',
    #         u'middle': u'Mathison',
    #         u'last': u'Turing',
    #         u'born': 1912
    #     })

          
    # def fetch_stock(self):
    #     users_ref = self.db.collection(u'news')
    #     docs = users_ref.stream()

    #     for doc in docs:
    #         print(doc.to_dict())

    def put_post(self,id,post):
        doc_ref = self.db.collection('News').document(id)
        doc_ref.set(post)