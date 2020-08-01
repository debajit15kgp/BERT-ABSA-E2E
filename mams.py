import pandas as pd
import numpy as np
import csv
from nltk.tokenize import sent_tokenize
csv_file=open("/home/debajit15/extra/final/train+dev.csv")

df=pd.read_csv(csv_file,sep=',');
df = df[pd.notnull(df['Aspects'])]
print(df.shape)

def train_validate_test_split(df, train_percent=.8, validate_percent=.2, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    train = df.iloc[:train_end]
    validate = df.iloc[train_end:]
    return train, validate

trainl,vall=train_validate_test_split(df)

lis=[1,0,-1]

def get(df,wq,lk):
	final="<?xml version=\"1.0\" encoding=\"utf-8\"?>"+"\n"
	final+="<sentences>\n"
	col=df[['review_body']]
	#print(col.head())
	aspect=df[['Aspects']]
	#print(aspect.head())
	opinions=df[['Sentiments']]
	#print(opinions.head())
	#print(df.shape)
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
		#print(senti)
		#print(l)
		it=0
		for t in l:
			f=0
			chks=[x.strip() for x in senti[it].split(",")]
			chka=[x.strip() for x in asp[it].split(",")]
			for i in chka:
				if(i=='$'):
					f=1;
					break
			if(f==1):
				continue
			cnt=0
			itr=0
			g=0
			if(len(chks)!=len(chka) or len(chka)<2):
				continue
			for i in chka:
				#chks[itr]=int(chks[itr])
				if(chks[itr]=='1' or chks[itr]=='-1' or chks[itr]=='0'):
					#print('a')
					continue
				elif(i=='$'):
					g=1;
					cnt+=1
				else:
					cnt+=1
					#print('a')
				itr+=1
			itr=0
			if(cnt==len(chks) or g==1):
				continue
			
			final+="\t"+"<sentence>"+"\n"
			final+="\t"+"\t"+"<text>"+t+"</text>"+"\n"
			#print(chks)
			#print(chka)
			
			itr=0

			final+="\t"+"\t"+"<aspectCategories>"+"\n"

			for i in chks:
				if(chka[itr]=='$'):
					continue
				chka[itr]=chka[itr].strip('"')
				final+="\t"+"\t"+"\t"+"<aspectCategory category=\""+chka[itr]+"\" polarity="
				if(i=='1'):	
					final+="\"positive\"/>"
				elif(i=='-1'):
					final+="\"negative\"/>"
				elif(i=='0'):
					final+="\"neutral\"/>"
				else:
					final+="\"neutral\"/>"
				final+='\n'
				itr+=1
			final+="\t"+"\t"+"</aspectCategories>"+"\n"
			#print(final)
			final+="\t"+"</sentence>"+"\n"
			it+=1
	final+="</sentences>"
	print(final)
	text_file = open("/home/debajit15/"+str(wq)+"/"+str(lk)+".xml", "w")
	n = text_file.write(final)
	text_file.close()
	# 	it=0
	# 	for i in l:
	# 		chks=[x.strip() for x in senti[it].split(",")]
	# 		chka=[x.strip() for x in asp[it].split(",")]
	# 		# for i in chks:
	# 		# 	print(i)
	# 		# 	if(i=='-1'):
	# 		# 		label+="negative\n"
	# 		# 	if(i=='0'):
	# 		# 		label+="neutral\n"
	# 		# 	if(i=='1'):
	# 		# 		label+="positive\n"
	# 		#print(chks)
	# 		itr=0
	# 		for k in chka:
	# 			if(k=='$'):
	# 				continue
	# 			review+=i+'\n'
	# 			k=k.strip('"')
	# 			term+=k+'\n'
	# 			for h in range(0,len(i)-len(k)):
	# 				f=i[h:h+len(k)]
	# 				if(f==k):
	# 					se=h
	# 					en=h+len(k)
	# 					break
	# 			position+=str(se)+","+str(en)+"\n"
	# 			#print(k,i)
	# 			#label+=chks[itr]+'\n'
	# 			if(chks[itr]=='-1'):
	# 				label+="negative\n"
	# 			if(chks[itr]=='0'):
	# 				label+="neutral\n"
	# 			if(chks[itr]=='1'):
	# 				label+="positive\n"
	# 			#print(k)
	# 			#print(chks[itr])
	# 			num=chks[itr]
				
	# 		#print(term)
	# 		#label=label.rstrip('\n')
	# 		#print(label)
	# 		#print(i)
	# 		#print(chka)
	# 		it+=1
		
	# 	print(review)
	# 	print(term)
	# 	print(label)
	# 	print(position)
	# label=label.rstrip('\n')
	# term=term.rstrip('\n')
	# review=review.rstrip('\n')
	# position=position.rstrip('\n')
	# text_file = open("/home/debajit15/"+str(wq)+"/"+str(lk)+"/label.txt", "w")
	# n = text_file.write(label)
	# text_file.close()
	# text_file = open("/home/debajit15/"+str(wq)+"/"+str(lk)+"/review.txt", "w")
	# n = text_file.write(review)
	# text_file.close()
	# text_file = open("/home/debajit15/"+str(wq)+"/"+str(lk)+"/term.txt", "w")
	# n = text_file.write(term)
	# text_file.close()
	# text_file = open("/home/debajit15/"+str(wq)+"/"+str(lk)+"/position.txt", "w")
	# n = text_file.write(position)
	# text_file.close()

	# print(position)


# def get(df):
	
s="final"
train=get(trainl,s,"train")
#test=get(df,s,"test")
val=get(vall,s,"val")

# text_file = open("/home/debajit15/custom/petra/train.txt", "w")
# n = text_file.write(train)
# text_file.close()
# text_file = open("/home/debajit15/custom/petra/test.txt", "w")
# n = text_file.write(test)
# text_file.close()
# text_file = open("/home/debajit15/custom/petra/dev.txt", "w")
# n = text_file.write(val)
# text_file.close()


