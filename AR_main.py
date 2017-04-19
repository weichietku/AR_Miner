#!/usr/bin/python
#
# Implementation of the AR Miner:
# "AR-Miner: Mining Informative Reviews for Developer from Mobile App MarketPlace"
#
# Authors:
# 1) Shanshan Li
# 2) Yingyezhe Jin
# 3) Tianshu Chu
# 4) Xiao Huang

# python imports
import os, numpy

# AR Miner imports
from AR_util import AR_parse, AR_loadReviews, AR_writeReviews
from AR_reviewInstance import Review
from AR_classifier import AR_emnb, AR_svm
from AR_lda import AR_lda

# The main method:
def main():
	# 0. Given the application, read the reviews and stem them
	datasetName = "templerun2"
	rmStopWords = False # Removing stop words lead to information loss and bad f-score
	rmRareWords = True

	# trainSet/testSet/unlabel: lists of review data
	# vocabulary: dictionary len = V and the positional index of each term in the doc vector
	# set skParse True to directly read of the data that has been filtered out
	skParse = False
	if(skParse == False):
		# the vocabulary is the words on the entire data set!
		trainSet, testSet, unlabelSet, vocabulary = AR_parse(datasetName, rmStopWords, rmRareWords)


	# 1. Use the EM-NB or SVM to filter out the informative reviews
	# informMat: the informative reviews in X x V sparse matrix from, X: documents size, V: vocabulary size
	# informRev: corresponding reviews wrapped as a list of review instances
	useSVM = True # SVM is way better than emnb in terms of the testing. 
				   # But it may not filter out the information effectively
	if(skParse == False):
		if(useSVM == False):
			informRev, informMat = AR_emnb(trainSet, testSet, unlabelSet, vocabulary, datasetName)
		else:
			informRev, informMat = AR_svm(trainSet, testSet, unlabelSet, vocabulary, datasetName)

		# write the result back to the file (optional)
		#AR_writeReviews(informRev, datasetName)
	else:
		# directly read from the file
		informRev, informMat, vocabulary = AR_loadReviews(datasetName)

	print("Number of informative reviews: " + str(len(informRev)))

	# 2. Use the LDA to do the grouping based on the topic
	# doc_topi : a k*n_topics np matrix, which indicates the probability of each review belongs to one of the topic
	# vocab_list: a list of vocabulary words
	n_topics = 20
	doc_topic, vocab_list = AR_lda(informRev, informMat, vocabulary, n_topics)

# call the main
if __name__ == "__main__":
	main()