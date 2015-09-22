import simplejson as json
from models import *


def read_comments():
    comments_file = open('skuid_comments.json', mode='r')
    for line in comments_file.readlines():
        comment = json.loads(line)
        yield comment


def parse_count(product_summary, type_name):
    result = {
        'count': product_summary[type_name + 'Count'],
        'rate': product_summary[type_name + 'Rate'],
        'rate_show': product_summary[type_name + 'RateShow'],
        'rate_style': product_summary[type_name + 'RateStyle'],
    }
    return result


def parse_comment():
    index = 0
    for c in read_comments():
        p = c['productCommentSummary']
        try:
            product = Product.objects.get(skuid=p['skuId'])
        except DoesNotExist:
            product = Product(skuid=p['skuId'])
        product.show_count = p['showCount']
        product.comment_count = p['commentCount']
        product.score = [p['score%dCount' % s] for s in range(1, 6)]
        product.score_type = {
            'good': parse_count(p, 'good'),
            'general': parse_count(p, 'general'),
            'poor': parse_count(p, 'poor'),
        }
        product.save()
        for comment in c['comments']:
            custom = Custom(
                level=comment['userLevelId'],
                province=comment['userProvince'],
                name=comment['nickname']
            )
            custom.save()
            try:
                ref_id = int(comment['referenceId'])
            except ValueError:
                print('???' + comment['referenceId'])
                continue

            if ref_id != product.id:
                try:
                    p = Product.objects.get(skuid=ref_id)
                except DoesNotExist:
                    p = Product(skuid=ref_id)
                    p.save()
            else:
                p = product

            comment_instance = Comment(
                product=p,
                comment_id=comment['id'],
                content=comment['content'],
                score=comment['score'],
                useful_vote_count=comment['usefulVoteCount'],
                useless_vote_count=comment['uselessVoteCount'],
                custom=custom
            )
            comment_instance.save()
        index += 1
        print('Current Line:', index)

if __name__ == '__main__':
    parse_comment()
