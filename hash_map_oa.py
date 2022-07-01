# Name: Chandan Sohi
# OSU Email: sohic@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: Hash Map Implementation Using Open Addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If the given key already exists in the hash map, its
        associated value is replaced with the new value. If the given key is not in the hash map, the key / value pair
        is added.
        """
        # Check table load and re-size if needed
        if self.table_load() >= 0.5:
            self.resize_table(2*self._capacity)

        # get hash and calculate initial index
        hash = self._hash_function(key)
        indexInitial = hash % self._capacity

        # get bucket
        bucket = self._buckets.get_at_index(indexInitial)

        # if bucket is None or bucket.is_tombstone is True, insert new HashEntry at indexInitial
        if bucket is None or bucket.is_tombstone is True:
            self._buckets.set_at_index(indexInitial, HashEntry(key, value))
            self._size += 1
            return
        # else if bucket key matches required key, change bucket.value to match passed value
        elif bucket.key == key:
            bucket.value = value
            return
        # else keep on searching for key using open addressing
        else:
            j = 0
            found = False
            while found is False:
                j += 1
                # quadratic probing
                i = (indexInitial + j**2) % self._capacity
                bucket = self._buckets.get_at_index(i)
                # if bucket is none or bucket.is-tombstone is True
                if bucket is None or bucket.is_tombstone is True:
                    self._buckets.set_at_index(i, HashEntry(key, value))
                    self._size += 1
                    found = True
                # else if the bucket key matches
                elif bucket.key == key:
                    bucket.value = value
                    found = True
            return

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table
        """
        count = 0
        for i in range(0, self._capacity):
            bucket = self._buckets.get_at_index(i)
            if bucket is None:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs remain in the
        new hash map, and all hash table links are rehashed. If new_capacity is less than 1, or less than the
        current number of elements in the map, the method does nothing
        """
        # Check for valid new_capacity, more than 1 and self._size
        if new_capacity < 1 or new_capacity < self._size:
            return

        # initialize temp_array to store existing HashEntry objects
        temp_array = DynamicArray()
        count = 0

        # store existing HashEntry objects into temp_array
        for index in range(0, self._capacity):
            entry = self._buckets.get_at_index(index)
            if entry is not None and entry.is_tombstone is False:
                temp_array.append(entry)
                count += 1

        # initialize a new HashTable, and set capacity to ne_capacity and size to 0
        self._buckets = DynamicArray()
        for i in range(0, new_capacity):
            self._buckets.append(None)
        self._capacity = new_capacity
        self._size = 0

        # rehash existing HashEntry objects and store them into new HashTable
        for i in range(0, count):
            entry = temp_array.get_at_index(i)
            key = entry.key
            value = entry.value
            self.put(key, value)
        return

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash map, the method
        returns None.
        """
        # get initial index
        hash = self._hash_function(key)
        indexInitial = hash % self._capacity

        # get bucket for initial index
        bucket = self._buckets.get_at_index(indexInitial)
        # if the bucket is none, return
        if bucket is None:
            return
        # if bucket.key = key and bucket.is_tombstone is False, return bucket.value
        elif bucket.key == key and bucket.is_tombstone is False:
            return bucket.value
        # else use quadratic probing to continue search
        else:
            j = 0
            # search while bucket is not None
            while bucket is not None:
                j += 1
                i = (indexInitial + j ** 2) % self._capacity
                bucket = self._buckets.get_at_index(i)
                # if bucket.key = key and bucket.is_tombstone is False, return bucket.value
                if bucket is not None and bucket.key == key and bucket.is_tombstone is False:
                    return bucket.value
            return

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False.
        """
        # get initial index
        hash = self._hash_function(key)
        indexInitial = hash % self._capacity

        # locate bucket
        bucket = self._buckets.get_at_index(indexInitial)
        # if bucket is None, return False
        if bucket is None:
            return False
        # else if bucket.key = key and bucket.is_tombstone is False
        elif bucket.key == key and bucket.is_tombstone is False:
            return True
        # else use quadratic probing to continue search
        else:
            j = 0
            # search while bucket is not None
            while bucket is not None:
                j += 1
                i = (indexInitial + j ** 2) % self._capacity
                bucket = self._buckets.get_at_index(i)
                # if bucket.key = key and bucket.is_tombstone is False, return True
                if bucket is not None and bucket.key == key and bucket.is_tombstone is False:
                    return True
            return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map
        """
        if self.contains_key(key) is False:
            return

        # get initial index
        hash = self._hash_function(key)
        indexInitial = hash % self._capacity

        # get to appropriate bucket
        bucket = self._buckets.get_at_index(indexInitial)
        # if bucket is none, return
        if bucket is None:
            return
        # else if bucket.key = key and bucket.is_tombstone is False, set bucket.is_tombstone to True, reduce self._size
        elif bucket.key == key and bucket.is_tombstone is False:
            bucket.is_tombstone = True
            self._size -= 1
            return
        # else continue searching using quadratic probing
        else:
            j = 0
            # while bucket does not equal None
            while bucket is not None:
                j += 1
                i = (indexInitial + j ** 2) % self._capacity
                bucket = self._buckets.get_at_index(i)
                # if bucket.key = key and bucket.is_tombstone is False, set bucket.is_tombstone to True, reduce
                # self._size
                if bucket is not None and bucket.key == key and bucket.is_tombstone is False:
                    bucket.is_tombstone = True
                    self._size -= 1
            return

    def clear(self) -> None:
        """
        This method clears the contents of the hash map without changing its capacity
        """
        for index in range(0, self._capacity):
            self._buckets.set_at_index(index, None)
        self._size = 0
        return

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map
        """
        # initialize DynamicArray to store keys
        keys = DynamicArray()
        # iterate through the HashMap table
        for index in range(0, self._capacity):
            bucket = self._buckets.get_at_index(index)
            # if bucket is not None and bucket.is_tombstone is False add to keys (DynamicArray)
            if bucket is not None and bucket.is_tombstone is False:
                    keys.append(bucket.key)
        return keys


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
