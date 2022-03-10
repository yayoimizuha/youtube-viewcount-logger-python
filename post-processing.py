import datetime
import os
from github import Github
import firebase_storage_upload

blob_url = firebase_storage_upload.upload_log()

with open('out.txt', mode='r') as f:
    file = f.read()

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
