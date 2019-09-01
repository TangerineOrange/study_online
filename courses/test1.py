import random
import time
from threading import Timer
from threading import Thread

from django.shortcuts import render
from .models import Movies
from .models import image
from django.http import HttpResponse
import sys
import datetime
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
# 引入我们创建的表单类
from .forms import AddForm
from django.conf import settings
import os
import logging
import json
import re
import requests
from .models import CoversLocal, MoviesLocal, CoversPsLocal
from django.http import JsonResponse


# Create your views here.


def insertAllMoviesIntoSQL():
    # for id in settings.ID_INFO_LIST:

    # resDir = '\\学习资料\\prestige\\ABP\\'
    # resDirUrl = '学习资料/prestige/ABP/'
    m_root = ''
    idName = settings.ID_INFO_LIST['ABP']

    dataList = []
    resDir = ''
    index = 0
    resDirUrl = ''
    for file in os.listdir(m_root):
        index += 1

        fType = os.path.splitext(file)[1]
        if fType == '.mp4' or fType == '.avi':
            print('file ', file)
            print('path ', settings.STATIC_URL + resDir + file)
            idNum = re.search('[1-9]\d{0,2}', file).group()
            movies = Movies(
                number='abp-' + idNum,
                title=file,
                movie_path=settings.STATIC_URL + resDirUrl + file,
                cover_name='',
                cover_path='',
                stars='',
                date='2019-07-24',
                studio='',
                label='',
                series='',
            )
            # Determine if the file is a picture type
            for f2 in os.listdir(m_root):
                fType = os.path.splitext(f2)[1]
                if fType == '.jpg' or fType == '.jpeg' or fType == '.png':
                    # Extracting ID_Num from picture
                    idNum = re.search('[1-9]\d{0,2}', f2).group()
                    print('f2 ', f2)
                    print('idNum ', idNum)
                    if (idNum in file):
                        movies.cover_name = f2
                        movies.cover_path = settings.STATIC_URL + resDirUrl + f2
        dataList.append(movies)

    try:
        Movies.objects.bulk_create(dataList)
        return "插入成功"
    except Exception as err:
        logging.warning(('post_error', str(err)))
        return "插入失败" + "OS error: {0}".format(err)


def removeAllMoviesFromSQL():
    try:
        Movies.objects.all().delete()
        return "删除成功"
    except Exception as err:
        logging.warning(('post_error', str(err)))
        return "删除失败" + "OS error: {0}".format(err)


