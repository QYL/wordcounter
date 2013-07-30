#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ---------------------------------------
# a production of Qiu Yuanle(aka Le.py) #
# Created on 2013-5-26 01:56:03         #
# ---------------------------------------

import re
import urllib
import codecs
import os
import os.path

BASE_URL = 'http://tech2ipo.com/'

def get_author_list():
	try:
		author_list = codecs.open("C:\\author.txt","r","utf-8-sig").read().split("#")
	except:
		print "Error#798CD68\n"
		q = input('''Failed to open author.txt.\nPlease create a txt file named author in C:\ and write the author's name in it.\nIf there are more than one name please seperate them by #.\nPress any key to quit.
			''')
	return author_list

AUTHOR_LIST =  get_author_list()

def article_id(start, end):
    article_id = []
    for i in range(int(start), int(end)+1):
        article_id.append(i)
    return article_id

def make_url(article_id): #need a list
    url=[]
    for i in article_id:
        url_item = BASE_URL + str(i)
        url.append(url_item)
    return url

def get_webpage(url):
    page_for_article = urllib.urlopen(url).read().decode('utf8')
    page_for_at = urllib.urlopen(url).read()
    return page_for_article, page_for_at

def get_aticle(page_for_article):
    reg_art = r'(?s)(?=<section id="article-content">).*?(?<=<div class="articleTag">)'
    if re.findall(reg_art, page_for_article):
    	article = re.findall(reg_art, page_for_article)[0]
    else:
    	article = None
    return article

def get_author(page_for_at):
    reg_author =r'class="author">.*?</'
    if re.findall(reg_author, page_for_at):
    	author = str(re.findall(reg_author, page_for_at)[0]).split(">")[1].split("<")[0]
    	#print author
    else:
    	author = None
    return author

def get_title(page_for_at):
    reg_title=r'class="title".*?</'
    title = (str(re.findall(reg_title, page_for_at)[0]).split(">")[1].split("<")[0]).decode('utf8')
    return title

def get_time(page_for_at):
    reg_time = r'(\d{2}|\d{4})(?:\-)?([0]{1}\d{1}|[1]{1}[0-2]{1})(?:\-)?([0-2]{1}\d{1}|[3]{1}[0-1]{1})(?:\s)?([0-1]{1}\d{1}|[2]{1}[0-3]{1})(?::)?([0-5]{1}\d{1})(?::)?([0-5]{1}\d{1})'
    time = re.findall(reg_time, page_for_at)[0]
    ymd = time[0]+"-"+time[1]+"-"+time[2]
    hms = time[3]+":"+time[4]+":"+time[5]
    time = ymd+"@"+hms
    return time

def word_count(item):
    cn = re.compile(u'(?:<.*?>)|([\u4e00-\u9fa5]+)|([a-zA-Z0-9_-]+)')
    words = 0
    for chr in cn.finditer(item):
        zh, en = chr.groups()
        if zh:
            words += len(zh.encode('utf-8'))/3
        if en:
            words += 1  
    return words

def make_file(author,title,time,article_count):
    txt = codecs.open("C:\\"+author+".txt","a","utf8")
    items = []
    items.append(author)
    items.append(title)
    items.append(time)
    items.append(article_count)
    for i in items:
    	if not("@" in str(i)):
            txt.write(str(i).replace(" ", "")+" ")
        else:
        	txt.write(str(i).replace("@", " ")+" ")
    txt.write("\r\n")
    txt.close()

def count(start,end,author):
	
    print u'正在统计......'
    #print start,end,author
    article_id_list = article_id(start,end)
    #print article_id_list,type(article_id_list)
    url_list = make_url(article_id_list)
    #print url_list,type(url_list)
    ip = 0
    TITLE_COUNT = 0
    TOTAL_WORDS = 0
    for i in range(0, len(url_list)):
        page_for_article, page_for_at = get_webpage(url_list[i])
        try:
            author_get = get_author(page_for_at)
            #print u"author_get:"+author_get
        except Exception, e:
            pass
        if author_get == author:
            title = get_title(page_for_at)
            time = get_time(page_for_article)
            article = get_aticle(page_for_article)
            article_count = word_count(article)

            TITLE_COUNT = TITLE_COUNT + word_count(title)
            TOTAL_WORDS = TOTAL_WORDS + article_count
            ip = ip+1
            print u'完成',ip,u'篇'
            make_file(author,title,time,article_count)
            
        else:
            pass
    
    txt = codecs.open("C:\\"+author+".txt","a","utf8")
    txt.write(u"标题总字数："+str(TITLE_COUNT)+" "+u"正文总字数："+str(TOTAL_WORDS)+"\n\n")
    txt.close()
    print "Done with "+author+"!"
    #print "Done."
if __name__ == '__main__':
	print u'''
		     WORD COUNTER FOR TECH2IPO
		     
	    # --------------------------------------#
            # a production of Qiu Yuanle(aka Le.py) #
            # Created on 2013-5-25 13:56:03         #
            # --------------------------------------#
	'''
	import sys 
	reload(sys) 
	sys.setdefaultencoding('utf8')

	start_id = input("please enter the start id:")
	end_id = input("please enter the end id:")

	#print "AUTHOR_LIST:",AUTHOR_LIST

	for author_i in range(0,len(AUTHOR_LIST)):
		author = AUTHOR_LIST[author_i]
		#print author
		if os.path.isfile("C:\\"+author+".txt"): 
			os.remove("C:\\"+author+".txt")
		count(start_id,end_id,author)
		
	quit = input("Press any key to quit.")


