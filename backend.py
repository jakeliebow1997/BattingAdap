import numpy as np
#data.groupby(['home_team','events']).agg('count')
#from pybaseball import statcast
import pandas as pd
import pymongo
import boto3
import pymongo
#app = Flask(__name__)

import json
client = pymongo.MongoClient("mongodb+srv://sah:dude@cluster0-ufrcd.mongodb.net/test?retryWrites=true")
mydb = client["final"]
mycol = mydb["BA"]
df=pd.read_csv('data.csv')

def getPlayer(name):
	mydoc = mycol.find({ "batter": name })
	for x in mydoc:
		return x

def main(batter):
	df=pd.read_csv('data.csv')
	df=df.loc[df['batter']==batter]#Mookie Betts
	P=0
	d={}
	for i,x in df.iterrows():
		if type(x['pitch_type'])==type('s'):
			if x['pitch_type'] not in [*d]:
				d[x['pitch_type']]=[0,0]
			if x['description']=='foul' or x['description']=='foul_tip':
				d[x['pitch_type']][0]+=0.5#foul worth half points as hit
				d[x['pitch_type']][1]+=1.0
			if x['description']=='swinging_strike' or x['description']=='swinging_strike_blocked':
				d[x['pitch_type']][1]+=1.0
			if x['description']=='hit_into_play' or x['description']=='hit_into_play_no_out' or x['description']=='hit_into_play_score':
				d[x['pitch_type']][0]+=1.0
				d[x['pitch_type']][1]+=1.0
	arr=[]
	for x in [*d]:
		arr.append(d[x][0]/d[x][1])

	s=0
	for x in arr:
		s+=(x-np.mean(arr))**2
	d['Batting Adaptability']=s/(len(arr)-1)
	mydict = { "batter": batter, "data": d }
	prop=getPlayer(batter)
	flag=False
	try:
		print(len(prop))
	except:
		y = mycol.insert_one(mydict)

	return d
#main(605141.0)#MB
for x in df.groupby(['batter']).agg('count').index:
	if x==605141.0:
		print(main(x))
