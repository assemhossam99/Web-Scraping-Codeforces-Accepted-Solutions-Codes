import time
import os
from bs4 import BeautifulSoup
import requests

username = input('please enter your codeforces user name (handle): ')
finished_ids = set()
inf = 10000000
done = False
savedProblems = 0
wait_cnt = 0
if not os.path.isdir(f'{username}\'s solutions'):
    os.makedirs(f'{username}\'s solutions')
for page in range(1, inf):
    print(f'page {page} starts...')
    print(' ')
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
    problem_number = ''
    for idx, submission in enumerate(submissions):
        if idx % 8 == 0:
            submission_id = submission.text
            if submission_id in finished_ids:
                done = True
                break
            finished_ids.add(submission_id)
        elif idx % 8 == 3:
            problem_number = ''
            problem = str(submission.a['href'])
            problem_name = submission.text
            if problem[1] == 'c':
                contest_gym = 0
            else:
                contest_gym = 1
                continue
            while not problem[-1].isdigit() or len(problem) > 20:
                problem = problem[:-1]
            for c in problem:
                if c >= '0' and c <= '9':
                    problem_number += c
        elif idx % 8 == 4:
            language = submission.text
        elif idx % 8 == 5:
            wait_cnt = 0
            status = submission.text
            if 'Accepted' in status and contest_gym == 0:
                print(problem_name.strip())
                code = 'archive-name.zip'
                while 'archive-name.zip' in code:
                    code_link = requests.get(f'https://codeforces.com{problem}/submission/{submission_id.strip()}').text
                    newSoup = BeautifulSoup(code_link, 'lxml')
                    code = newSoup.find('pre').text
                    if code == None:
                        code = 'archive-name.zip'
                        continue
                    if 'archive-name.zip' in code:
                        if wait_cnt == 2:
                            print(f'could not save problem {problem_name}.')
                            print('')
                            break
                        print('please wait..')
                        time.sleep(300)
                        wait_cnt += 1
                if code == None or 'archive-name.zip' in code:
                    continue
                print(submission_id.strip())
                ex = 'txt'
                if '++' in language:
                    ex = 'cpp'
                elif 'Py' in language:
                    ex = 'py'
                elif '#' in language:
                    ex = 'cs'
                elif 'Java' in language:
                    ex = 'java'
                problem_name = problem_name.strip()
                letter = problem_number + problem_name[0]
                problem_name = ''.join(ch for ch in problem_name if ch.isalnum())
                problem_name = problem_name[1:]
                problem_name = letter + '-' + problem_name
                print(problem_name)
                with open(f'{username}\'s solutions/{problem_name.strip()}.{ex}', 'w') as f:
                    f.write(code)
                savedProblems = savedProblems + 1
                print(f'problem [{problem_name.strip()}] saved successfully. {savedProblems} problems were saved successfully.')
                print('')
                time.sleep(5)
