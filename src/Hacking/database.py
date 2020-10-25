import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://hack:Passw0rd@cluster0.gu6ke.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('WorkersDay_db')
prod = db.Productivity

#adds worker random worker if database is empty
if prod.count_documents({}) == 0:
    prod.insert_one({'name': "PlaceHolder", 'data': [1,1,1,1,1,1,1,1]})

#adds specified worker to database using {name: '', data: []} json string as input
def add_worker (w):
    prod.insert_one(w)

#updates specified worker data array in database using {name: '', data: []} json string as input
def update_worker (w):
    arr = {'data': w['data']}
    prod.update_one({'name': w['name']}, {'$set': arr})

#returns specified worker data json string in this format {'_id': ObjectId(), 'name': '', 'data': []}
def get_worker (w):
    return prod.find_one({'name': w['name']})

#deletes a worker from the database
def delete_worker(w):
    prod.delete_one({'name': w['name']})

#def main ():
    #delete_worker( {'name': "PlaceHolder", 'data': [1,1,1,1,1,1,1,1]})
    #w = {'name': "ale", 'data': [1,1,1,1,1,1,1,1]}
    #add_worker(w)
    #update = {'name': "ale", 'data': [0,0,0,0,0,0,0,0]}
    #update_worker(update)
    #print(get_worker(w))
    delete_worker({'name': "PlaceHolder", 'data': [1,1,1,1,1,1,1,1]})
    delete_worker({'name': "PlaceHolder", 'data': [1,1,1,1,1,1,1,1]})
    #delete_worker({'name': "PlaceHolder", 'data': [1,1,1,1,1,1,1,1]})
    #delete_worker({'name': "ale", 'data': [0,0,0,0,0,0,0,0]})


#if __name__ == "__main__":
#    main()


#{name: '', data: []}
