import requests
import simplejson as json
import time
import random

base_url = r'http://s.club.jd.com/productpage/p-%s-s-0-t-0-p-%d.html'
results = open('skuid_comments.json', mode='w')
skuid_file = open('skuids.txt', mode='r')
user_agents_file = open('uas.txt', mode='r')
ua_list = [x.strip() for x in user_agents_file.readlines()]

for skuid_str in skuid_file.readlines():
    skuid = skuid_str.strip()
    print('Current Skuid:', skuid)
    page = 0
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
                exit(0)
        if not comments_json.text:
            break
        comments = json.loads(comments_json.text)
        if len(comments['comments']):
            results.write(comments_json.text + '\n')
            page += 1
            print('Page: ', page)
        else:
            break
