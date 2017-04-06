#!/usr/bin/python
#! - * - coding: utf-8 - * -

import requests
import time
import os
import re, urllib
import urllib2
from bs4 import BeautifulSoup
from socket import error as SocketError
import errno
import json
from selenium import webdriver
from sys import argv

class PantipCrawler:

    def __init__(self, username='temp', password='temp'):
        self.username = username
        self.password = password
        self.base_url = "http://pantip.com"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override","Mozilla/5.0")
        self.browser = webdriver.Firefox(profile)
        self.cookies = requests.get(self.base_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0'}, verify=False).cookies

    def get(self, url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0',
              'Host': 'pantip.com',
              'Referer': 'http://pantip.com/',
              'Cache-Control': 'max-age=0'}):
        return requests.get(self.base_url + url, cookies=self.cookies, headers=headers, verify=False)

    def get_link_from_tag(self, tag):
        try:
            links = []
            url = "http://www.pantip.com/tag/"+tag
            self.browser.get(url)
            soup = self.browser.page_source.encode('utf-8')
            soup = BeautifulSoup(soup)
            productDivs = soup.findAll('div', attrs={'class' : 'post-item-title'})
            folder = '/home/melpst/Web Crawler/'+tag
            if not os.path.exists(folder):
                os.makedirs(folder)
            for div in productDivs:
                link = div.find('a')['href']
                links.append(link)
            i = 1
            for link in links:
                print link
                is_ads = re.match('//ads.*', link)
                if not is_ads:
                    print "get link from tag >> get comment"                
                    self.get_comments(link, folder)
                    print i
                    i += 1
                
        except requests.exceptions.RequestException as e:
            print e

    def get_comments(self, topic, folder):
        comments = []
        try:
            url = "http://www.pantip.com"+topic
            self.browser.get(url)
            soup = self.browser.page_source.encode('utf-8')
            soup = BeautifulSoup(soup)
            for link in soup.select('div.display-post-story'):
                message = link.text
                message = message.replace("\r","")
                message = message.replace("\n","")
                message = message.replace("\t","")
                message = message.strip();
                comments.append(message)
            topic = topic.replace("/topic/","")
            print topic
            self.write_file(comments, topic, folder)
            print "finished topic"

        except requests.exceptions.RequestException as e:
            print e

    def write_file(self, comments, title, folder):
        with open(folder+'/CommentLog_'+title+'.txt', 'w') as f:
            i = 1
            for comment in comments:
                f.write('Comment '+str(i)+' :\n')
                f.write(comment.encode('utf-8')+"\n")
                f.write('================================\n')
                i+=1


# print "Crawler Bot initializing...\n===============================\n\n"

if __name__ == '__main__':
    script, tag = argv
    bot = PantipCrawler()

    bot.get_link_from_tag(tag)
