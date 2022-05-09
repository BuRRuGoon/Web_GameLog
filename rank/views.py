from django.shortcuts import redirect, render
from .models import Steam
from .models import Mobile
from .models import Online
from datetime import datetime

import pymysql  # 모듈 import
import requests as req
import re
from bs4 import BeautifulSoup

from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys

# Create your views here.
def main(request):
    online = Online.objects.all().order_by('id')[:5]
    mobile = Mobile.objects.all().order_by('id')[:5]
    steam = Steam.objects.all().order_by('id')[:5]

    contents = {
        'online': online,
        'mobile': mobile,
        'steam': steam,
    }
    return render(request, 'rank/mainRanking.html', contents)

def onlineRanking(request):
    online = Online.objects.all()

    return render(
        request, 'rank/onlineRanking.html',
        {
            'online' : online
        }
    )

def mobileRanking(request):
    mobile = Mobile.objects.all().order_by('id')[:50]

    return render(
        request, 'rank/mobileRanking.html',
        {
            'mobile' : mobile
        }
    )

def steamRanking(request):
    steam = Steam.objects.all().order_by('id')[:50]

    return render(
        request, 'rank/steamRanking.html',
        {
            'steam' : steam
        }
    )

def steamReload(request):
    res = req.get('https://store.steampowered.com/stats/?l=koreana').text

    soup = BeautifulSoup(res, 'html.parser')

    steamGames = soup.select('.gameLink')
    currentServers = soup.select('.currentServers')

    conn = pymysql.connect(
        host='localhost', user='root', password='1234',
        db='project', charset='utf8'
    )  # 데이터베이스 접속

    cursor = conn.cursor()  # 커서 객체 생성

    steamServersql = '''UPDATE steam SET NOWCURRENT = %s, FULLCURRENT = %s
            WHERE ID = %s'''
    steamTitlesql = '''UPDATE steam SET TITLE = %s
            WHERE ID = %s'''
    steamIdsql = '''UPDATE steam SET STEAMGAMEKEY = %s
            WHERE ID = %s'''
    steamIconUrlsql = '''UPDATE steam SET ICONURL = %s
            WHERE ID = %s'''

    # 현재 접속자수 업데이트
    idCount = 1
    currentCount = True
    sumBool = False
    for currentServer in currentServers:
        # 스팀 통계 현재 접속중인 인원
        if currentCount:
            nowCurrent = currentServer.getText()
            nowCurrent = re.sub(",","",nowCurrent)
            currentCount = False
        else:
            fullCurrent = currentServer.getText()
            fullCurrent = re.sub(",","",fullCurrent)
            currentCount = True # SQL 실행
            sumBool = True
            
        if sumBool:
            cursor.execute(steamServersql, (int(nowCurrent), int(fullCurrent), idCount))
            idCount += 1
            sumBool = False

    # 타이틀명 업데이트
    idCount = 1
    for steamGame in steamGames:
        steamGameName = steamGame.getText()
        cursor.execute(steamTitlesql, (steamGameName, idCount))
        idCount += 1
        
    # 스팀 게임 Id 업데이트
    regex = '/app/(\d+)' 
    pattern = re.compile(regex)
    steamGameIds = pattern.findall(str(steamGames))

    idCount = 1
    print(len(steamGameIds))
    for steamGameId in steamGameIds:
        cursor.execute(steamIdsql, (int(steamGameId), idCount))
        idCount += 1

    idCount = 1
    for steamGameId in steamGameIds:
        url_string = "https://cdn.cloudflare.steamstatic.com/steam/apps//header.jpg"
        index = url_string.find('/header')
        final_string = url_string[:index] + steamGameId + url_string[index:]
        cursor.execute(steamIconUrlsql, (final_string, idCount))
        idCount += 1


    conn.commit()  # 실행내용 저장
    cursor.close()  # 커서 객체 종료
    conn.close()  # 접속 해제

    steam = Steam.objects.all()

    return redirect('/rank/steam')

