import re
import requests

base_url = r'http://list.jd.com/list.html?cat=670,671,672%s'
page = r'&page=%d'

skuids = set()
first_try = requests.get(base_url)
sku_re = re.compile(r'data-sku="(\d+)"', re.MULTILINE | re.IGNORECASE)
ids = re.findall(sku_re, first_try.text)
print(ids)
print('find...', len(ids))
skuids |= set(ids)

i = 2
while True:
    url = base_url % (page % i)
    html = requests.get(url)
    ids = set(re.findall(sku_re, html.text))
    if i == 193 or len(ids) == 0 or len(skuids - ids) == 0:
        break
    else:
        i += 1
    skuids |= set(ids)
    total = len(skuids)
    print('Total:', total)

with open('skuids.txt', mode='w') as s:
    for sku in skuids:
        s.write(sku + '\n')
