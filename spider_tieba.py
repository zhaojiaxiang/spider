'''
抓取百度贴吧--生活大爆炸吧的基本内容
'''
import requests
from bs4 import BeautifulSoup
import time

# 首先写好抓取网页的函数
def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding ='utf-8'
        return r.text
    except:
        return 'Error!'

def get_content(url):
    '''
    分析贴吧的网页文件，整理信息，保存到列表变量中
    '''

    #初始化一个列表来保存所有的帖子信息
    comments = []
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('li', attrs={'class':' j_thread_list clearfix'})

    for li in liTags:
        comment = {}
        try:
            comment['title']=li.find('a',attrs={'class':'j_th_tit'}).text.strip()
            comment['link']='http://tieba.baidu.com/'+\
                li.find('a', attrs={'class':'j_th_tit'})['href']
            comment['name']=li.find('span',attrs={'class':'tb_icon_author'}).text.strip()
            comment['time']=li.find('span', attrs={'class':'pull-right is_show_create_time'}).text.strip()
            comment['replyNum']=li.find('span', attrs={'class':'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            print('Something Wrong!')
    return comments

def Out2File(dict):
    '''
    将爬去到的数据写入到本地
    保存到当前目录的TTBT.txt文件中
    '''
    with open('TTBT.txt','a+') as f:
        for comment in dict:
            try:
                f.write('标题：{} \t 链接: {} \t 发帖人： {} \t  发帖时间: {} \t 回复数量: {} \n'.format(
                    comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
            except:
                continue
            
        print('当前页面爬取完成')

def main(base_url, deep):
    url_list = []
    # 将所有的需要爬去的url存入列表中
    for i in range(1, deep):
        url_list.append(base_url+ '&pn='+ str(50*i))
    print('所有的网页已经下载到本地！开始筛选信息。。。。')

    # 循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('所有的讯息都已经保存完毕！')

base_url='http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'

deep = 3

if __name__=='__main__':
    main(base_url, deep)