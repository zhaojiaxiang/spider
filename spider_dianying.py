'''
爬取最新电影排行榜单
url：http://dianying.2345.com/top/
'''
import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status
        #该网站使用gbk编码
        r.encoding = 'gbk'
        return r.text
    except Exception as e:
        return e

def get_pic_from_url(url, name):
    pic_content = requests.get(url, stream=True).content
    open('D:/python/spider/img/'+name+'.jpg', 'wb+').write(pic_content)

def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    movies_list = soup.find('ul', class_='picList clearfix')
    movies = movies_list.find_all('li')
    
    for top in movies:
        img_url = 'http:'+top.find('img')['src']  #要加 http: 不然报错
        name = top.find('span', class_='sTit').a.text

        try:
            time = top.find('span', class_='sIntro').text
        except Exception as e:
            #print('time: ', str(e))
            time = '暂无上映时间'

        actors = top.find('p', class_='pActor')
        actor  = ''

        for act in actors:
            actor = actor+act.string+'  '
        
        intro = top.find('p', class_='pTxt pIntroShow').text
        print('片名：{}\t{}\n{}\n{} \n \n'.format(name, time, actor, intro))

        # with open('D:/python/spider/img/' +name+ '.png', 'wb+') as f:
        #     f.write(requests.get(img_url).content)
        get_pic_from_url(img_url, name)


def main():
    url = 'http://dianying.2345.com/top/'
    get_content(url)

if __name__ == '__main__':
    main()

