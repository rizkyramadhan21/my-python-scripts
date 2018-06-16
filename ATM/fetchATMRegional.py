#-*- coding: utf-8 -*-
#---------------------------------------
#!/usr/bin/python
#---------------------------------------
# fetchATMRegional.py
# © Rizky Ramadhan, June 2018
# to be used with telegram-bot plugin
# usage: python fetchATMRegional.py
#---------------------------------------

import urllib2
import pandas as pd
import os, sys
from bs4 import BeautifulSoup
from helperlibrary import *


def fetchATMRegional():
	# Specify the url:
	alamatURL = dashboardBR + '?REGID=' + regID + '&REGNAME=' + regName
	fileName  = "ATMRegional.csv"

	try:
		page = urllib2.urlopen(alamatURL, timeout=4)

	except urllib2.URLError:
		print ("*Oops!*\n_Connection error, failed to load ATMPro data_")

	else:
		soup  = BeautifulSoup(page, 'html.parser')
		table = soup.find('table', attrs={'class': 'fancy'})

		if table is None:
			print('_No table class matched with your search criteria_')

		else:
			html = cleanUpHTML(table)
			html = fixBroken(html)

			# Make temp. output file "ATMRegional.csv":
			file = open(outputDIR + fileName, "w")
			file.write(html) 
			file.close()

			dataset   = pd.read_csv(outputDIR + fileName, usecols=[0,1,2,3,4])
			tabledata = dataset.to_csv(header=None, index=False)
			tabledata = cleanUpNames(tabledata)
			lastdata  = tabledata.title()
			os.system("rm " + outputDIR + fileName)

			f = open(outputDIR + fileName, "w")
			f.write(lastdata)
			f.close()
			
			# My fastest solution is using bash script for execute LOAD DATA LOCAL INFILE (CSV):
			os.system('cd ' + outputDIR +'\n' + sqlInit + '\n' + sqlEmp + '\n' + sqlExec + '\n' + sqlExit)


def cleanUpHTML(html):
	# membuat 1 kata kunci utama = strKey dan print teks:
	html = str(html).replace('-cdrp.pl?AREA_ID=', '><"/><"">strKey')
	html = BeautifulSoup(html, "lxml")
	html = html.findAll('td')
	html = [i.text for i in html]
	return html

def fixBroken(strTableKey):
	# fixing broken HTML:
	strTableKey = str(strTableKey).replace('strKey', "\nstrKeyu'")
	strTableKey = str(strTableKey).replace('">', "', u'")
	strTableKey = str(strTableKey).replace("u''","u'0'")
	strTableKey = str(strTableKey).replace(" u'"," ")
	strTableKey = str(strTableKey).replace("'","")
	strTableKey = str(strTableKey).replace("^u", "")
	strTableKey = str(strTableKey).replace("[u1, "+ firstBranch +", \n","A, B, C, D, E\n")
	strTableKey = str(strTableKey).replace("strKeyu","")
	strTableKey = str(strTableKey).replace(", ",",")
	return strTableKey

fetchATMRegional()
