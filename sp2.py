import urllib
import re
import os

sd_urlRoot = "http://cist.bnu.edu.cn/"  # the target website
sd_targetDir = r"/Users/Ivy11D/Desktop/IR/webpage"  #文件保存路径
def destFile(sd_path): 
    if not os.path.isdir(sd_targetDir):  
        os.mkdir(sd_targetDir)
    sd_urldir = sd_path[len(sd_urlRoot):len(sd_path)]
    sd_urldirlist = sd_urldir.split('/')
    sd_abPath = sd_targetDir
    for sd_urldirelem in sd_urldirlist[0:len(sd_urldirlist)-1]:
        sd_abPath = os.path.join(sd_abPath,sd_urldirelem)
        if not os.path.isdir(sd_abPath):  
            os.mkdir(sd_abPath)
    sd_abPath = os.path.join(sd_abPath,sd_urldirlist[len(sd_urldirlist)-1])    
    return sd_abPath  
    
def getCss(sd_pageContent,sd_url):
    sd_reg = r'href="([^\s]*?(.css))"'
    sd_cssre = re.compile(sd_reg)
    sd_cssList = re.findall(sd_cssre,str(sd_pageContent))
    sd_cssNewList = getNormalUrls(sd_cssList,sd_url)
    for sd_cssUrl in sd_cssNewList:
        sd_cssPath = destFile(sd_cssUrl)
        try:
            urllib.request.urlretrieve(sd_cssUrl,sd_cssPath)
        except urllib.error.HTTPError:
            print("The css file '",sd_cssUrl,"' not Found.")  
           
def getImgs(sd_pageContent,sd_url):
    sd_reg = r'src="([^\s]*?(jpg|png|gif))"'
    sd_imgre = re.compile(sd_reg)
    sd_imgList = re.findall(sd_imgre,str(sd_pageContent))
    sd_imgNewList = getNormalUrls(sd_imgList,sd_url)
    for sd_imgurl in sd_imgNewList:
        sd_imgPath = destFile(sd_imgurl)
        try:
            urllib.request.urlretrieve(sd_imgurl,sd_imgPath)
        except urllib.error.URLError:
            print("The image '",sd_imgurl,"' not Found.")  
            
def getNormalUrls(sd_urlList,sd_url):
    sd_newUrlList = []
    for sd_urlLink,sd_t in sd_urlList:
        if sd_urlLink.startswith('http://',0,len(sd_urlLink)):
            if sd_urlLink.find(sd_urlRoot,0,len(sd_urlLink)) != -1  and sd_urlLink.find != sd_urlRoot + '#':
                sd_newUrlList.append(sd_urlLink) 
        else :
            sd_newUrlLink = urllib.parse.urljoin(sd_url,sd_urlLink)
            sd_newUrlList.append(sd_newUrlLink)
    return sd_newUrlList
    
def getHtmls(sd_pageContent,sd_urlList,sd_url):
    sd_urlLink = re.compile(r'href="([^\s]*?(html))"')
    sd_htmlUrlList = set(re.findall(sd_urlLink,str(sd_pageContent)))
    sd_normalHtmlUrlList = getNormalUrls(sd_htmlUrlList,sd_url) # filter html url & make it as absolute url path
    sd_newUrlList = sd_urlList + sd_normalHtmlUrlList
    sd_urlList = sorted(set(sd_newUrlList),key=sd_newUrlList.index)
    return sd_urlList

def getpageConent(sd_url):
    sd_page = urllib.request.urlopen(sd_url)
    sd_pageContent = sd_page.read()
    return sd_pageContent

if __name__ == '__main__':
    sd_urlList = [] 
    sd_pageNumber = 0 
    sd_urlList.append(sd_urlRoot+"index.html")
    while sd_pageNumber < len(sd_urlList):
        print("sd_pageNumber:",sd_pageNumber)
        print("len(sd_urlList):",len(sd_urlList))
        sd_url = sd_urlList[sd_pageNumber]
        try:
            urllib.request.urlretrieve(sd_url,destFile(sd_url))
            sd_pageContent = getpageConent(sd_url)
            sd_lastSplashPos = sd_url.rindex('/')
            sd_url = sd_url[0:sd_lastSplashPos+1]
            getImgs(sd_pageContent,sd_url)         
            getCss(sd_pageContent,sd_url)
            sd_urlList = getHtmls(sd_pageContent,sd_urlList,sd_url)
        except urllib.error.URLError:
            print("The page '", sd_url, "' not Found.")
        sd_pageNumber += 1
