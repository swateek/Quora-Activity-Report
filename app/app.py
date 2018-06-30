#!/usr/bin/python

import time
import csv
import os
from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from make_graphs import MakeGraphs


class FetchAnswersCSV():

	def __init__(self):
		self.my_email = 'MY_EMAIL'
		self.my_password = 'MY_PASSWORD'

		############################## DO NOT MODIFY ANYTHING BELOW THIS LINE ##############################

		self.driver = None
		self.wait = ui.WebDriverWait(self.driver,10)
		self.my_profile_url = ''
		self.profile_username = ''
		self.days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
		self.today = datetime.today()

	def login(self):
		# Login
		self.driver = webdriver.Firefox()
		self.driver.maximize_window()
		self.driver.get("https://www.quora.com/")
		login = self.driver.find_element_by_xpath("//input[@placeholder='Email']")
		login.send_keys(self.my_email)
		login.send_keys(Keys.TAB)
		password = self.driver.find_element_by_xpath("//input[@placeholder='Password']")
		password.send_keys(self.my_password)
		password.send_keys(Keys.TAB)
		submit_button = self.driver.find_element_by_xpath("//input[@value='Login']")
		submit_button.send_keys(Keys.RETURN)
		self.wait.until(lambda driver: self.driver.find_element_by_xpath('//*[@class="right_contents"]/div[2]/span/div/a'))
		#driver.get("https://www.quora.com/profile/Swateek-Jena/") # Go to Profile
		hover_menu = self.driver.find_element_by_xpath('//*[@class="right_contents"]/div[2]/span/div/a')
		hover_menu.click()
		self.wait.until(lambda driver: self.driver.find_element_by_xpath('//*[@class="hover_menu_item"]'))
		profile_link = self.driver.find_element_by_xpath('//*[@class="hover_menu_item"]')
		profile_link.click()
		self.my_profile_url = self.driver.current_url
		self.profile_username = self.my_profile_url[8:].split('/')[2]
		

	def click_on_more_btn(self):
		# Exapnd questions
		question_block = self.driver.find_elements_by_class_name('ui_qtext_more_link')
		for block in question_block:
			try:
				block.click()
			except Exception as e:
				print e

	def infinite_scroll(self):
		# Scroll to the end and also click 'MORE' button
		SCROLL_PAUSE_TIME = 8
		# Get scroll height
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:
		    # Scroll down to bottom
		    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		    # Wait to load page
		    time.sleep(SCROLL_PAUSE_TIME)
		    self.click_on_more_btn()

		    # Calculate new scroll height and compare with last scroll height
		    new_height = self.driver.execute_script("return document.body.scrollHeight")
		    if new_height == last_height:
		        break
		    last_height = new_height

	def format_date(self, date):
		new_dt = date.replace('Answered ', '')
		new_dt = new_dt.replace('Updated ', '')

		if new_dt.strip() in self.days_of_week: # get particular date from day of week
			delta_day = self.days_of_week.index(new_dt) - self.today.isoweekday()
			if delta_day >= 0: 
				delta_day -= 7 # go back 7 days
			new_dt = self.today + timedelta(days=delta_day)
			new_dt = new_dt.strftime('%b %d, %Y')
		elif "," not in new_dt: # add current year to date
			new_dt = new_dt + ', ' + str(self.today.year)
			pass
		else: # do nothing
			pass

		return str(new_dt.strip()).encode('utf-8')

	def format_upvotes(self, upvotes):
		up = upvotes.replace('Upvotes', '').strip()
		up = up.replace('Upvote', '').strip()

		if 'k' in up:
			up = up.replace('k', '')
			up = float(up) * 1000
			up = up.replace(',', '')

		return str(up).encode('utf-8')

	def fetch_answer_to_csv(self):
		my_quora_answers = []
		self.wait.until(lambda driver: self.driver.find_element_by_xpath('//*[@class="pagedlist_item"]'))
		page_items = self.driver.find_elements_by_xpath('//*[@class="pagedlist_item"]')
		for item in page_items:
			try:
				link = item.find_element_by_xpath('.//*/span/span/div/div/div/a').get_attribute('href') + '/answer/' + self.profile_username
				question = item.find_element_by_xpath('.//*/span/span/div/div/div/a').text
				upvotes = item.find_element_by_xpath('.//*/div/div/div[2]/div[2]/span/a/div/span').get_attribute('innerHTML')
				answered_date = item.find_element_by_xpath('.//*/span/span/div[2]/div/div/div/div[2]/span/div/div/span/a').get_attribute('innerHTML')
				itm = {}
				itm['question'] = question.encode('utf-8')
				itm['link'] = link.encode('utf-8')
				itm['upvotes'] = self.format_upvotes(upvotes)
				itm['date'] = self.format_date(answered_date)
				my_quora_answers.append(itm)
			except Exception as e:
				print e

		here = os.path.dirname(os.path.realpath(__file__))
		subdir = "data"
		csv_file_name = self.profile_username.replace("-", "_") + "_answers.csv"
		filepath = os.path.join(here, subdir, csv_file_name)
		keys = my_quora_answers[0].keys()
		with open(filepath, 'wb') as output_file:
		    dict_writer = csv.DictWriter(output_file, keys)
		    dict_writer.writeheader()
		    dict_writer.writerows(my_quora_answers)


	def run_test(self):
		self.login()
		self.click_on_more_btn()
		self.fetch_answer_to_csv()
		self.driver.close()
		make_graphs = MakeGraphs(self.profile_username)
		make_graphs.run()

	def run(self):
		self.login()
		self.infinite_scroll()
		self.fetch_answer_to_csv()
		self.driver.close()
		make_graphs = MakeGraphs(self.profile_username)
		make_graphs.run()

	def graph_test(self):
		make_graphs = MakeGraphs('Swateek_Jena')
		make_graphs.run()


FetchAnswersCSV().run()