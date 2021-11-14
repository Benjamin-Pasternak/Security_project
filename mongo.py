import pymongo 
import datetime
import time
import os
import sys 
# import rsa2



class mongodb_atlas_test:
    def __init__(self):
        """
        TODO: This client connection string needs to probabaly be secured. Need to figure out what 
        the best way to do this is.
        """
        self.client = pymongo.MongoClient('')
        self.db = self.client.myFirstDatabase
        self.collection = self.db.user_info
        

    def insert_data(self,data):
        """
        This function is used to insert data into the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        self.collection.insert_one(data)

    def get_data(self,username):
        """
        This function is used to get data from the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        return list(self.collection.find({ "$text": { "$search": f"{username}" } } ) )

    def delete_data(self,data):
        """
        This function is used to delete data from the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        self.collection.delete_one(data)
    
    def upsert_data(self,data):
        """
        This function is used to upsert data into the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        self.collection.update_one(data,{'$set':data},upsert=True)
    

if __name__ == "__main__":
    mongodb_atlas_test = mongodb_atlas_test()
    # publicKey1, e = rsa2.gen_public_key()
    # privateKey1 = rsa2.gen_private_key(publicKey1[0], e)
    # publicKey2, e = rsa2.gen_public_key()
    # privateKey2 = rsa2.gen_private_key(publicKey2[0], e)
    # data1 = {
    #     "username": "John",
    #     "password": "yomama",
    #     "publicKey": publicKey1
    # }
    data2 = {
        "username": "Bob",
        "password": "yo_mama",
        "publicKey": (13, 5)
    }
    
    
    # data2 = {mongodb_atlas_test.collection.find( { "$text": { "$search": "Bob" } } )



    
    the = mongodb_atlas_test.get_data('Bob')
    # the = mongodb_atlas_test.collection.find({ "$text": { "$search": "Bob" } } )

    # the = mongodb_atlas_test.get_data({"$text": { "$search": "Bob" } })

    print(the)
    
    
    
    