from bson import ObjectId
from pymongo import MongoClient, DESCENDING

class MongoDAO:

    def __init__(self, host, port, db):
        self.db = db
        self.host = host
        self.port = port
        self.client = MongoClient(host=self.host, port=self.port)

    def save(self, collection, obj):
        coll = self.getcoll(collection)
        if not type(obj) == list:
            obj = [obj]
        obj_to_insert = [o for o in obj if "_id" not in o]
        obj_to_update = [o for o in obj if "_id" in o]
        # insert on object without "_id" field
        if len(obj_to_insert) > 0:
            coll.insert(obj_to_insert, check_keys=False)
        # update on object with "_id" field
        for o in obj_to_update:
            id_ob = o["_id"]
            del o["_id"]
            try:
                doc = coll.find_one_and_update(
                    {"_id": ObjectId(id_ob)},
                    {"$set": o}, upsert=True)
                if not doc:
                    coll.insert(o, check_keys=False)
            except:
                coll.insert(o, check_keys=False)

    def update_by_id(self, collection, id, key_values_dict):
        coll = self.getcoll(collection)
        coll.find_one_and_update({"_id": ObjectId(id)}, {"$set": key_values_dict}, upsert=True)

    def update_by_conditiondict(self, collection, conditiondict, updatedict):
        coll = self.getcoll(collection)
        coll.update_one(conditiondict, {"$set": updatedict}, upsert=True)

    def delete(self, collection, id):
        coll = self.getcoll(collection)
        coll.remove({"_id": ObjectId(id)})

    def delete_by_conditiondict(self, collection, conditiondict):
        coll = self.getcoll(collection)
        coll.remove(conditiondict, True)

    def all(self, collection, start: int = 0, rows: int = None, selection=None):
        coll = self.getcoll(collection)
        if rows:
            for el in coll.find(None, selection).skip(start).limit(rows):
                el["_id"] = str(el["_id"])
                yield el
        else:
            for el in coll.find().skip(start):
                el["_id"] = str(el["_id"])
                yield el

    def getbyid(self, collection, id):
        coll = self.getcoll(collection)
        el = coll.find_one({"_id": ObjectId(id)})
        if not el:
            raise Exception("Element with id " + str(id) + " not found")
        el["_id"] = str(el["_id"])
        return el

    def get_by_conditiondict(self, collection, conditiondict):
        coll = self.getcoll(collection)
        el = coll.find_one(conditiondict)
        if not el:
            raise Exception("Element not found")
        return el

    def collections(self):
        return self.client.get_database(self.db).collection_names() #ritorna tutte le collezioni

    def drop(self, collection):
        coll = self.getcoll(collection) #elimina una collection
        coll.drop()

    def getcoll(self, collection):
        return self.client.get_database(self.db).get_collection(collection) #ritorna la collezione richiesta

    def sample(self, collection, n):
        coll = self.getcoll(collection)
        for el in coll.aggregate([{"$sample": {"size": n}}]):
            el["_id"] = str(el["_id"])
            yield el

    def query(self, collection, q):
        coll = self.getcoll(collection)
        for el in coll.find(q):
            el["_id"] = str(el["_id"])
            yield el

    def copy(self, collection1, collection2):
        coll1 = self.getcoll(collection1)
        coll2 = self.getcoll(collection2)
        coll2.remove()
        for el in coll1.find():
            coll2.insert(el)

    def count(self, collection):
        return self.getcoll(collection).count()

    def get_last(self, collection, q: {} = None):
        coll = self.getcoll(collection)
        return coll.find_one(sort=[('_id', DESCENDING)])


# if __name__ == '__main__':

    # database = MongoDAO("localhost", 27017, "URLs")
    # mydb = database.client[database.db]["Links"]
    #
    # dict = {"URL": "www.corriere.it"}
    #
    # x = mydb.insert_one(dict)
    #
    # print(x.inserted_id)
