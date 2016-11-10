# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib
import re
import os

sd_targetDir = r"/Users/Ivy11D/Desktop/IR/webpage"  #文件保存路径
def destFile(sd_path):  #e.g sd_path='images/lsxy.jpg'
    if not os.path.isdir(sd_targetDir):  
        os.mkdir(sd_targetDir)  
    sd_pos = sd_path.rindex('/')  
    sd_abPath = os.path.join(sd_targetDir, sd_path[sd_pos+1:len(sd_path)])  
    return sd_abPath  
    
def getpageConent(sd_url):
    sd_page = urllib.request.urlopen(sd_url)
    sd_pageContent = sd_page.read()
    return sd_pageContent

def getImgs(sd_pageContent,sd_urlRoot):
    sd_reg = r'src="([^\s]*?(jpg|png|gif))"'
    sd_imgre = re.compile(sd_reg)
    sd_imglist = re.findall(sd_imgre,str(sd_pageContent))
    for sd_imgurl, sd_t in sd_imglist:
        sd_imgurl = sd_urlRoot + sd_imgurl
        sd_imgPath = destFile(sd_imgurl)
        urllib.request.urlretrieve(sd_imgurl,sd_imgPath)

sd_url = "http://history.bnu.edu.cn/"
sd_pageContent = getpageConent(sd_url)
getImgs(sd_pageContent,sd_url)