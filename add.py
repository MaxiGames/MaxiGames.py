import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey2.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection(u'servers').stream()
for doc in docs:
    data = doc.to_dict()
    data['giveaways'] = []
    db.collection(u'servers').document(doc.id).set(data)