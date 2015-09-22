import requests
import simplejson as json
import time
import random

base_url = r'http://s.club.jd.com/productpage/p-%s-s-0-t-0-p-%d.html'
results = open('skuid_comments.json', mode='a')
skuid_file = open('skuids.txt', mode='r')
user_agents_file = open('uas.txt', mode='r')
current_progress = open('progress', mode='r')
progress = current_progress.read()
current_skuid = None
current_page = None
if progress:
    current_skuid = progress.strip().split(' ')[0].strip()
    current_page = progress.strip().split(' ')[1].strip()
ua_list = [x.strip() for x in user_agents_file.readlines()]

for skuid_str in skuid_file.readlines():
    if current_skuid:
        if skuid_str.strip() != current_skuid:
            continue
        page = int(current_page)
        current_skuid = None
        current_page = None
    else:
        page = 0
    skuid = skuid_str.strip()
    print('Current Skuid:', skuid)
    while True:
        sec = random.randint(1, 4)
        time.sleep(sec)
        ua = random.choice(ua_list)
        try:
            comments_json = requests.get(base_url % (skuid, page), headers={'User-Agent': ua})
            print(comments_json.request.headers)
        except:
            with open('progress', mode='w') as p:
                p.write(skuid + ' ' + str(page))
            time.sleep(180)
            continue
        if not comments_json.text:
            break
        comments = json.loads(comments_json.text)
        if len(comments['comments']):
            results.write(comments_json.text + '\n')
            page += 1
            print('Page: ', page)
        else:
            break
