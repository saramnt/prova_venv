from innolva_spider.dao.MongoDAO import MongoDAO


class LinksForMongo(MongoDAO):

    def __init__(self, host, port, db):
        super().__init__(host, port, db)


#nel costruttore andremo ad inserire le varie informazioni riguardanti il DB
    def object_to_dict(self, obj, collection):
        mydb = self.client[self.db][collection]
        dict = {



                "URL": obj.url,
                "Data": obj.date,
                "Autore": obj.author,
                "Titolo": obj.title,
                "Body": obj.body

                                }
        mydb.insert_one(dict)






if __name__ == '__main__':
    database = LinksForMongo("localhost", 27017, "articles_mongodb")








