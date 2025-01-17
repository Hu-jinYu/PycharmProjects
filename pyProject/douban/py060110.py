import re
import requests
from bs4 import BeautifulSoup

# 获取豆瓣话题评论中的邮箱（视频，提取函数之后）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}


def download_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    url_set = set()
    paginator_eles = soup.find('div', attrs={'class': 'paginator'})
    if paginator_eles:
        for a_ele in paginator_eles.find_all('a'):
            url_set.add(a_ele.attrs.get('href'))
        page_obj_list = [soup]
        for url in url_set:
            print(f'下载分页{url}')
            page_obj = requests.get(url, headers=headers)
            page_obj_url = BeautifulSoup(page_obj.text, 'lxml')
            page_obj_list.append(page_obj_url)
    return page_obj_list


def fetch_emails(page_obj_list):
    mail_list = []
    for page_obj in page_obj_list:
        comment_eles = page_obj.find_all('div', attrs={'class': 'reply-doc'})
        for ele in comment_eles:
            comment_ele = ele.find('p', attrs={'class': 'reply-content'})
            mail = re.search(r'\w+@\w+.\w+', comment_ele.text, re.A)
            # print(mail)
            if mail:
                pub_time = ele.find('span', attrs={'class': 'pubtime'})
                # print(mail.group(), '\t\t\t', pub_time.text)
                mail_list.append([mail.group(), pub_time.text])
    print(mail_list)


all_page_list = download_page('https://www.douban.com/group/topic/198233257/')
fetch_emails(all_page_list)
