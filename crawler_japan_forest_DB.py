# coding:utf-8
import requests

from lxml import html

def downloadImg(img_relativeWebPath,img_saveAbsLocation):
    #img_url = 'https://db.ffpri.go.jp/WoodDB/image/OM-S/Micro-24/img-18231.JPG'
    img_url = 'https://db.ffpri.go.jp/WoodDB/'+img_relativeWebPath[3:] # get ride of '../'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537'
    }     
    tem = requests.get(img_url, headers=headers, timeout=2)
    #with open(r'C:\Users\dell\Desktop\pic.jpg','wb') as f:
    img_url_reverse = img_url[::-1]
    imgname_revURL_i_end = img_url_reverse.find('\\')
    if imgname_revURL_i_end == -1:
        imgname_revURL_i_end = img_saveLocation_reverse.find('/')
    imgname_rev = img_url_reverse[:imgname_revURL_i_end]
    imgname = imgname_rev[::-1]
    with open(img_saveAbsLocation + '\\' + imgname,'wb') as f:
        f.write(tem.content)

def getWoodFamilyInfoByPost(wood_family_infoLink):
    wood_family_infoLink = 'browserecord.php?-action=browse&-recid=292048'
    target_weblink = r'https://db.ffpri.go.jp/WoodDB/JWDB-E_OM/'+wood_family_infoLink
    #test='https://db.ffpri.go.jp/WoodDB/JWDB-E_OM/browserecord.php?-action=browse&-recid=292363'
    # 消息头数据
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '107',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests':'1', 
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',  
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cookie': 'JWDBP_PHP01_1211259925815=35af418934378ecd455d9f88c070b953; TWTwDB_PHP01_1214293436528=86b9b7c55be37ac167b6911224204b68; IDB_PHP01_1222235436982=94f0302b377cbf50edf5bfc85b428619',
        'Host': 'db.ffpri.go.jp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Referer': 'https://db.ffpri.go.jp/WoodDB/JWDB-E_OM/recordlist.php',
        'Origin': 'https://db.ffpri.go.jp', 
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }

    responds_ = requests.post(target_weblink, headers=headers, verify=False)
    return responds_;


def getWoodFamilyRespondByPost(wood_species_family): 
    #url = "https://passport.cnblogs.com/user/signin" # 接口地址
    janpan_forest_OM_DB_url = "https://db.ffpri.go.jp/WoodDB/JWDB-E_OM/recordlist.php" # 接口地址

    # 消息头数据
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '107',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests':'1', 
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',  
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cookie': 'JWDBP_PHP01_1211259925815=35af418934378ecd455d9f88c070b953; TWTwDB_PHP01_1214293436528=86b9b7c55be37ac167b6911224204b68; IDB_PHP01_1222235436982=94f0302b377cbf50edf5bfc85b428619',
        'Host': 'db.ffpri.go.jp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Referer': 'https://db.ffpri.go.jp/WoodDB/JWDB-E_OM/findrecords.php?-db=JWDB_OM&-lay=All_data&',
        'Origin': 'https://db.ffpri.go.jp', 
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }


    #bug here
    #wood_species_family = 'Actinidiaceae'
    
    
    #Payload raw format 
    #-lay=%24layoutName&-action=find&-lop=and&0=eq&1=&2=eq&3=Actinidiaceae&5=eq&6=&7=cn&8=&9=eq&10=&-find=Search
    payload = {
        '0': 'eq',
        '1': '',
        '2': 'eq',
        '3':  wood_species_family,
        '5': 'eq',
        '6': '',
        '7': 'cn',
        '8': '',
        '9': 'eq',
        '10': '',
        '-lay': '$layoutName',
        '-action': 'find',
        '-lop': 'and',
        '-find': 'Search' ,
    }
    # verify = False 忽略SSH 验证

    responds_ = requests.post(janpan_forest_OM_DB_url, json=payload, headers=headers,verify=False)
    return responds_;



def inspect_POST_familyPage(html_txt):
    tree = html.fromstring(html_txt)
    elements = tree.xpath('//td[@class="browse_cell2 right"]')
    elements = tree.xpath('//td[@class="browse_cell2 left"]')
    for element in elements:
        a_ = element.xpath('a')
        TWTwNo = a_[0].text
        wood_family_infoLink = a_[0].attrib['href']

        #HERE POST FOR Wood Family Species Infomation page.
        responds_infopage = getWoodFamilyInfoByPost(wood_family_infoLink)
        infopageTree = html.fromstring(responds_infopage.text)
        # get all <TD> elements at webpage  ### 
        TDs = infopageTree.xpath('//td')
        keylist_raw = []
        valuelist_raw = []
        index = 0
        for i in TDs:
            if index % 2 == 0:
                 keylist_raw.append(i.text)
            else :
                 valuelist_raw.append(i.text)
            index = index + 1
        #TODO: handle key & value list data to a dict
        


field_data
responds_woodFamilyPage = getWoodFamilyRespondByPost("Actinidiaceae")
wood_familyPage_html_txt = responds_woodFamilyPage.text

inspect_POST_familyPage(wood_familyPage_html_txt)
img_relativeWebPath = 
img_saveAbsLocation = r''
downloadImg(img_relativeWebPath,img_saveAbsLocation):

#print(html_)
#这是所有的树名td
ele = tree.xpath('//td[@class="browse_cell2 left"]') 
elements_spceies_name = []
for i in ele:
    elements_spceies_name.append(i.text)
tmp = ''
count = 0
#check dupulicated name
for i in elements_spceies_name:
    if i is tmp:
        count = count + 1
    else:
        tmp = i

#定位图像的<table>,前提ele必须是TWTwNo/树名所在的所有td
firstTWTwNo_Table = ele[0].xpath('../../following-sibling::table[@width="1410"]')[0]
#                TR  TD a  img   #表示第三行的TD里面的东西
firstTWTwNo_Table[0][3][0][0].attrib['src']


