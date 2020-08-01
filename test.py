import pandas as pd
import numpy as np
import csv
#import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize
csv_file=open("/home/debajit15/train+dev.csv")
pd.set_option('display.max_colwidth', None)
df=pd.read_csv(csv_file,sep=',');
df = df[pd.notnull(df['Aspects'])]
#print(df['Opinion_Words'].iloc[0:1])

def train_validate_test_split(df, train_percent=.8, validate_percent=.2, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    train = df.iloc[:train_end]
    validate = df.iloc[train_end:]
    return train, validate

trainl,vall=train_validate_test_split(df)

def get(df):
	col=df[['review_body']]
	print(col.head())
	aspect=df[['Aspects']]
	opinions=df[['Sentiments']]
	print(df.shape[0])
	now=""
	for o in range(0,df.shape[0]):
		d=col.iloc[o:o+1]
		sd=d.to_string(index=False,header=None)
		sd=sd[1:]
		l=sent_tokenize(sd)

		a=aspect.iloc[o:o+1]
		sa=a.to_string(index=False,header=None)
		asp=sa.split(";")

		a=opinions.iloc[o:o+1]
		sa=a.to_string(index=False,header=None)
		senti=sa.split(";")

		if(len(asp)!=len(senti) or len(l)!=len(asp) or len(l)!=len(senti)):
			continue
		it=0
		for i in l:
			chks=[x.strip() for x in senti[it].split(",")]
			chka=[x.strip() for x in asp[it].split(",")]

			g=[]
			itr=0
			if(len(chks)!=len(chka)):
				continue
			for k in chka:
				f=k.split(" ")
				num=chks[itr]
				if(len(f)>1):
					h=0
					for x in f:
						x=x.strip(' ')
						x=x.strip('"')
						g+=[x]
						if(h<len(f)-1):
							chks.insert(itr,'1')
						h+=1
				else:
					g+=f
				itr+=1
			chka=g
			now+=i
			now+="####"
			j=i.split(" ")
			itr=0
			for word in j:
				if itr<len(chka) and word==chka[itr] :
					if chks[itr]=='1':
						s=word+"=T-POS"
					elif chks[itr]=='0':
						s=word+"=T-NEU"
					else:
						s=word+"=T-NEG"
					itr+=1
				else:
					s=word+"=O"
				now+=s+" "
			now+="\n"
			it+=1
	return now


train=get(trainl)
val=get(vall)

text_file = open("/home/debajit15/train.txt", "w")
n = text_file.write(train)
text_file.close()
text_file = open("/home/debajit15/dev.txt", "w")
n = text_file.write(val)
text_file.close()


# #print(df[['review_body']])
