#-*- coding: utf-8 -*-
#------------------------------------------------
#!/usr/bin/python
# © Rizky Ramadhan, June 2018
# Backup XML Blogger post (Blogspot)
#------------------------------------------------

def backupBlogger():
	from selenium import webdriver
	from pyvirtualdisplay import Display
	import time

	# Set 0: None | 1: Visible
	display = Display(visible=0, size=(800, 600))
	display.start()

	browser = webdriver.Chrome()

	alamatURL = 'https://mail.google.com/mail/'
	alamatBlog = 'https://www.blogger.com/blogger.g?blogID=4855034551840349875#othersettings'

	browser.get(alamatURL)

	browser.find_element_by_id("identifierId").send_keys("yourGoogleAccount")
	browser.find_element_by_id("identifierNext").click() #usernameGoogle
	time.sleep(5)

	browser.find_element_by_css_selector('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys("yourGooglePassword")
	browser.find_element_by_id("passwordNext").click() #password
	time.sleep(5)

	browser.get(alamatBlog)
	time.sleep(5)

	browser.find_element_by_css_selector('#blogger-app > div.K3JSBVB-e-h > div.K3JSBVB-e-e > div > div.K3JSBVB-i-x > div.K3JSBVB-i-m > div.K3JSBVB-i-l > div.otherSettings > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td.K3JSBVB-J-wb > button:nth-child(2)').click()

	time.sleep(2)
	browser.find_element_by_css_selector('#blogger-app > div.blogg-dialog > div > div > div.K3JSBVB-l-l > div > div > div.K3JSBVB-l-i > div.K3JSBVB-l-e > button').click()
	time.sleep(10)

	browser.quit()
	display.stop()

	
backupBlogger()

