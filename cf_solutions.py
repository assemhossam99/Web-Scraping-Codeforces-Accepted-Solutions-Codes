import time
import os
from bs4 import BeautifulSoup
import requests

username = input('please enter your codeforces user name (handle): ')
finished_ids = set()
inf = 10000000
done = False
if not os.path.isdir('solutions'):
    os.makedirs('solutions')
for page in range(1, inf):
    print(f'page {page} starts...')
    if done:
        break
    html = requests.get(f'https://codeforces.com/submissions/{username}/page/{page}').text
    soup = BeautifulSoup(html, 'lxml')
    submissions = soup.find_all('td')
    contest_gym = 0
    submission_id = ''
    language = ''
    status = ''
    problem_name = ''
    for idx, submission in enumerate(submissions):
        if idx % 8 == 0:
            submission_id = submission.text
            if submission_id in finished_ids:
                done = True
                break
            finished_ids.add(submission_id)
        elif idx % 8 == 3:
            problem = str(submission.a['href'])
            problem_name = submission.text
            while not problem[-1].isdigit() or len(problem) > 20:
                problem = problem[:-1]
            if problem[1] == 'c':
                contest_gym = 0
            else:
                contest_gym = 1
        elif idx % 8 == 4:
            language = submission.text
        elif idx % 8 == 5:
            status = submission.text
            if 'Accepted' in status and contest_gym == 0:
                print(problem_name.strip())
                code = 'archive-name.zip'
                while 'archive-name.zip' in code:
                    code_link = requests.get(f'https://codeforces.com{problem}/submission/{submission_id.strip()}').text
                    newSoup = BeautifulSoup(code_link, 'lxml')
                    code = newSoup.find('pre')
                    if 'archive-name.zip' in code:
                        print('please wait..')
                        time.sleep(300)
                if code == None:
                    continue
                code = code.text
                print(submission_id.strip())
                ex = ''
                if '++' in language:
                    ex = 'cpp'
                elif 'Py' in language:
                    ex = 'py'
                elif '#' in language:
                    ex = 'cs'
                elif 'Java' in language:
                    ex = 'java'
                problem_name = problem_name.strip()
                letter = problem_name[0]
                problem_name = ''.join(ch for ch in problem_name if ch.isalnum())
                problem_name = problem_name[1:]
                problem_name = letter + '-' + problem_name
                print(problem_name)
                with open(f'solutions/{problem_name.strip()}.{ex}', 'w') as f:
                    f.write(code)
                print(f'problem [{problem_name.strip()}] saved successfully.')
                print('')
                time.sleep(5)