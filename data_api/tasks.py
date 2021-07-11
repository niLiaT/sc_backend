from celery import shared_task
import requests
from bs4 import BeautifulSoup
import re
from calendar import month_abbr
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import User, Article, Comment, CommonComment

def new_session():
    ses = requests.Session()
    ses.post('https://www.ptt.cc/ask/over18',
             data={'from': '/bbs/Gossiping/index.html', 'yes': 'yes'})

    return ses

def get_trending(session, date):
    date = date.strftime(' %m/%d').replace(' 0', ' ')
    result = {
        '爆': [],
        'XX': []
    }

    url = 'https://www.ptt.cc/bbs/Gossiping/search?'
    params = {
        'page': '1',
        'q': 'recommend:100'
    }
    flag = True
    while flag == True:
        res = session.get(url, params=params)
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = soup.find_all('div', {'class': 'r-ent'})
        for article in articles:
            if article.findNext('div', {'class': 'date'}).text == date:
                flag = False
                break
            try:
                result[article.span.text].append(
                    'https://www.ptt.cc' + article.div.find_next_sibling().a['href'])
            except:
                pass

        params['page'] = str(int(params['page']) + 1)
        if flag == False and params['q'] == 'recommend:100':
            flag = True
            params['page'] = '1'
            params['q'] = 'recommend:-100'

    return result

def dump_article(session, url):
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    info_list = []
    push_list = []
    article = {
        'original_poster': '',
        'board': '',
        'title': '',
        'date': '',
        'time': '',
        'ip': '',
        'content': '',
        'comments': []
    }

    abbr_to_num = {name: num for num,
                   name in enumerate(month_abbr) if num}

    for info in soup.select('span.article-meta-value'):
        info_list.append(info.extract().text)
    for push in soup.select('div.push'):
        push_list.append(push.extract())
    for content in soup.select('#main-content'):
        content = content.extract().text

    try:
        date_time = info_list[-1].split(' ')
        year = date_time[-1]

        article['original_poster'] = info_list[0].split(' ')[0]
        article['board'] = info_list[1]
        article['title'] = info_list[2]
        article['date'] = year + '-' + \
            str(abbr_to_num[date_time[1]]).zfill(
                2) + '-' + date_time[-3].zfill(2)
        article['time'] = date_time[-2][0:5]

        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        article['ip'] = pattern.search(content)[0]

        article['content'] = content
    except Exception as e:
        with open('log.txt', 'a') as log:
            log.write(str(e) + ': ' + url + '\n')

    for each_push in push_list:
        try:
            article['comments'].append({
                'type': each_push.contents[0].text.strip(),
                'user': each_push.contents[1].text,
                'opinion': each_push.contents[2].text[2:],
                'ip': each_push.contents[3].text.split(' ')[-3],
                'date': year + '-' + each_push.contents[3].text.split(' ')[-2].replace('/', '-'),
                'time': each_push.contents[3].text.split(' ')[-1].strip()
            })
        except IndexError as e:
            print(e, url)
        except AttributeError as e:
            print(e, url)
        except UnboundLocalError as e:
            with open('log.txt', 'a') as log:
                log.write(str(e) + ': ' + url + '\n')

    return article

def unique_id(string1, string2):
    str_list = sorted([string1, string2])
    return str_list[0] + str_list[1]

def import_data(raw, url):
    try:
        user = User.objects.create(id=raw['original_poster'])
    except IntegrityError:
        user = User.objects.get(id=raw['original_poster'])
    try:
        Article.objects.create(id=url, original_poster=user, board=raw['board'], \
            title=raw['title'], date=raw['date'], time=raw['time'], ip=raw['ip'], content=raw['content'])
    except IntegrityError:
        pass
    push_set = set()
    boo_set = set()
    for comment in raw['comments']:
        try:
            poster = User.objects.create(id=comment['user'])
        except IntegrityError:
            poster = User.objects.get(id=comment['user'])
        try:
            Comment.objects.create(id=(comment['user']+comment['opinion']+comment['date']+comment['time']), \
                poster=poster, article=Article.objects.get(id=url), reaction=comment['type'], opinion=comment['opinion'], \
                    date=comment['date'], time=comment['time'], ip=comment['ip'])
        except IntegrityError:
            pass
        except ValidationError as e:
            print(comment)
        if comment['type'] == '推':
            push_set.add(poster)
        elif comment['type'] == '噓':
            boo_set.add(poster)
    push_set = [element for element in push_set]
    for index1 in range(len(push_set) - 1):
        for index2 in range(index1 + 1, len(push_set)):
            try:
                CommonComment.objects.create(id=unique_id(push_set[index1].id, push_set[index2].id), account1=push_set[index1], account2=push_set[index2], weight=1)
            except IntegrityError:
                common_comment = CommonComment.objects.get(id=unique_id(push_set[index1].id, push_set[index2].id))
                common_comment.weight += 1
                common_comment.save()
    boo_set = [element for element in boo_set]
    for index1 in range(len(boo_set) - 1):
        for index2 in range(index1 + 1, len(boo_set)):
            try:
                CommonComment.objects.create(id=unique_id(boo_set[index1].id, boo_set[index2].id), account1=boo_set[index1], account2=boo_set[index2], weight=1)
            except IntegrityError:
                common_comment = CommonComment.objects.get(id=unique_id(boo_set[index1].id, boo_set[index2].id))
                common_comment.weight += 1
                common_comment.save()

@shared_task(name='update_ptt_data')
def update_data():
    session = new_session()

    article_dict = get_trending(session, datetime.today() - timedelta(days=2))

    for each_url in article_dict['爆']:
        import_data(dump_article(session, each_url), each_url)
    for each_url in article_dict['XX']:
        import_data(dump_article(session, each_url), each_url)