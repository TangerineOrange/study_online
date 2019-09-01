import requests


def getData():

    TIME_OUT = 10
    try:
        page = 1
        url = 'https://www.wanrong.gov.cn/zmhd/ldxx.jsp?formname54999at=3&formname54999ap=%d&formname54999ac=25&urltype=tree.TreeTempUrl&wbtreeid=1050' % page
        res = requests.get(url,   timeout=TIME_OUT)
        res.encoding = 'utf-8'
    except Exception as e:
        print(repr(e))
        return

    # .find_next_sibling() ,下一个存在且是标签，则返回，否则None
    # find_next() 是下一个标签 ，下一个如果不是标签，继续往下找
    # find_next(text=True) 从本标签的Text 开始的，一直下一个Text

    # .next_element       从本标签的Text 开始的，一直下一个Text
    # .next_sibling       兄弟节点，必须同在一个父标签内
    # 没有找到，不存在的，就都是None，可以用if判断。

    # div_info = soup.select('div.movie > div.info')[0]
    # pl_url = soup.select('div.movie > div.screencap > a.bigImage')[0]['href']
    # ps_url = item.find("img", src=True).get("src")