def onlineReload(request):
    res = req.get('https://www.gamemeca.com/ranking.php').text

    soup = BeautifulSoup(res, 'html.parser')

    pcGamesIconUrl = soup.select('.game-icon')
    pcGamesTitle = soup.select('.game-name > a')
    pcGamesCompany = soup.select('.company > a')

    # 아이콘 이미지 url만 추출
    regex = 'https://cdn.gamemeca.com/gmdb/g\w*/\w*/\w*/\S+\.jpg'
    pattern = re.compile(regex)
    pcGamesIconUrl = pattern.findall(str(pcGamesIconUrl))

    conn = pymysql.connect(
        host='localhost', user='root', password='1234',
        db='project', charset='utf8'
    )  # 데이터베이스 접속

    cursor = conn.cursor()  # 커서 객체 생성

    pcGamesTitlesql = '''UPDATE online SET TITLE = %s
            WHERE ID = %s'''
    pcGamesCompanysql = '''UPDATE online SET COMPANY = %s
            WHERE ID = %s'''
    pcGamesIconUrlsql = '''UPDATE online SET ICONURL = %s
            WHERE ID = %s'''

    # 현재 접속자수 업데이트
    idCount = 1
    for pcGameTitle in pcGamesTitle:
        pcGameTitle = pcGameTitle.getText()
        cursor.execute(pcGamesTitlesql, (pcGameTitle, idCount)) # SQL 실행
        idCount += 1
        
    idCount = 1
    for pcGameCompany in pcGamesCompany:
        pcGameCompany = pcGameCompany.getText()
        cursor.execute(pcGamesCompanysql, (pcGameCompany, idCount)) # SQL 실행
        idCount += 1

    idCount = 1
    for pcGameIconUrl in pcGamesIconUrl:
        cursor.execute(pcGamesIconUrlsql, (pcGameIconUrl, idCount)) # SQL 실행
        idCount += 1
        
    conn.commit()  # 실행내용 저장
    cursor.close()  # 커서 객체 종료
    conn.close()  # 접속 해제

    online = Online.objects.all()

    return redirect('/rank/online')


def mobileReload(request):
    # 키 이벤트에서 특수키 사용하기 위해서 선언
    END = '\ue010'

    conn = pymysql.connect(
        host='localhost', user='root', password='1234',
        db='project', charset='utf8'
    )  # 데이터베이스 접속

    cursor = conn.cursor()  # 커서 객체 생성

    titlesql = '''UPDATE mobile SET TITLE = %s, COMPANY = %s
                WHERE ID = %s'''

    iconUrlsql = '''UPDATE mobile SET ICONURL = %s
            WHERE ID = %s'''

    googlesql = '''UPDATE mobile SET GOOGLE = %s
            WHERE ID = %s'''

    applesql = '''UPDATE mobile SET APPLE = %s
            WHERE ID = %s'''

    onesql = '''UPDATE mobile SET ONE = %s
            WHERE ID = %s'''

    # Headless 모드 옵션
    webdriver_options = wd.ChromeOptions()
    webdriver_options .add_argument('headless')

    # 브라우저 접속을 위한 설정
    chromedriver = 'chromedriver.exe'
    driver = wd.Chrome(chromedriver, options=webdriver_options )
    # driver = wd.Chrome(executable_path='chromedriver.exe') 

    # 대상 웹사이트로 접속
    driver.get('https://www.mobileindex.com/mi-chart/top-100/top-games')
    driver.implicitly_wait(100)

    mobileGamesData = driver.find_elements_by_css_selector('td > span > span > span')

    selectElement = driver.find_element_by_css_selector('.select')
    driver.implicitly_wait(10)
    selectElement.send_keys(Keys.END)
    driver.implicitly_wait(10)
    iconUrls = driver.find_elements_by_css_selector('.app-name > .app-icon')

    googleGamesData = driver.find_elements_by_css_selector('.google > span')
    appleGamesData = driver.find_elements_by_css_selector('.apple > span')
    oneGamesData = driver.find_elements_by_css_selector('.one > span')

    # 모바일 게임 타이틀과 게임사
    # CURRENTCOUNT는 NOW와 FULL을 각각 나눠주기 위해서 사용
    # SUMBOOL은 나눠진 2개의 데이터를 넣기 위해서 스위치구문으로 사용 
    idCount = 1
    currentCount = True
    sumBool = False

    for mobileGameData in mobileGamesData:
        if currentCount:
            mobileGameTitle = mobileGameData.text
            currentCount = False
        else:
            mobileGameCompany = mobileGameData.text
            currentCount = True
            sumBool = True
            
        if sumBool:
            cursor.execute(titlesql, (mobileGameTitle, mobileGameCompany, idCount))
            sumBool = False
            idCount += 1

    # 앱 아이콘
    idCount = 1
    for iconUrl in iconUrls:
        iconUrl = iconUrl.get_attribute('src')
        cursor.execute(iconUrlsql, (iconUrl, idCount))
        idCount += 1

    # 구글
    idCount = 1
    for googleGameData in googleGamesData:
        googleGameData = googleGameData.text.replace("\n위","")
        cursor.execute(googlesql, (googleGameData, idCount))
        idCount += 1

    # 애플
    idCount = 1
    for appleGameData in appleGamesData:
        appleGameData = appleGameData.text.replace("\n위","")
        cursor.execute(applesql, (appleGameData, idCount))
        idCount += 1

    # 원스토어
    idCount = 1
    for oneGameData in oneGamesData:
        oneGameData = oneGameData.text.replace("\n위","")
        cursor.execute(onesql, (oneGameData, idCount))
        idCount += 1

    conn.commit()  # 실행내용 저장
    cursor.close()  # 커서 객체 종료
    conn.close()  # 접속 해제
    driver.quit()

    mobile = Mobile.objects.all()

    return redirect('/rank/mobile')
