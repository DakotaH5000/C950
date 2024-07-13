class HashTable:
  #Part A requirements
   
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
   
   
    def insert(self, key, item): #  does both insert and update 
        # get the bucket list where this item will go.
        bucket = int(key) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append(item)
    
    def search(self, key):
        bucket = int(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Search for the key in the bucket list
        for item in bucket_list:
            if int(item.id) == int(key):
                return item
        # The key is not found
        return None

    def remove(self, key):
        bucket = int(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)
    
    def __iter__(self):
    # Iterate over all items in the hash table
        for bucket in self.table:
            for kv in bucket:
                yield kv