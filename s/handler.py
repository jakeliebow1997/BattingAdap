import pymongo
import json

def main(event,context):
    batter=float(event['body'])
    client = pymongo.MongoClient("mongodb+srv://sah:dude@cluster0-ufrcd.mongodb.net/test?retryWrites=true")
    mydb = client["final"]
    mycol = mydb["BA"]
    data=mycol.find({'batter':batter})
    #print(data)
    d={}
    for x in data:
        d=x['data'].copy()
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'},
            'body': json.dumps(d,ensure_ascii=False)
        }