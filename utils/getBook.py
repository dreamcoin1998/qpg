import requests
from youshengshu.models import Youshengshu
import json


def getBook(pk, page, headers):
    '''
    获取有声书资源
    :param pk:
    :return:
    '''
    try:
        session = requests.Session()
        youshengshu = Youshengshu.objects.filter(pk=pk)
        print(youshengshu)
        src_link = youshengshu[0].link
        link_mid = src_link.replace('https://ting55.com', '')
        id = link_mid.replace('/book/', '') # 有声书在恋听网的id
        data= {'bookId': id, 'isPay': '0', 'page': page}
        r = 'https://ting55.com/book/%s-%s' % (id, page)
        session.get(r, headers=headers)
        headers['Referer'] = r
        print(data)
        res = session.post('https://ting55.com/glink', data=data, headers=headers)
        dic = res.json()
        del dic['status']
        print(headers)
        print(res)
        print(res.json())
        for key, value in dic.items():
            if value:
                return value
    except Exception as e:
        print(e)
        return None


def search2(name,pages):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
    url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + name + '&page='+ str(pages) + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
    html = requests.get(url,headers = headers)
    all = json.loads(html.text)
    data = all['data']['result']['response']['docs']
    datas = []
    for x in data:
        datas.append(x)
    return datas



def search1(book):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
    url = 'https://www.ximalaya.com/revision/search?core=album&kw=' + book + '&spellchecker=true&rows=20&condition=relation&device=iPhone'
    html = requests.get(url, headers=headers)
    all = json.loads(html.text)
    total_pages = all['data']['result']['response']['totalPage']
    list1 = range(1, total_pages + 1)
    datas = []
    for n in list1:
        books = search2(book, n)
        for b in books:
            datas.append(b)
    print(len(datas))
    return datas


def getDetail2(id, pages):
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + id + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=' + str(
        pages) + '&pageSize=10&pre_page=0'
    html = requests.get(url)
    all = json.loads(html.text)
    data = all['data']['list']
    return data


def getDetail1(albumId, type, ji=None, page=None):
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=%s&pageSize=%s&pre_page=0'
    if type == 'all':
        url = url % ('1', '10')
        html = requests.get(url)
        all = json.loads(html.text)
        total_pages = all['data']['totalCount']
        if total_pages % 10:
            pagenum = total_pages // 10 + 1
        else:
            pagenum = total_pages // 10
        assert int(page) <= pagenum, ('页数超出')
        books = getDetail2(albumId, page)
        return books, pagenum
    elif type == 'one':
        url = url % (str(ji), '1')
        html = requests.get(url)
        all = json.loads(html.text)
        data = all['data']['list']
        return data[0]


def getTypeList(father_type, son_type, sort, page, perPage=10):
    url = 'https://www.ximalaya.com/revision/category/queryCategoryPageAlbums?category=%s&subcategory=%s&meta=&sort=%s&page=%s&perPage=%s' % (str(father_type), str(son_type), str(sort), str(page), str(perPage))
    res = requests.get(url)
    total = res.json()['data']['total']
    if total % perPage:
        pagenum = total // 10 + 1
    else:
        pagenum = total // 10
    assert page <= pagenum, ('页数超出')
    books = res.json()['data']['albumId']
    return books, total


# getDetail1('22291692', 'all', page=12)