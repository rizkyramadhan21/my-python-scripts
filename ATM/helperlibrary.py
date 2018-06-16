# -*- coding: utf-8 -*-
#!/usr/bin/python
#----------------------------------------------
# helperlibrary.py
# readConfig © Jansen A. Simanullang
# © Rizky Ramadhan, Juni 2018
#----------------------------------------------
# Python usage:
#
# from helperlibrary import function_name
#----------------------------------------------

import urllib2
import os, sys, configparser
from bs4 import BeautifulSoup
from helperlibrary import *

#---------------------------------------------------------------------------------------------
# constanta: config.ini
scriptDIR = os.path.dirname(os.path.realpath(__file__))
configPath = (scriptDIR + "/conf/config.ini")
outputDIR  = (scriptDIR + "/conf/.output/")
Config = configparser.ConfigParser()
Config.read(configPath)

def readConfig(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
#---------------------------------------------------------------------------------------------

# Read config: config.ini | please specify the url, branch, etc (in file):
statusAtmURL = readConfig("Atmpro")['statusatm']
dashboardBR = readConfig("Atmpro")['dashboardcabang']
regID = readConfig("Atmpro")['region_id']
regName = readConfig("Atmpro")['region_name']
firstBranch = readConfig("Atmpro")['first_branch']
myhost = readConfig("Mysql")['myhost']
myuser = readConfig("Mysql")['myuser']
mypass = readConfig("Mysql")['mypass']
myDB = readConfig("Mysql")['mydb']
regionTable = readConfig("Mysql")['region_table']


# MySQL Bash, cause pymysql always ERROR to import LOCAL in FILE (CSV)
# ISSUE: https://github.com/PyMySQL/PyMySQL/issues/62
sqlInit = '    mysql --host=' + myhost + ' --user=' + myuser + ' --password=' + mypass + ' ' + myDB + '<< EOF'
sqlEmp  = 'TRUNCATE atmregional;'
sqlExec	= "LOAD DATA LOCAL INFILE 'ATMRegional.csv' INTO TABLE " + regionTable + " FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';"
sqlExit	= 'EOF'

strHeaderLine = "\n--------------------------------------------------------------------------"

#---------------------------------------------------------------------------------------------
def cleanUpHTML(html):
	# fixing broken HTML:
	html = str(html).replace("\n", "")
	html = str(html).replace("</td></tr>", "\n")
	html = str(html).replace("<th colspan", "\n<th colspan")
	html = str(html).replace("</b></td><td>", ": ")
	html = str(html).replace("</td><td bgcolor=", ": </td><td bgcolor=")
	html = str(html).replace("</th></tr><tr>", "\n</th></tr><tr>")
	html = str(html).replace('<tr><td align="center" bgcolor="#00FF40"','\n<tr><td')
	html = str(html).replace('<table border="0" cellspacing="0" class="fancy"><tr>', '')
	return html
#---------------------------------------------------------------------------------------------
def getHTMLtext(html):
	# getText from HTML tag:
	html = BeautifulSoup(html, "lxml")
	html = html.text.encode('utf-8').strip()
	return html
#---------------------------------------------------------------------------------------------
def markdownBotAPI(markdownText):
	# markdown style telegram bot API:
	markdownText = str(markdownText).replace(": OK", ": *OK*")
	markdownText = str(markdownText).replace(": FAIL", ": *FAIL*")
	markdownText = str(markdownText).replace(": LOW", ": *LOW*")
	markdownText = str(markdownText).replace(": OUT", ": *OUT*")
	markdownText = str(markdownText).replace("_", " ")
	markdownText = str(markdownText).replace("ATM ID","ATM ID: ")
	markdownText = str(markdownText).replace("Kanwil", "Kanwil: ")
	markdownText = str(markdownText).replace("+62 ", "0")
	markdownText = str(markdownText).replace(": :", ":")
	return markdownText
#---------------------------------------------------------------------------------------------
def headerHTML(tableDiv):
	# just for good looking - make headerline for every subTitle:
	tableDiv = str(tableDiv).replace("General Info", "*General Info*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Info Mesin", "*Info Mesin*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Jarkom", "*Jarkom*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Paramerer", "*Paramerer*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Trx. Info", "*Trx. Info*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Hardware Info", "*Hardware Info*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Cassette Info", "*Cassette Info*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("Parameter", "*Parameter*" + strHeaderLine)
	tableDiv = str(tableDiv).replace("PIC Call Tree", "\n*PIC Call Tree*" + strHeaderLine)
	return tableDiv
#---------------------------------------------------------------------------------------------
def cleanUpNames(strLocation):
	strLocation = str(strLocation).replace("KC ", "")
	strLocation = str(strLocation).replace("KANCA ", "")
	strLocation = str(strLocation).replace("JKT ", "")
	strLocation = str(strLocation).replace("Jakarta ", "")
	strLocation = str(strLocation).replace("JAKARTA ", "")
	return strLocation
#---------------------------------------------------------------------------------------------
