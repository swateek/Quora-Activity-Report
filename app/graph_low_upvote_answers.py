#!/usr/bin/python

from datetime import datetime
import matplotlib.pyplot as plt

class GraphLowUpvoteAnswers():

	def __init__(self, profile_username):
		self.profile_username = profile_username

	def plotter(self, low_upvote_answer):
		low_upvote_answer = [(k,v) for k,v in low_upvote_answer.iteritems()]
		low_upvote_answer = sorted(low_upvote_answer, key=lambda x: x[0])

		uv_xaxis = zip(*low_upvote_answer)[0]
		uv_yaxis = zip(*low_upvote_answer)[1]

		plt.bar(range(len(uv_yaxis)), uv_yaxis, align='center')
		plt.xticks(range(len(uv_xaxis)), uv_xaxis)

		ax = plt.subplot()
		ctr = 0
		for i in ax.patches:
			# get_x pulls left or right; get_height pushes up or down
			ax.text(i.get_x()-0.01, i.get_height()+.5, str(uv_yaxis[ctr]), fontsize=9, color='dimgrey')
			ctr = ctr + 1

		title = self.profile_username.replace("_", " ") + '\'s Low Upvoted Answers'
		plt.title(title, fontsize=18)
		plt.xlabel('Upvotes', fontsize=8)
		plt.ylabel('No. of Answers', fontsize=8)
		#plt.show()
		#plt.savefig('foo.png', bbox_inches='tight')
		filename = self.profile_username + '_Low_Upvoted_Answers.png'
		plt.savefig('./data/'+filename)
		plt.close()