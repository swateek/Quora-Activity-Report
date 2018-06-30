#!/usr/bin/python

from datetime import datetime
import matplotlib.pyplot as plt

class GraphUpvotesOverYears():

	def __init__(self, profile_username):
		self.profile_username = profile_username

	def plotter(self, year_upvote_data):
		year_upvote_data = [(k,v) for k,v in year_upvote_data.iteritems()]
		year_upvote_data = sorted(year_upvote_data, key=lambda x: x[0])

		uv_xaxis = zip(*year_upvote_data)[0]
		uv_yaxis = zip(*year_upvote_data)[1]

		plt.bar(range(len(uv_yaxis)), uv_yaxis, align='center')
		plt.xticks(range(len(uv_xaxis)), uv_xaxis)

		ax = plt.subplot()
		ctr = 0
		for i in ax.patches:
			# get_x pulls left or right; get_height pushes up or down
			ax.text(i.get_x()-0.01, i.get_height()+.5, str(uv_yaxis[ctr]), fontsize=9, color='dimgrey')
			ctr = ctr + 1

		title = self.profile_username.replace("_", " ") + '\'s Answer Upvotes'
		plt.title(title, fontsize=18)
		plt.xlabel('Year', fontsize=8)
		plt.ylabel('No. of Upvotes', fontsize=8)
		#plt.show()
		#plt.savefig('foo.png', bbox_inches='tight')
		filename = self.profile_username + '_Upvotes_By_Year.png'
		plt.savefig('./data/'+filename)
		plt.close()