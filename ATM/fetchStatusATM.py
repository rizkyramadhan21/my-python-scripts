#-*- coding: utf-8 -*-
#---------------------------------------
#!/usr/bin/python
#---------------------------------------
# fetchStatusATM.py
# (c) Rizky Ramadhan, June 2018
# to be used with telegram-bot plugin
#---------------------------------------
# script name followed by space and TID
# usage: python statusATM.py 1234567
#---------------------------------------

import urllib2
import sys
from bs4 import BeautifulSoup
from helperlibrary import *


def fetchStatusATM():
	# Specify the url:
	TID = sys.argv[1]
	alamatURL = statusAtmURL + '?ATM_NUM=' + TID

	try:
		page = urllib2.urlopen(alamatURL, timeout=4)

	except urllib2.URLError:
		print ("*Oops!*\n_Connection error, failed to load ATMPro data_")

	else:
		soup  = BeautifulSoup(page, 'html.parser')
		table = soup.find('table', attrs={'class': 'fancy'})

		if table is None:
			print('_No ATM ID matched with your search criteria_')
		else:
			cleanHTML = cleanUpHTML(table)
			getTextHTML = getHTMLtext(cleanHTML)
			mdStyles = markdownBotAPI(getTextHTML)
			gStatusATM = headerHTML(mdStyles)
			print gStatusATM


fetchStatusATM()
