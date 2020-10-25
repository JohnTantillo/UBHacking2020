import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://hack:Passw0rd@cluster0.gu6ke.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('WorkersDay_db')
prod = db.Productivity


# adds worker random worker if database is empty
if prod.count_documents({}) == 0:
    prod.insert_one({'name': "PlaceHolder", 'data': [1,1,1,1,1,1,1,1]})


# adds counter variable
if prod.find_one({'name': 'counter'}) == None:
    prod.insert_one({'name': 'counter', 'c': 0})


# updates counter
def update_counter (newc):
    prod.update_one({'name': 'counter'}, {'$set': {'c': newc}})


# returns current counter
def get_counter():
    ret = prod.find_one({'name': 'counter'})
    return {'name': ret['name'], 'c': ret['c']}


# adds specified worker to database using {name: '', data: []} json string as input
def add_worker (w):
    prod.insert_one(w)


# updates specified worker data array in database using {name: '', data: []} json string as input
def update_worker (w):
    arr = {'data': w['data']}
    prod.update_one({'name': w['name']}, {'$set': arr})


# returns specified worker data json string in this format {'name': '', 'data': []}
def get_worker (w):
    ret = prod.find_one({'name': w['name']})
    return {'name': ret['name'], 'data': ret['data']}


# deletes a worker from the database
def delete_worker(w):
    prod.delete_one({'name': w['name']})


# {name: '', data: []}
