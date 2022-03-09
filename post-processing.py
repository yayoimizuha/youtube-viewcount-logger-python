import datetime
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

from github import Github

credential = credentials.Certificate(json.loads(os.environ['FIREBASE_CREDENTIAL']))
firebase_admin.initialize_app(credential, {'storageBucket': 'gs://viewcount-logger-20043.appspot.com/'})
bucket = storage.bucket()
blob = bucket.blob(blob_name=str(str(datetime.datetime.now()) + '_log.txt'))
blob_url = ''
with open('out.txt', mode='r') as f:
    file = f.read()
    blob.upload_from_file(file_obj=file, content_type='text/plain')
    blob.make_public()
    blob_url = blob.public_url
    print(blob_url)

body_text = """{date}
[{url}]({url})
```
{content}
```""".format(date=str(datetime.datetime.now().isoformat()),
              content=file[len(file) - 30000:-1],
              url=blob_url)

gh = Github(os.environ['GITHUB_TOKEN'])
repo = gh.get_repo('yayoimizuha/youtube-viewcount-logger-python')

error_label = repo.get_label('error')
bug_label = repo.get_label('bug')
help_wanted_label = repo.get_label('help wanted')

if os.environ['DEBUG'] == 'YES':
    issue = repo.create_issue(title='Fetch debug log',
                              body=body_text, labels=[help_wanted_label])
else:
    issue = repo.create_issue(title='UP-FRONT YouTube View Counter GitHub Actions was failed',
                              body=body_text, labels=[error_label, bug_label])

print(issue)
bool('True')
