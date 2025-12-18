# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'AHMongo05!' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient(f'mongodb://%s:%s@%s:%d/?authSource=admin' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def get_next_record_number(self):
        last_record = self.database.animals.find_one(sort=[("record_number", -1)])
        if last_record: 
            return last_record.get("record_number", 0) + 1
        else:
            return 1
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            # self.database.animals.insert_one(data)  # data should be dictionary  
            
            data["record_number"] = self.get_next_record_number()
            
            result = self.database.animals.insert_one(data)
            return result.inserted_id
            
        else: 
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            result = self.database.animals.find(query)
            return list(result)
        else:
            raise Exception("Cannot perform read(), query is empty")
            
    # Update method to implement the U in CRUD.
    def update(self, query, update_value):
        if query is None or update_value is None:
            raise Exception("Query and update_values parameters empty")
            
        result = self.database.animals.update_many(query, {"$set": update_value})
        
        return { "matched_count": result.matched_count, "modified_count": result.modified_count }
    
    # Delete method to implement the D in CRUD.
    def delete(self, query):
        if query is None:
            raise Exception("No query parameter found.")
        
        result = self.database.animals.delete_many(query)
        
        return { "deleted_count": result.deleted_count }
        
    
    
    
        
