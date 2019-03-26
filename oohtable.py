from jinja2 import Environment

class HashTable:

    @staticmethod
    def hashcode(o):
        """
        Return a hashcode for strings and integers; all others return None
        For integers, just return the integer value.
        For strings, perform operation h = h*31 + ord(c) for all characters in the string
        """
        if isinstance(o, str):  # str
            h = 0
            for c in o:
                h = (h * 31) + ord(c)
            return (h)
        elif isinstance(o, int):
            return (o)
        else:  # neither string nor int
            return None

    @staticmethod
    def bucket_indexof(targetBucket, key):
        """
        You don't have to implement this, but I found it to be a handy function.
        Return the index of the element within a specific bucket; the bucket is:
        table[hashcode(key) % len(table)]. You have to linearly
        search the bucket to find the tuple containing key.
        """
        return ([tup[0] for tup in targetBucket].index(key))

    def __init__(self, nbuckets):
        """Return a list of nbuckets lists"""
        self.table = [[] for bucket in range(nbuckets)] # nbuckets empty lists

    def __len__(self):
        """Return length of elements among all buckets"""
        counter = 0
        for bucket in self.table:
            for elem in bucket:
                counter = counter + 1
        #print(counter)
        return counter

    def __setitem__(self, key, value):
        """
        Perform the equivalent of table[key] = value
        Find the appropriate bucket indicated by key and then append (key,value)
        to that bucket if the (key,value) pair doesn't exist yet in that bucket.
        If the bucket for key already has a (key,value) pair with that key,
        then replace the tuple with the new (key,value).
        Make sure that you are only adding (key,value) associations to the buckets.
        The type(value) can be anything. Could be a set, list, number, string, anything!
        """
        bucketIndex = HashTable.hashcode(key) % len(self.table)
        targetBucket = self.table[bucketIndex]
        if any(key in tup for tup in targetBucket):  # check existence
            self.table[bucketIndex][HashTable.bucket_indexof(targetBucket, key)] = (key, value)  # for strings, just replace instead of update
        else:
            self.table[bucketIndex].append((key, value))

    def __getitem__(self, key):
        """
        Return the equivalent of table[key].
        Find the appropriate bucket indicated by the key and look for the
        association with the key. Return the value (not the key and not
        the association!). Return None if key not found.
        """
        bucketIndex = HashTable.hashcode(key) % len(self.table)
        targetBucket = self.table[bucketIndex]
        if any(key in tup for tup in targetBucket):  # check existence
            return int(targetBucket[HashTable.bucket_indexof(targetBucket, key)][1])
        else:
            return None

    def __contains__(self, key):
        for bucket in self.table:
            for tup in bucket:
                if key in tup:
                    return True

    def __iter__(self):
        for bucket in self.table:
            for pair in bucket:
                yield pair[0] # key

    def keys(self):
        final_list = []
        for bucket in self.table:
            for pair in bucket:
                final_list.append(pair[0])
        return final_list

    def items(self):
        final_list = []
        for bucket in self.table:
            for pair in bucket:
                final_list.append(pair)
        return final_list

    def __repr__(self):
        OUTPUT = """{%for bucket in table%}{{'%04d'%(loop.index-1)}}->{% for tup in bucket %}{{tup[0]}}:{{tup[1]}}{% if loop.last == false %}, {% endif %}{% endfor %}
{% endfor %}"""
        stringOutput = Environment().from_string(OUTPUT).render(table=self.table)
        return (stringOutput)

    def __str__(self):
        nonempty = [b for b in self.table if b]
        if len(nonempty) == 0:
            return ("{}")
        elif nonempty:
            valType = type(nonempty[0][0][1])
            if valType is set:
                OUTPUT = """{% raw %}{{% endraw%}{% for bucket in table %}{% for elem in bucket %}{{ elem[0] }}:{{ elem[1] }}{% endfor %}{% endfor %}{% raw %}}{% endraw%}"""
            else:
                OUTPUT = """{% raw %}{{% endraw%}{% for bucket in table %}{% for elem in bucket %}{{ elem[0] }}:{{ elem[1] }}{% if loop.last == false %}, {% endif %}{% endfor %}{% if loop.last == false %}, {% endif %}{% endfor %}{% raw %}}{% endraw%}"""
        stringOutput = Environment().from_string(OUTPUT).render(table=nonempty)
        return (stringOutput)


