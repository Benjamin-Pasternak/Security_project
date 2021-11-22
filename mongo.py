import pymongo
import datetime
import time
import os
import sys
import certifi
import json
import rsa3

def decrypt_connection_string():
    file = open('./secrets.json')
    data = json.load(file)
    connect_string = rsa3.rsa_decrypt_message(data['string'], data['d'], data['n'])
    connect_string = int(''.join([str(x) for x in connect_string]))
    connect_string = connect_string.to_bytes((connect_string.bit_length() + 7) // 8, 'big').decode('utf-8')
    return connect_string



class mongodb_atlas_test:
    def __init__(self):
        # connection_uri =
        self.client = pymongo.MongoClient('mongodb+srv://general_user:Snapdragon777apZ@cluster0.shbn7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        self.db = self.client.myFirstDatabase
        self.collection = self.db.user_info

    def insert_data(self, data):
        """
        This function is used to insert data into the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        self.collection.insert_one(data)

    def get_data(self, username):
        """
        This function is used to get data from the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        return list(self.collection.find({"$text": {"$search": f"{username}"}}))

    def delete_data(self, data):
        """
        This function is used to delete data from the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        self.collection.delete_one(data)

    def upsert_data(self, data):
        """
        This function is used to upsert data into the database collection.
        @param data: This is the data that is to be inserted into the database. Dictionary format.
        """
        self.collection.update_one(data, {'$set': data}, upsert=True)


# if __name__ == "__main__":
#     mongodb_atlas_test = mongodb_atlas_test()
#     # publicKey1, e = rsa2.gen_public_key()
#     # privateKey1 = rsa2.gen_private_key(publicKey1[0], e)
#     # publicKey2, e = rsa2.gen_public_key()
#     # privateKey2 = rsa2.gen_private_key(publicKey2[0], e)
#     # data1 = {
#     #     "username": "John",
#     #     "password": "yomama",
#     #     "publicKey": publicKey1
#     # }
#     data2 = {
#         "username": "Bob",
#         "password": "yo_mama",
#         "publicKey": (13, 5)
#     }
#
#     # data2 = {mongodb_atlas_test.collection.find( { "$text": { "$search": "Bob" } } )
#
#     the = mongodb_atlas_test.get_data('Bob')
#     # the = mongodb_atlas_test.collection.find({ "$text": { "$search": "Bob" } } )
#
#     # the = mongodb_atlas_test.get_data({"$text": { "$search": "Bob" } })
#     yoo = 'yo_mama'
#     print(the)
#     if not the:
#         print('hmm')
#     temp = str(the[0])
#     print(temp.find('password'))
#     print(temp[66])
#     num = temp.find('password')
#     num = num+12
#     temp = temp[num:]
#     print(temp.find("'"))
#     num2 = temp.find("'")
#     temp = temp[:num2]
#     print(temp)
#     if(temp == yoo):
#         print('yay')
#     #the2 = dict[(the)]
#
#    # usetemp = the2.get("username")
#    # print(usetemp)

# if __name__ == "__main__":
#     decrypt_connection_string()