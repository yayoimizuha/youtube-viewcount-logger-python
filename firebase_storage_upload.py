import datetime
import json
import os
import firebase_admin
from firebase_admin import credentials, storage


def upload_log():
    credential = credentials.Certificate(json.loads(os.environ['FIREBASE_CREDENTIAL']))
    firebase_admin.initialize_app(credential, {'storageBucket': 'viewcount-logger-20043.appspot.com'})
    bucket = storage.bucket()
    blob = bucket.blob(blob_name=str(str(datetime.datetime.now()) + '_log.txt'))
    blob_url = ''
    with open('out.txt', mode='rb') as f:
        blob.upload_from_file(file_obj=f, content_type='text/plain')
        blob.make_public()
        blob_url = blob.public_url
        print(blob_url)
    return blob_url