def DateEncoder(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime('%Y-%m-%d')


def showAllMoviesFromSQL():
    movies = Movies.objects.all()
    jsonObj = json.dumps(list(movies.values()),
                         default=DateEncoder, ensure_ascii=False)
    return jsonObj
    # return render(request, 'home.html', {'num': num})
    # return JsonResponse(json.dumps(a),safe=False)
    # return HttpResponse(num)


def insertOneMovieIntoSQL():
    try:
        Movies.objects.create(
            id=1,
            name="XIAOWANG",
            path="TEST",
            type=".jpg",
        )
        return "插入成功"
    except IntegrityError as err:
        print("OS error: {0}".format(err))
        return "插入失败" + "OS error: {0}".format(err)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "插入失败" + str(sys.exc_info()[0])


def getTheLatestMoviesCover(idName):
    existedCount = 0
    downloadCount = 0
    downloadList = []
    times = 0

    print('idName ', idName)

    moviesDir = settings.MOVIE_DIRS[idName]

    latestIdNum = getTheLatestId(idName)
    coversList = getCoverIdList(moviesDir)

    coverUrl = settings.COVERS_URLS[idName]
    coverUrlParam = settings.COVERS_URLS_PARAM[idName]

    while not (existedCount > 5 or latestIdNum < 1):
        print('looper ', times)
        times += 1
        i = 0

        # Scan all existed covers, if not same download it, else count plus one

        # Reverse sorting 'coversList'. So the first item is MAX!
        # if latestIdNum > MAX, it means latestIdNum not included
        if latestIdNum > coversList[0] or (latestIdNum not in coversList):
            # if not included download it, else count plus one
            downloadCover(moviesDir, coverUrl, coverUrlParam, str(latestIdNum), idName)
            downloadCount += 1
            downloadList.append(str(latestIdNum))
        else:
            existedCount += 1
        latestIdNum -= 1

    if downloadCount > 0:
        return "download successful. " + str(downloadCount) + " covers download. there is " + ",".join(downloadList)
    else:
        return "you covers is latest!"


def getTheLatestId(idName):
    latestIdUrl = settings.ID_INFO_LIST[idName]['JAV_URLS']
    print('latestIdUrl ', latestIdUrl)

    # 需要判断这些番号是否是发布完毕的。
    if latestIdUrl == settings.JAV_FULL:
        return int(settings.JAV_FULL)

    rep = requests.get(latestIdUrl)
    rep.encoding = 'utf-8'
    soup = BeautifulSoup(rep.text, "html5lib")
    latestId = soup.select(settings.JAV_ELE)[0].text
    latestIdNum = int(re.search('[1-9][0-9]{0,2}', latestId).group())

    print('latestIdNum ', latestIdNum)

    return latestIdNum


def getCoverIdList(moviesDir):
    print('moviesDir ', moviesDir)

    fileList = os.listdir(moviesDir)
    coversList = []
    for file in fileList:
        fType = os.path.splitext(file)[1]
        if fType == '.jpg' or fType == '.jpeg' or fType == '.png':
            idNum = int(re.search('[1-9]\d{0,2}', file).group())
            coversList.append(idNum)

    coversList.sort(reverse=True)
    print('coversList:  ', coversList)

    return coversList


def downloadCover(moviesDir, coverUrl, urlParam, idNum, idName):
    url = coverUrl + idNum + '/' + urlParam + idNum + 'pl.jpg'

    print('url: ', url)

    img = requests.get(url)

    print('img.content', len(img.content))

    if len(img.content) > 2732:
        print('write this image: ', (moviesDir + idName + idNum + 'pl.jpg'))
        f = open(moviesDir + idName + idNum + 'pl.jpg', 'wb')  # 存储图片，多媒体文件需要参数b（二进制文件）
        f.write(img.content)  # 多媒体存储content
        f.close()
    else:
        print('this image doesn\'t exist ')
        print('this image size is : ', len(img.content))


def timeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


class MoviesInfo:
    idName = ''
    latestIdUrl = ''
    latestIdNum = -1
    moviesDir = ''

    def __init__(self, idName):
        self.idName = idName


# 获取列表的第二个元素
def takeKey(CoversLocal):
    return CoversLocal.cover_c_time


def insertLocalDataOfMoviesIntoSQL(idNames):
    # moviesDir = settings.MOVIE_DIRS[idName]
    coversList = []
    moviesList = []
    psList = []

    CoversLocal.objects.all().delete()
    MoviesLocal.objects.all().delete()
    CoversPsLocal.objects.all().delete()
    # check database table
    # check the length
    # coversList = list(CoversLocal.objects.filter(cover_name__icontains=idName).order_by('cover_c_time'))

    for idName in idNames:
        print(idName)
        moviesDir = settings.ID_INFO_LIST[idName]['MOVIES_DIR']

        fileList = os.listdir(moviesDir)
        for file in fileList:
            fType = os.path.splitext(file)[1]
            path = moviesDir + file
            c_time = timeStampToTime(os.path.getctime(path))

            if fType == '.jpg' or fType == '.jpeg' or fType == '.png':
                idNum = re.search('[1-9][0-9]{0,2}', file).group()
                id_name = idName + '-' + idNum

                coversLocal = CoversLocal(
                    cover_pl_name=file,
                    cover_pl_c_time=c_time,
                    cover_pl_path=path,

                    id_name=id_name,
                )
                coversList.append(coversLocal)

            elif fType == '.mp4' or fType == '.avi':
                idNum = re.search('[1-9][0-9]{0,2}', file).group()
                id_name = idName + '-' + idNum
                moviesLocal = MoviesLocal(
                    movie_name=file,
                    movie_c_time=c_time,
                    movie_path=path,
                    movie_size=os.path.getsize(path),
                    id_name=id_name,
                )
                moviesList.append(moviesLocal)

        img_ps_dir = moviesDir + 'ps\\'

        if not os.path.exists(img_ps_dir):
            os.makedirs(img_ps_dir)

        for file in os.listdir(img_ps_dir):
            f_type = os.path.splitext(file)[1]
            if f_type == '.jpg' or f_type == '.jpeg' or f_type == '.png':
                id_num = re.search('[1-9][0-9]{0,2}', file).group()

                coversPsLocal = CoversPsLocal(
                    cover_ps_name=file,
                    cover_ps_c_time=timeStampToTime(os.path.getctime(img_ps_dir + file)),
                    cover_ps_path=img_ps_dir + file,

                    id_name=idName + '-' + id_num,
                )
                psList.append(coversPsLocal)

    CoversLocal.objects.bulk_create(coversList)
    CoversPsLocal.objects.bulk_create(psList)
    MoviesLocal.objects.bulk_create(moviesList)

    return 'insert successful!, ' + str(len(moviesList)) + ' data of the movies  inserted.  ' \
           + str(len(coversList)) + ' data of the covers inserted.  ' \
           + str(len(psList)) + ' data of the ps covers inserted. \n '


TIME_OUT = 7

MIN_W_T = 8
MAX_W_T = 13
proxies = {'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}


def scanHTMLtoGetItem(idName, items, page):
    try:
        res = requests.get(settings.ID_INFO_LIST[idName]['AVMOO_URLS'] % page, proxies=proxies, verify=True)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html5lib")
        # recursive=False 表示只搜查直接子节点
        items += soup.find("div", id="waterfall").find_all("div", class_="item", recursive=False)

        for i in range(len(items) - 1, -1, -1):
            id_all = items[i].find("date").text
            result = Movies.objects.filter(number__icontains=id_all)
            if result:
                items.pop(i)
                print('del' + id_all)
        # print(items)
        print(len(items))

        print(" 这是  " + idName + "  ，当前共 " + str(len(items)) + "条数据")

    except Exception as e:
        print(repr(e))


def scanItemToGetInfo(item, movie_list):
    try:
        info_url = item.find("a", class_="movie-box").get("href")
        res = requests.get(info_url, proxies=proxies, verify=True, timeout=TIME_OUT)
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

    soup = BeautifulSoup(res.text, "html5lib")
    div_info = soup.select('div.movie > div.info')[0]
    pl_url = soup.select('div.movie > div.screencap > a.bigImage')[0]['href']
    ps_url = item.find("img", src=True).get("src")

    img_ps_name, img_ps_dir, img_pl_name, img_pl_dir = downloadCoverPsPl(ps_url, pl_url)

    title = soup.select('div.container')[0].find_next("h3").text
    number = div_info.find("span", text=u"識別碼:").find_next("span").text

    try:
        release_date = div_info.find("span", text=u"發行日期:").next_sibling.string
    except Exception as e:
        release_date = ''

    try:
        length = div_info.find("span", text=u"長度:").next_sibling.string
    except Exception as e:
        length = ''

    studio = div_info.find("p", text="製作商: ").find_next("a", href=True).text
    label = div_info.find("p", text="發行商: ").find_next("a", href=True).text

    try:
        series = div_info.find("p", text="系列:").find_next().text
    except Exception as e:
        series = ''

    try:
        stars = soup.select('a.avatar-box')[0].find('span').text
    except Exception as e:
        stars = ''

    # scan file here
    movie = Movies(
        title=title,
        number=number,
        release_date=release_date,
        length=length,
        studio=studio,
        label=label,
        series=series,
        stars=stars,
        cover_ps_name=img_ps_name,
        cover_ps_path=img_ps_dir,
        cover_pl_name=img_pl_name,
        cover_pl_path=img_pl_dir,
    )

    movie_list.append(movie)

    print('title:  ', title)
    print('number:  ', number)
    print('release_date:  ', release_date)
    print('length:  ', length)
    print('studio:  ', studio)
    print('label:  ', label)
    print('series:  ', series)
    print('stars:  ', stars)


def downloadCoverPsPl(ps_url, pl_url):
    try:
        imgName = os.path.basename(ps_url)
        imgAZ = re.search('([a-zA-Z]{2,4})(0*)([1-9][0-9]{0,2})', imgName).groups()[0].upper()
        imgNum = re.search('([a-zA-Z]{2,4})(0*)([1-9][0-9]{0,2})', imgName).groups()[2]

        img_ps_dir = settings.ID_INFO_LIST[imgAZ]['MOVIES_DIR'] + 'ps\\'
        img_pl_dir = settings.ID_INFO_LIST[imgAZ]['MOVIES_DIR']

        imgPsName = imgAZ + '-' + imgNum + '-' + 'ps.jpg'
        imgPlName = imgAZ + '-' + imgNum + '-' + 'pl.jpg'

        print('imgAZ' + imgAZ)
        print('imgNum' + imgNum)
        print('imgPlName' + imgPlName)
        print('img_pl_dir' + img_pl_dir)
        print('img_ps_dir' + img_ps_dir)
        if not os.path.exists(img_ps_dir):
            os.makedirs(img_ps_dir)
    except Exception as e:
        imgUrl, imgName, imgAZ, imgNum, img_ps_dir, img_pl_dir = '', '', '', '', '', ''
        print('can\'t download img')
        return

    print('ps_url : ', ps_url)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cl = CoversLocal.objects.get(id_name__icontains=imgAZ + '-' + imgNum)
    except Exception as e:
        downloadImage(pl_url, img_pl_dir, imgPlName)
        cl = CoversLocal.objects.create(
            cover_pl_name=imgPlName,
            cover_pl_c_time=now,
            cover_pl_path=img_pl_dir + imgPlName,
            id_name=imgAZ + '-' + imgNum,
        )

    try:
        pl = CoversPsLocal.objects.get(id_name__icontains=imgAZ + '-' + imgNum)
    except Exception as e:
        downloadImage(ps_url, img_ps_dir, imgPsName)
        pl = CoversPsLocal.objects.create(
            cover_ps_name=imgPsName,
            cover_ps_c_time=now,
            cover_ps_path=img_ps_dir + imgPsName,
            id_name=imgAZ + '-' + imgNum,
        )

    imgPsName, img_ps_dir, imgPlName, img_pl_dir = pl.cover_ps_name, \
                                                   pl.cover_ps_path, \
                                                   cl.cover_pl_name, \
                                                   cl.cover_pl_path

    return imgPsName, img_ps_dir, imgPlName, img_pl_dir


def downloadImage(imgUrl, imgPath, imgName):
    try:
        # cover_ps_name = models.TextField(verbose_name=u"小封面名称", default="")
        # cover_ps_c_time = models.TextField(verbose_name=u"小封面创建时间", default="")
        # cover_ps_path = models.TextField(verbose_name=u"小封面地址", default="")
        img = requests.get(imgUrl, proxies=proxies, verify=True, timeout=TIME_OUT)
        print('write this image: ', (imgPath + imgName))
        f = open(imgPath + imgName, 'wb')  # 存储图片，多媒体文件需要参数b（二进制文件）
        f.write(img.content)  # 多媒体存储content
        f.close()
    except Exception as e:
        print(repr(e))


def timer_todo(function, args=None):
    wait_time = random.randint(MIN_W_T, MAX_W_T)
    print('wait ' + str(wait_time) + ' second ')
    t = Timer(wait_time, function, args)
    t.start()
    t.join()


def insertTheNetInfoOfMovies(idNames):
    movie_list = []

    t = Thread(target=excuteDownload, args=[idNames, movie_list])
    t.start()
    t.join()

    result = str(len(movie_list)) + ' data inserted !'
    print(result)
    return result


def excuteDownload(idNames, movie_list):
    insertLocalDataOfMoviesIntoSQL(idNames)
    # Movies.objects.all().delete()
    items = []

    page = 1
    # get HTML Item
    for idName in idNames:
        # id_num = getTheLatestId(idName)
        # print(id_num)
        timer_todo(scanHTMLtoGetItem, args=[idName, items, page])

    # get detail from Item
    for item in items:
        timer_todo(scanItemToGetInfo, args=[item, movie_list])
    Movies.objects.bulk_create(movie_list)
