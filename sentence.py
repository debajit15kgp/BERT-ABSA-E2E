#import all the libraries and if nltk not present download it
import pandas as pd
import numpy as np
import csv
from nltk.tokenize import sent_tokenize

# change here just to make for the entire file
main="greatwall"

# open the file - give your own path
csv_file = open("/home/debajit15/extra/"+main+"/"+main+".csv")

# using the separator ',' as delimitor
df = pd.read_csv(csv_file,sep=',');

# this is done to drop all the rows with blank values or unannotated data
df = df[pd.notnull(df['Aspects'])]

# A helper function to print individual features
def debug(opi_ind,asp_ind,senti_ind):
	print(opi_ind)
	print(asp_ind)
	print(senti_ind)
	print("-----------------------")

# A helper function to concatenate two elements
def func(full_ind):
	ret = ""
	for ind in full_ind:

		# if we want to remove double quotes uncomment the next line
		# asp = asp.strip('"')
		ret += ind + " "

	ret += '\n'
	return ret


# defining a function to separate the annotated sentences
def get(df,folder):

	# defining different dataframes for each column
	reviews = df[['review_body']]
	aspects = df[['Aspects']]
	sentiments = df[['Sentiments']]
	opinions = df[['Opinion_Words']]

	# initialising an empty string
	review = aspect = sentiment = opinion = ""

	# iterating over the rows of the dataframe
	for row in range(df.shape[0]):

		# taking one paragraph at a time in one row at a time
		rev = reviews.iloc[row:row+1]
		rev_string = rev.to_string(index=False,header=None)
		rev_string = rev_string[1:]

		# using sent_tokenize from nltk to separate sentences from a paragraph
		sentence_list = sent_tokenize(rev_string)

		# taking aspects one at a time
		asp = aspects.iloc[row:row+1]
		asp_string = asp.to_string(index=False,header=None)
		asp_string = asp_string.split(";")

		# taking sentiments one at a time
		senti = sentiments.iloc[row:row+1]
		senti_string = senti.to_string(index=False,header=None)
		senti_string = senti_string.split(";")

		# taking opinions one at a time
		opi = opinions.iloc[row:row+1]
		opi_string = opi.to_string(index=False,header=None)
		opi_string = opi_string.split(";")

		# checking whether they have all the same length or not
		if( len(opi_string) == len(asp_string) and len(asp_string) == len(senti_string) and len(senti_string) == len(sentence_list) ):
			pass
		else:
			continue

		# keeping a counter for the current sentence in the for loop below
		it=0

		# iterating through the sentences
		for sentence in sentence_list:

			# separating the different features (sentiments,opinions,aspects) based on ',' and removing extra white spaces
			senti_ind = [x.strip() for x in senti_string[it].split(",")]
			asp_ind = [x.strip() for x in asp_string[it].split(",")]
			opi_ind = [x.strip() for x in opi_string[it].split(",")]

			# printing to check individual elements
			# debug(opi_ind,asp_ind,senti_ind)
			
			# filling each individual elements
			review += sentence + '\n'
			
			aspect += func(asp_ind)

			sentiment += func(senti_ind)

			opinion += func(opi_ind)
			

			it+=1
		
	# label=label.rstrip('\n')
	# term=term.rstrip('\n')
	# review=review.rstrip('\n')
	# position=position.rstrip('\n')

	# Put your own path in the place of "/home/debajit15/"
	path = "/home/debajit15/"+str(folder)


	text_file = open(path+"/review.txt", "w")
	n = text_file.write(review)
	text_file.close() 

	text_file = open(path+"/opinion.txt", "w")
	n = text_file.write(opinion)
	text_file.close()
	
	text_file = open(path+"/sentiment.txt", "w")
	n = text_file.write(sentiment)
	text_file.close()
	
	text_file = open(path+"/aspect.txt", "w")
	n = text_file.write(aspect)
	text_file.close()

fin_path = "Sentence_Annotations/" + main
print(fin_path)
get(df,fin_path)



