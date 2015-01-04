import urllib
import json
import time

from plot_statistics import plotify


MAX_SUBS = 1000000
MAX_CF_CONTEST_ID = 600
MAGIC_START_POINT = 17000

SUBMISSION_URL = 'http://codeforces.com/api/contest.status?contestId={contestId}&handle={handle}&from=1&count={count}'
USER_RATING_URL = 'http://codeforces.com/api/user.rating?handle={handle}'
CONTEST_URL = 'http://codeforces.com/contest/{contestId}'
PROBLEM_URL = 'http://codeforces.com/contest/{contestId}/problem/{index}'
PROBLEM_TAG = 'data-problem-name'
SPAN_CLASS =  '<span class="tag-box"'

def get_problems_amount(con_id):
    resp = urllib.urlopen(CONTEST_URL.format(contestId=con_id)).read()
    return resp.count(PROBLEM_TAG) - 2 # 2 extra

def get_tags(con_id, prob_id):
    resp = urllib.urlopen(PROBLEM_URL.format(contestId=con_id, index=prob_id)).read()
    start_pos = resp.find(SPAN_CLASS)
    tags = []
    while start_pos > -1:
        start_pos = resp.find('>', start_pos) + 1
        end_pos = resp.find('<', start_pos)
        tags.append(resp[start_pos:end_pos].strip())
        start_pos = resp.find(SPAN_CLASS, end_pos)
    return tags

handle = 'tacklemore'
user_rating_info = urllib.urlopen(USER_RATING_URL.format(handle=handle)).read()
dic = json.loads(user_rating_info)
if dic['status'] != u'OK':
    print 'Oops.. Something went wrong...'
    exit(0)

rated_contests = dic['result']
start_time = time.time()

popular_tags = ['data structures', 'dp', 'combinatorics', 'trees', 'greedy', 'two pointers', 'binary search', 'hashing', 'number theory']
popular_tags_output = ['data\nstructures', 'dp', 'combi\nnatorics', 'trees', 'greedy', 'two\npointers', 'binary\nsearch', 'hashing', 'number\ntheory']
probs_solved = {key: 0 for key in popular_tags}
probs_failed = {key: 0 for key in popular_tags}

for rated_contest in rated_contests:
    con_id = rated_contest['contestId']
    submissions_info = urllib.urlopen(SUBMISSION_URL.format(contestId=con_id, handle=handle, count=MAX_SUBS)).read()
    #print SUBMISSION_URL.format(contestId=con_id, handle=handle, count=MAX_SUBS)
    dic = json.loads(submissions_info)
    
    if dic['status'] != u'OK':
        print 'Oops.. Something went wrong...'
        exit(0)

    submissions = dic['result']
    solved = set()
    
    for submission in submissions:
        if submission['author']['participantType'] == u'CONTESTANT' and submission['verdict'] == u'OK' and \
                                                        submission['problem']['index'] not in solved:
            solved.add(submission['problem']['index'])
            tags = submission['problem']['tags']
            for tag in tags:
                if tag in popular_tags:
                    probs_solved[tag] += 1

    prob_amo = get_problems_amount(con_id)
    prob_list = [chr(65 + i) for i in range(prob_amo)] # 65 is ASCII code of A
    for prob_index in prob_list:
        if prob_index not in solved:
            tags = get_tags(con_id, prob_index)
            for tag in tags:
                if tag in popular_tags:
                    probs_failed[tag] += 1

plotify(popular_tags_output, [probs_solved[key] for key in popular_tags], \
                [probs_failed[key] for key in popular_tags], handle)

for key in popular_tags:
    print key + ': ' + str(probs_solved[key]) + ' ' + str(probs_failed[key])

end_time = time.time()
print 'Execution time %d seconds' % int(end_time - start_time)
