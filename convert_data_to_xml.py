#import all the libraries and if nltk not present download it
import pandas as pd
import numpy as np
import csv
from nltk.tokenize import sent_tokenize
from sklearn.model_selection import train_test_split

# change here just to make for the entire file
main="greatwall"

# open the file - give your own path
csv_file = open("/home/debajit15/extra/"+main+"/"+main+".csv")

# using the separator ',' as delimitor
df = pd.read_csv(csv_file,sep=',');

# this is done to drop all the rows with blank values or unannotated data
df = df[pd.notnull(df['Aspects'])]

# splitting test train data with random state 40 (seed)
df1, df2 = train_test_split(df, test_size=0.2, random_state=40)

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

def get(df,wq,lk):
	# defining different dataframes for each column
	reviews = df[['review_body']]
	aspects = df[['Aspects']]
	sentiments = df[['Sentiments']]
	opinions = df[['Opinion_Words']]

	final="<?xml version=\"1.0\" encoding=\"utf-8\"?>"+"\n"
	final+="<sentences>\n"

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

		# checking whether they have same length or not
		if( len(opi_string) == len(asp_string) and len(asp_string) == len(senti_string) and len(senti_string) == len(sentence_list) ):
			pass
		else:
			continue

		it=0
		text = ""

		for sentence in sentence_list:

			# separating the different features (sentiments,opinions,aspects) based on ',' and removing extra white spaces
			senti_ind = [x.strip() for x in senti_string[it].split(",")]
			asp_ind = [x.strip() for x in asp_string[it].split(",")]
			opi_ind = [x.strip() for x in opi_string[it].split(",")]

			# printing to check individual elements
			# print (sentence)
			# debug (opi_ind,asp_ind,senti_ind)

			# find position of aspect term in sentence and maintain simultaneous counter for other features
			itr=0
			sen_len=len(sentence)

			# if length does not match then correct the annotations
			if(len(asp_ind)==len(senti_ind) and len(senti_ind)==len(opi_ind)):
				pass
			else:

				continue
			
			newasp = []
			newopi = []
			newsenti = []

			for asp in asp_ind:
				
				sent = senti_ind[itr]
				op = opi_ind[itr]
				op = op.strip('"')
				asp = asp.strip('"')
				# a bool variable to check if the number of aspects,opinions and sentiments match or not
				found = 0

				# check in the whole sentence
				for i in range(sen_len):

					# if the first letters match check for the whole sentence
					if(sentence[i]==asp[0]):
						j=i
						k=0
						while(k<len(asp) and j<sen_len and sentence[j]==asp[k]):
							j+=1
							k+=1
						if(k==len(asp)):
							l=[asp,[i,i+k-1]]
							found=1

				for i in range(sen_len):

					# if the first letters match check for the whole sentence
					if(sentence[i]==op[0]):
						j=i
						k=0
						while(k<len(op) and j<sen_len and sentence[j]==op[k]):
							j+=1
							k+=1
						if(k==len(op) and found==1):
							g=[op,[i,i+k-1]]
							found=2
				
				# for a neutral aspect with no opinions 
				if(found==1 and sent=="0"):
					newasp.append(l)
					newopi.append(['$',[0,0]])
					newsenti.append('neutral')

				# for all aspects complete with opinions and sentiments
				if(found==2 and sent!="$"):
					newasp.append(l)
					newopi.append(g)
					if(sent=="1"):
						newsenti.append("positive")
					elif(sent=="0"):
						newsenti.append("neutral")
					else:
						newsenti.append("negative")

				itr+=1


			# starting each individual sentence
			text+="\t<sentence>\n"

			# concatenating the review first
			text+="\t \t<text>"+sentence+"</text>\n"

			
			# now attaching the aspect terms
			text+="\t \t<aspectTerms>\n"
			
			itr=0;
			# iterating over all the possible aspects in the sentence
			for asp in newasp:

				# now attaching individual aspects
				text=text+"\t \t \t<aspect term=\""+str(asp[0])+"\" from=\""+str(asp[1][0])+"\" to=\""+str(asp[1][1])+"\" polarity=\""+newsenti[itr]+"\">\n"
				
				# now its the turn of opinions
				text+="\t \t \t \t<opinions>\n"

				nowopi = [x.strip() for x in newopi[itr][0].split(":")]
				for opi in nowopi:
					found=[0,0]
					for i in range(sen_len):
						if(sentence[i]==opi[0]):
							j=i;
							k=0;
							while(j<sen_len and k<len(opi) and sentence[j]==opi[k]):
								j+=1
								k+=1
							if(k==len(opi)):
								found=[i,i+k-1]
								break

					if(found==[0,0]):
						continue

					text+="\t \t \t \t \t<opinionTerm term=\""+opi+"\" from=\""+str(found[0])+"\" to=\""+str(found[1])+"\"/>\n"

				text+="\t \t \t \t</opinions>\n"
				text+="\t \t \t</aspect>\n"

				itr+=1

			text+="\t \t</aspectTerms>\n"

			# closing the sentence
			text+="\t</sentence>\n"
			it+=1

		# appending the answer for current paragraph
		final+=text

	# adding the final tag
	final+="</sentences>\n"

	# writing it to a file
	text_file = open("/home/debajit15/"+str(wq)+"/"+str(lk)+".xml", "w")
	n = text_file.write(final)
	text_file.close()
	
s=""
print(df1.head())
train = get(df1 , s, "train")
test  = get(df2 , s, "test")


