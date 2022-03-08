import datetime
import os

from github import Github

with open('out.txt', mode='r') as f:
    file = f.read()

body_text = """{date}
```
{content}
```""".format(date=str(datetime.datetime.now().isoformat()),
              content=file)

gh = Github(os.environ['GITHUB_TOKEN'])
repo = gh.get_repo('yayoimizuha/youtube-viewcount-logger-python')

error_label = repo.get_label('error')
bug_label = repo.get_label('bug')
help_wanted_label = repo.get_label('help wanted')

if os.environ['DEBUG'] == 'True':
    issue = repo.create_issue(title='Fetch debug log',
                              body=body_text, labels=[help_wanted_label])
else:
    issue = repo.create_issue(title='UP-FRONT YouTube View Counter GitHub Actions was failed',
                              body=body_text, labels=[error_label, bug_label])

print(issue)
