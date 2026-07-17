class Hash_Table:
    def __init__(self):
        self.size = 8
        self.load_factor = 0.7
        self.buckets = self._create_buckets(self.size)
        self.length = 0

    def _create_buckets(self, count):
        return [[] for _ in range(count)]
    
    def _hash(self, key):
        return abs(hash(key))
    
    def _get_bucket_index(self, key):
        return self._hash(key) % self.size
    
    def get(self, key):
        bucket = self.buckets[self._get_bucket_index(key)]
        for item in bucket:
            if item[0] == key: return item[1]
    
    def insert(self, key, value):
        # Checks if assigned bucket already contains the current package and returns if so, appends otherwise. checks if table is over the load_factor threshold and calls resize if true.
        bucket = self.buckets[self._get_bucket_index(key)]
        for item in bucket:
            if item[0] == key: return

        bucket.append((key, value))
        self.length += 1

        if self.length / self.size > self.load_factor: self._resize()

    def _resize(self):
        # create new buckets and save to local variable. loop through current buckets and re insert each item into new table. after point self.buckets to new table and double size property
        self.size *= 2
        new_buckets = self._create_buckets(self.size)
        for bucket in self.buckets:
            for item in bucket:
                key = item[0]
                value = item[1]
            # insert into new_buckets table.
                new_bucket = new_buckets[self._get_bucket_index(key)]
                new_bucket.append((key, value))
        self.buckets = new_buckets


    def remove(self, key):
        pass
        # decrement length
