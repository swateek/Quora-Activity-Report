#!/usr/bin/python

import csv
import os
from datetime import datetime
from graph_answers_over_years import GraphAnswersOverYears
from graph_upvotes_over_years import GraphUpvotesOverYears
from graph_low_upvote_answers import GraphLowUpvoteAnswers

class MakeGraphs():

	def __init__(self, profile_username):
		self.answers_over_years = GraphAnswersOverYears(profile_username)
		self.upvotes_over_years = GraphUpvotesOverYears(profile_username)
		self.low_upvote_answers = GraphLowUpvoteAnswers(profile_username)
		self.profile_username = profile_username

	def run(self):

		year_time_data = []
		year_upvote_data = {}
		low_upvotes_arr = ['0', '1', '2', '3', '4', '5', '6'];
		low_upvote_answer = {}

		current_path = os.path.abspath(os.path.dirname(__file__))
		csv_file = os.path.join(current_path, "data/"+self.profile_username+"_answers.csv")
		with open(csv_file, 'rb') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				year_time_data.append(row['date'])
				self.__handle_upvote_by_year_data(row, year_upvote_data)
				upvotes = row['upvotes'].replace(",", "")
				if row['upvotes'] in low_upvotes_arr:
					if low_upvote_answer.get(upvotes, None) is not None:
						low_upvote_answer[upvotes] = low_upvote_answer[upvotes] + int(1)
					else:
						low_upvote_answer[upvotes] = int(1)

		self.answers_over_years.plotter(year_time_data)
		self.upvotes_over_years.plotter(year_upvote_data)
		self.low_upvote_answers.plotter(low_upvote_answer)

	def __handle_upvote_by_year_data(self, row, year_upvote_data):
		answer_dt = datetime.strptime(row['date'], '%b %d, %Y')
		answer_year = int(answer_dt.year)
		upvotes = row['upvotes'].replace(",", "")

		if year_upvote_data.get(answer_year, None) is not None:
			year_upvote_data[answer_year] = year_upvote_data[answer_year] + int(upvotes)
		else:
			year_upvote_data[answer_year] = int(upvotes)

		return True

#MakeGraphs().run()