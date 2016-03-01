#!/usr/bin/python
#! - * - coding: utf-8 - * -

import requests
import os
import json
import re, urllib
from sys import argv


def ssense(comment):
	url = "http://www.sansarn.com/api/ssense.php?key=02f7460db97cad58c6651a6bec7c792b&text="
	if(not (comment=="")):
		full_url = url+comment
		#print (full_url)
		req = requests.get(full_url)
		react = json.loads(req.content.decode("utf-8") )
		return react['sentiment']['polarity']

if __name__ == '__main__':
	script, topic = argv
	txt = open("/home/melpst/Web Crawler/รถไฟฟ้า_(BTS)/CommentLog_"+topic+".txt")
	
	comments = txt.read()
	comments = re.sub(r"Comment [0-9]* :", "", comments)
	comments = comments.split("================================")
	
	for i in range(0, len(comments)):
	#for comment in comments:
		#print (comment)
		#print (i)
		#polarity = ssense(comment)
		polarity = ssense(comments[i])
		if(polarity == "positive"):
			print (str("positive"))
		elif(polarity == "negative"):
			print ("negative")
		else:
			print ("null")
			