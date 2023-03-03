import pymongo
import requests
from bs4 import BeautifulSoup
import os
import json


pendingQuestions = []
with open('./credentials.txt', 'r') as f:
    for line in f:
        srv  = line.strip()


def getMongoClient():
    client = pymongo.MongoClient(srv)
    # mongodb should handle the errors and exceptions
    return client


def parseQuestion(question):
    soup = BeautifulSoup(question, 'html.parser')
    getText = soup.get_text().strip()
    img_tag = soup.find('img')
    if img_tag:
        img_src = img_tag.get('src')
        return img_src,getText
    else:
        return None,getText


def queryDatabase(Information):
    getDadabase = getMongoClient().list_database_names()
    for info in getDadabase:
        if info == "waterCertification":
            get_collection = getMongoClient()[info].list_collection_names()
            for collection in get_collection:
                if collection == Information:
                    _get_collection = getMongoClient()[info][collection]
                    get_data = _get_collection.find()
                    return get_data




def getAnswer(answer_id):
    for answer in queryDatabase("ZANSWER"):
        if 'ZIDENTIFIER' in answer:
            if answer['ZIDENTIFIER'] == answer_id:
                answer['ZRAWCONTENT'] = answer['ZRAWCONTENT'].replace('\xa0', ' ')
                answer['ZTEXT'] = answer['ZTEXT'].replace('\xa0', ' ')
                return answer['ZRAWCONTENT'],answer['ZTEXT']


def queryServer(ZIDENTIFIER, ZQUESTION,ZRATIONAL):
    # TODO: This is an important part we need a try catch block to handle the errors quit the program if this fails for any reason
    try:

        cookies = {
        }

        headers = {
            'Accept': 'application/json',
            'APP_VERSION': '8.99.10566',
            'X-HLTBundleIdentifier': 'com.hltcorp.awwa',
            'HLTPaging': 'true',
            'platform': 'ios',
            'User-Agent': 'App/8.99.10566 (com.hltcorp.awwa; build:10566; iOS 14.0.0) Alamofire/8.99.10566',
            'HLTUserTimeZone': 'America/Chicago',
            'Accept-Language': 'en-US;q=1.0',
            'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
        }

        response = requests.get(f'https://hlt-web-service.herokuapp.com/api/v3/flashcard_meta_data/{ZIDENTIFIER}', headers=headers, cookies=cookies)
        records = response.json()
        for record in records['records']:
            if 'answer_id' in record:
                #TODO: find a way to use content
                content,text = getAnswer(record['answer_id'])
                record['answer'] = text
        image_src,question = parseQuestion(ZQUESTION)
        question = question.replace('\xa0', ' ')
        if image_src:
            records['diagram'] = image_src
        records['question'] = question
        if ZRATIONAL != None:
            image_src_rationale,rationale = parseQuestion(ZRATIONAL)
            rationale = rationale.replace('\xa0', ' ')
            if image_src_rationale:
                records['diagram_rationale'] = image_src_rationale
            records['rationale'] = rationale

        else:
            records['rationale'] = "No Rationale Provided"

        # records['question'] = parseQuestion(ZQUESTION)
        # records['rationale'] = parseQuestion(ZRATIONAL)
        max_percentage = max(records['records'], key=lambda x: x['percentage'])
        # answer_id = max_percentage['answer_id']
        # percentage = max_percentage['percentage']
        # print(f"The answer with answer id {answer_id} has the highest percentage of {percentage}%")
        # print(f"The answer is: {max_percentage['answer']}")
        records['correct_answer'] = max_percentage['answer']
        # with open('querylog.json','w') as f:
        #     json.dump(records,f)

        return records
    except Exception as e:
        # save error to file
        with open('querylog.txt','a') as f:
            f.write(f"Error: from queryServer(): {str(e)} ")
            f.write("\n")
        import subprocess
        print("check log querylog.txt for more information")
        subprocess.call("bash ./helper.sh q ", shell=True)
        os._exit(0)

# finally cache the data back to the database
def createbd(database,collection):
    getDadabase = getMongoClient().list_database_names()
    if database in getDadabase:
        return
    if database not in getDadabase:
        getMongoClient()[database][collection].insert_one({"test": "test"})
        getMongoClient()[database][collection].delete_one({"test": "test"})
    get_collection = getMongoClient()[database].list_collection_names()
    if collection not in get_collection:
        getMongoClient()[database][collection].insert_one({"test": "test"})
        getMongoClient()[database][collection].delete_one({"test": "test"})



def cacheJson(records=None,search=None):
    database = "ExamCache"
    collection = "generatedExam"
    createbd(database,collection)
    if search:
        image_src,question = parseQuestion(search)
        question = question.replace('\xa0', ' ')
        _get_collection_ = getMongoClient()[database].list_collection_names()
        for collection in _get_collection_:
            if collection == "generatedExam":
                _get_collection = getMongoClient()[database][collection]
                get_data = _get_collection.find()
                for data in get_data:
                    if 'question' in data:
                        if data['question'] == question:
                            return data
    if records != None:
        getMongoClient()[database][collection].insert_one(records)





def getQuestions():
    #  - TODO: save to file and read from file
    get_data = queryDatabase("ZFLASHCARD")
    return get_data


def generateQuestions(data,ZQUESTION,stdscr):
    generated = cacheJson(search=ZQUESTION)
    if generated:
        return generated
    # print("- please wait while the information generated shows -\n\n")
    if data['ZRATIONALE'] != None and data['ZRATIONALE'] != "":
        rationale = data['ZRATIONALE']
    else:
        rationale = None
    query = queryServer(ZIDENTIFIER = data['ZIDENTIFIER'] , ZQUESTION = data['ZQUESTION'], ZRATIONAL = rationale)
    if query:
        cacheJson(records=query)
        return query


