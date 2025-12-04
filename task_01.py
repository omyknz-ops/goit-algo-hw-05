'''A simple implementation of a hash table in Python with basic operations: insert, get, and delete.'''
class HashTable:
    def __init__(self, size): # Initialize the hash table with a given size
        self.size = size
        self.table = [[] for _ in range(self.size)]

    # Hash function to compute the index for a given key
    def hash_function(self, key):
        return hash(key) % self.size
    
    # Insert a key-value pair into the hash table
    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]
        
        for pair in self.table[key_hash]:
            if pair[0] == key:
                pair[1] = value
                return True
        
        self.table[key_hash].append(key_value)
        return True
    
    # Retrieve a value by its key from the hash table
    def get(self, key):
        key_hash = self.hash_function(key)
        
        for pair in self.table[key_hash]:
            if pair[0] == key:
                return pair[1]
        
        return None
    
    # Delete a key-value pair from the hash table by its key
    def delete(self, key):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]
        
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(i)
                return True
        
        return False