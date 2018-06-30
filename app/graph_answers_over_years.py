#!/usr/bin/python

from datetime import datetime
import matplotlib.pyplot as plt

class GraphAnswersOverYears():

	def __init__(self, profile_username):
		self.profile_username = profile_username

	def plotter(self, year_time_data):
		count_by_year = {}
		for dt in year_time_data:
			answer_dt = datetime.strptime(dt, '%b %d, %Y')
			answer_year = int(answer_dt.year)
			if count_by_year.get(answer_year, None) is not None:
				count_by_year[answer_year] = count_by_year[answer_year] + 1
			else:
				count_by_year[answer_year] = 1

		count_by_year = [(k,v) for k,v in count_by_year.iteritems()]
		count_by_year = sorted(count_by_year, key=lambda x: x[0])

		uv_xaxis = zip(*count_by_year)[0]
		uv_yaxis = zip(*count_by_year)[1]

		plt.bar(range(len(uv_yaxis)), uv_yaxis, align='center')
		plt.xticks(range(len(uv_xaxis)), uv_xaxis)

		ax = plt.subplot()
		ctr = 0
		for i in ax.patches:
			# get_x pulls left or right; get_height pushes up or down
			ax.text(i.get_x()-0.01, i.get_height()+.5, str(uv_yaxis[ctr]), fontsize=9, color='dimgrey')
			ctr = ctr + 1

		title = self.profile_username.replace("_", " ") + '\'s Quora Answer Activity'
		plt.title(title, fontsize=18)
		plt.xlabel('Year', fontsize=8)
		plt.ylabel('No. of Answers', fontsize=8)
		#plt.show()
		#plt.savefig('foo.png', bbox_inches='tight')
		filename = self.profile_username + '_Answers_By_Year.png'
		plt.savefig('./data/'+filename)
		plt.close()