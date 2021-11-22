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
        self.client = pymongo.MongoClient(f'{decrypt_connection_string()}', tlsCAFile=certifi.where())
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