'''
爬取豆瓣正在上映电影
电影名称、导演、主要演员、评分、链接
'''

import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        return e

def get_pic_from_url(url, name):
    pic_content = requests.get(url, stream=True).content
    open('D:/python/spider/doubandy/'+name+'.jpg', 'wb+').write(pic_content)

def get_movieurl(url):

    movie_list = []

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    movies_list = soup.find('ul', class_='lists')
    movies = movies_list.find_all('li', class_='list-item')
    for movie in movies:
        name = movie.find('li', class_='stitle').a.text
        name = name.strip()
        title_li = movie.find('li', class_='stitle')
        link = title_li.find('a', class_='ticket-btn')['href']
        movie_list.append(link)
        # try:
        #     with open('douban.txt', 'a+') as f:
        #         f.write('电影名称：{} \t 电影链接：{} \n'.format(name, link))
        #         print('电影名称写入', name)
        # except Exception as e:
        #     print(str(e))
    return movie_list

def get_comment_url(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    all_comment = soup.find('div', class_="mod-hd")
    # comment_title = (all_comment.find('h2')).find('i').text
    comment_url = (all_comment.find('h2')).find('a')['href']
    comment_num = (all_comment.find('h2')).find('a').text
    return comment_url, comment_num

def get_comments(url, title):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    comments = soup.find('div', class_='mod-bd')
    hot_comments = comments.find_all('div', class_='comment-item')
    for hot_comment in hot_comments:
        comment_user = hot_comment.find('span',class_='comment-info').a.text
        comment_date = (hot_comment.find('span',class_='comment-time ').text).strip()
        comment = (hot_comment.find('span', class_='short').text).strip()
        comment_user = comment_user.encode('gbk','ignore').decode('gbk')
        comment = comment.encode('gbk','ignore').decode('gbk')
        with open('D:\python\spider\doubandy\{}.txt'.format(title), 'a+') as f:
            f.write('评论者：{}\t 评论时间：{}\t 评论内容：{}\n'.format(comment_user, comment_date, comment))

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1').span.string
    title = title.encode('gbk','ignore').decode('gbk')
    with open('D:\python\spider\doubandy\{}.txt'.format(title), 'a+') as f:
        f.write(title+'\n')
    img_url = soup.find('img')['src']
    get_pic_from_url(img_url, title)
    print('图片下载完成')

    comments_url,comment_num = get_comment_url(url)
    comment_num = comment_num
    comment_num = comment_num[3:8]
    comment_pages = int(int(comment_num)/20)
    for page in range(0, comment_pages):
        try:
            get_comments(comments_url+'&start={}'.format(str(page*20)), title)
            print(comments_url+'&start={}'.format(str(page*20)))
        except Exception as e:
            return e
       
        print('当前页数：{}'.format(str(page+1)))

def get_single_url(all_url):
    for url in all_url:
        get_content(url)
        percent = (all_url.index(url)/len(all_url))*100
        print('当前进度{}%'.format(percent) ) 

def main():
    url = 'https://movie.douban.com/cinema/nowplaying/shanghai/'
    movie_list = get_movieurl(url)
    get_single_url(movie_list)
if __name__ == '__main__':
    main()