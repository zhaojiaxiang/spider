import requests
from bs4 import BeautifulSoup
import time

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status
        r.encoding=('utf-8')
        return r.text
    except :
        return 'Something Wrong!'

def get_content(url):
    '''
    爬取每一个类型小说的排行榜，
    按顺序写入文件
    文件内容为 小说名字+小说链接
    将内容保存到列表
    并且返回一个装满url链接的列表
    '''
    url_list = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    # 由于小说排版的原因，历史类和完本类小说不在一个div里

    category_list = soup.find_all('div', class_='index_toplist mright mbottom')

    history_finished_list = soup.find_all('div', attrs={'class':'index_toplist mbottom'})

    for cate in category_list:
        name = cate.find('div', class_ = 'toptab').span.string
        try:
            with open('novel_list.csv', 'a+') as f:
                f.write('\n小说种类：{}\n'.format(name))
        except Exception as e:
            print('Exception:',e)
        
        #直接通过上style属性来定位总排行榜
        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')

        for book in book_list:
            link = 'http://www.qu.la'+book.a['href']    
            title = book.a['title']
            url_list.append(link)
            with open('noval_list.csv','a+' ) as f:
                f.write('小说名:{}\t 小说地址：{}\n'.format(title,link))
    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string 
        with open('noval_list.csv', 'a+') as f:
            f.write('\n小说种类：{} \n'.format(name))

        general_list = cate.find(style = 'display: block;')
        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la' + book.a['href']    
            title = book.a['title']
            url_list.append(link)

            with open('noval_list.csv', 'a+') as f:
                f.write('小说名:{}\t 小说地址：{}\n'.format(title, link))     
    return url_list

def get_txt_url(url):
    '''
    获取每个章节的url地址
    并创建小说文件
    '''
    url_list = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text

    with open('D:\python\spider\小说\{}.txt'.format(txt_name), 'a+') as f:
        f.write('小说标题：{} \n'.format(txt_name))
    
    for url in lista:
        url_list.append('http://www.qu.la'+url.a['href'])

    return url_list, txt_name

def get_one_txt(url, txt_name):
    '''
    获取小说的每个章节的文本
    并写入到本地
    '''
    html = get_html(url).replace('<br/>', '\n')
    soup = BeautifulSoup(html, 'lxml')

    try:
        txt = soup.find('div', id='content').text.replace(
            'chaptererror();', '')
        #先用GBK编码，忽略非法字符，然后再用GBK译码
        txt = txt.encode('GBK','ignore').decode('GBk')
        title = soup.find('title').text
        with open('D:\python\spider\小说\{}.txt'.format(txt_name), 'a') as f:
            f.write(title +'\n\n')
            f.write(txt)
            print('当前小说：{} 当前章节{} 已经下载完成'.format(txt_name, title))
    except Exception as e:
        print(e)
        print('Someting Wrong!')

# def get_all_txt(url_list)
#     '''
#     下早排行榜里面的所有小说，并保存为txt格式
#     '''

def main(base_url):

    url_list = get_content(base_url)
    url_list = list(set(url_list))
    for url in url_list:
        page_list, txt_name = get_txt_url(url)

        for page_url in page_list:
            if page_url.find('book', 0, len(page_url)) != -1:
                get_one_txt(page_url, txt_name)
                print('当前进度{}%'.format(page_list.index(page_url)/len(page_list)*100))
        break

base_url = 'http://www.qu.la/paihangbang/'
if __name__ == '__main__':
    main(base_url)
    
