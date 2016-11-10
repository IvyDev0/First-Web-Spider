# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 23:35:05 2016

@author: Ivy11D
"""

import re
import urllib
import jieba
from bs4 import BeautifulSoup
from pagerank import *

sd_urlRoot = "http://cist.bnu.edu.cn/"
urllist_file = "url_list.txt"
simple_dic = {}   # 该网站所有文本的倒排索引词典 

graph = [[0 for col in range(700)] for row in range(700)]

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
    
def getHtmls(sd_pageContent,sd_urlList,sd_url,sd_pageNumber):
    sd_urlLink = re.compile(r'href="([^\s]*?(html))"')
    sd_htmlUrlList = set(re.findall(sd_urlLink,str(sd_pageContent)))
    sd_normalHtmlUrlList = getNormalUrls(sd_htmlUrlList,sd_url) # filter html url & make it as absolute url path
    buildGraph(sd_urlList,sd_normalHtmlUrlList,sd_pageNumber)
    sd_newUrlList = sd_urlList + sd_normalHtmlUrlList
    sd_urlList = sorted(set(sd_newUrlList),key=sd_newUrlList.index)
    return sd_urlList
 
def buildGraph(sd_urlList,sd_normalHtmlUrlList,sd_pageNumber):
    f = 0
    new = 0
    for i in range(0,len(sd_normalHtmlUrlList)):
        for j in range(0,len(sd_urlList)):
            if sd_normalHtmlUrlList[i]==sd_urlList[j]:
                f = 1
                graph[j][sd_pageNumber] = 1/len(sd_normalHtmlUrlList)
        if f==0:
            new += 1
            graph[sd_pageNumber+new][sd_pageNumber] = 1/len(sd_normalHtmlUrlList)


def getPageContent(sd_url):
    sd_page = urllib.request.urlopen(sd_url)
    sd_pageContent = sd_page.read().decode('utf-8')
    return sd_pageContent
# 获取网页文字内容
def getPageText(url):
    content = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(str(content),"lxml")
    for script in soup(["script", "style"]):
        script.extract()
    soup.prettify()
    return soup.get_text() 
   
def creat_quick_index(pagenum,url):
    text = getPageText(url)
    seg_text_list = list(jieba.cut(text,cut_all=True))
    word = list(set(seg_text_list)) # set去重  
    word.remove('')        
    f = 0
    for w in range(0,len(word)): 
        for k in simple_dic.keys(): 
            if word[w]==k: # 词典里已有这个词：
                simple_dic[k].append(pagenum)
                f = 1
                break
        if f==0: # 词典里还没有这个词：
            simple_dic[word[w]] = [pagenum] 
    print("Creating simple inverted index......")
  
       
def search_htmllist(queries):
    query_list = list(set(list(jieba.cut(queries,cut_all=True))))
    f = 0
    for query in query_list:
        for k in simple_dic.keys(): 
            if k == query:
                f = f+1
                return simple_dic[k]
    if f==0:
        return 0
        
        
if __name__ == '__main__':
    sd_pageNumber = 0 
    sd_urlList = []
    sd_urlList.append(sd_urlRoot+"index.html")
    while sd_pageNumber < len(sd_urlList):
        print("sd_pageNumber:",sd_pageNumber)
        print("len(sd_urlList):",len(sd_urlList))
        sd_url = sd_urlList[sd_pageNumber]
        
        try:
            sd_pageContent = getPageContent(sd_url)
            creat_quick_index(sd_pageNumber,sd_url)
            sd_lastSplashPos = sd_url.rindex('/')
            sd_url = sd_url[0:sd_lastSplashPos+1]
            sd_urlList = getHtmls(sd_pageContent,sd_urlList,sd_url,sd_pageNumber)            
            
        except urllib.error.URLError:
            print("The page '", sd_url, "' not Found.")
        sd_pageNumber += 1
        
    finalgraph = [[0 for col in range(sd_pageNumber)] for row in range(sd_pageNumber)]   
    for i in range(sd_pageNumber):
        for j in range(sd_pageNumber):
            finalgraph[i][j] = graph[i][j]
    ranking = powerIteration(finalgraph).sort_values(ascending=0)
    
    # 输入
    queries = input("Enter your input: ")
    while queries!='\n':
        print("Result: ")
        resultpage = search_htmllist(queries)
        if resultpage!=0:
            for pagenum in resultpage:
                for k in ranking.keys():
                    if int(k)==pagenum:
                        print(sd_urlList[pagenum])
        queries = input("Enter your input: ")
    print("End.")
