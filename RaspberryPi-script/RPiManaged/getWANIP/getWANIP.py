#!/usr/bin/python3

#
#
#

###
### import package:
###
import requests

from bs4 import BeautifulSoup
import bs4

import os
import sys

##import spiderutils

###
### global variables:
###

###
### funciton define:
###
def getHTMLText( URL, Params=None, Timeout=30):
	try:
		r = requests.get( URL, params=Params, timeout=Timeout )
		r.raise_for_status()
		r.encoding = r.apparent_encoding

		return r.text
	except:
		return None
def getIPstr( srcIP ):
	dst = ''
	for i in range( len(srcIP) ):
		if srcIP[i].isdigit() or srcIP[i]=='.' :
			dst = dst + srcIP[i]
		else:
			pass
	#rof
	return dst
#fed function


def main():
	#htmlData = getHTMLText()
	kv = { 'wd':'IP' }
	htmlData = getHTMLText("http://www.baidu.com/s", Params=kv)
	#print (htmlData)
	print ("get HTML text OK!")

	## -- 提取body：
	bodyData = htmlData[htmlData.find("<body"):htmlData.find("</body")]
	bodyData = '<html><head></head>' + bodyData + '</body></html>'
	## 这里可以输出 bodyData 一下
	
	BodySoup = BeautifulSoup( bodyData, "html.parser" )
	
	## -- 提取主要段落：
	result = BodySoup.find_all( 'div', attrs='result-op c-container' )
	# print( type(result) )
	
	result = list(result)  # turn set to list type
	RequestsResult = result[0]
	
	Str = "%s" % RequestsResult.span
	# print (Str)
	## >>> <span class="c-gap-right">本机IP: 1x2.1x3.1x5.2xx</span>
	
	## 注意，
	## Str 必须是正确的值才好进入下一步的字符串处理。
	## 这边是在解释器模式下的测试+代码记录在CSDN上，
	## 所以实际情况有一定的可能性不会那么刚好在第一个span标签就是上面所示的字符串

	## 提取 IP 值：
	ipSoup = BeautifulSoup ( Str, "html.parser" )
	
	ipStrKV = ipSoup.span.string
	# print ipStrKV
	## 本机IP: 1x2.1x3.1x5.2xx
	## >>> ipStrKV
	## '本机IP:\xa01x2.1x3.1x5.2xx'
	## >>>
	##
	
	( ipKey, ipValue) = ipStrKV.split(":") 	

	ipStr = getIPstr( ipValue )
	print ( ipStr )

	sys.exit(0)
#fed main function



if __name__ == "__main__":
	main()
#fi

