# Name: Chandan Sohi
# OSU Email: sohic@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: Hash Map Implementation (Chaining)


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        This method updates the key/value pair stored in the HashMap.  It the key already exists, its associated value
        is replaced with the new value.  If the key does not exist in the HashMap, the key/value pair is added.
        """
        # get hash
        hash = self._hash_function(key)
        # calculate index
        index = hash % self._capacity

        # get bucket
        llist = self._buckets.get_at_index(index)
        # determine if the key exists
        exists = llist.contains(key)
        if exists is None:
            llist.insert(key, value)
            self._size += 1
        else:
            exists.value = value
        return

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the Hash Table.
        """
        count = 0
        # iterate through all buckets
        for index in range(0, self._capacity):
            llist = self._buckets[index]
            # check length of linkedList (bucket)
            if llist.length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        This method returns the load factor of the HashMap.
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        This method clears the HashMap Table (DynamicArray) by clearing the linkedList's stored at each index of the
        DynamicArray.
        """
        for index in range(0, self._capacity):
            self._buckets.set_at_index(index, LinkedList())
        self._size = 0
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        This method re-sizes the HashMap table to a provided new capacity.
        """
        # check to see if capacity provided is greater than 1
        if new_capacity < 1:
            return

        # store old capacity
        old_capacity = self._capacity
        # initialize temp_array to store existing data
        temp_array = DynamicArray()

        number = 0
        # iterate through old HashMap and copy stored objects to temp_array
        for index in range(0, old_capacity):
            llist = self._buckets.get_at_index(index)
            for node in llist:
                temp_array.append(node)

        # initialize new table for HashMap
        self._buckets = DynamicArray()
        for index in range(0, new_capacity):
            self._buckets.append(LinkedList())

        # change capacity and size
        self._capacity = new_capacity
        self._size = 0

        # store previously existing objects into new HashMap DynamicArray
        for index in range(0, temp_array.length()):
            # get key
            key = temp_array.get_at_index(index).key
            # get value
            value = temp_array.get_at_index(index).value
            # store value by calling the "put" method
            self.put(key, value)
        return

    def get(self, key: str) -> object:
        """
        This method returns the value stored in a HashMap for a specific key.
        """
        # get hash value
        hash = self._hash_function(key)
        # calculate index
        index = hash % self._capacity
        # get bucket (linkedList)
        llist = self._buckets.get_at_index(index)
        # check if the key is stored in the linkedList
        exists = llist.contains(key)
        # return value if exists is not None
        if exists is None:
            return None
        else:
            return exists.value

    def contains_key(self, key: str) -> bool:
        """
        This method checks to see if a key is contained in a HashMap, return True if it is, False otherwise.
        """
        # get hash value
        hash = self._hash_function(key)
        # calculate index
        index = hash % self._capacity
        # get bucket
        llist = self._buckets.get_at_index(index)
        # check bucket (linkedList) to see if it contains the key
        exists = llist.contains(key)
        if exists is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        This method removes an entry matching a given key from a HashMap.
        """
        # hash value for key
        hash = self._hash_function(key)
        # get index
        index = hash % self._capacity
        # get bucket
        llist = self._buckets.get_at_index(index)
        # see if key is stored in bucket, remove if it does
        if llist.contains(key) is None:
            return
        else:
            llist.remove(key)
            self._size -= 1
            return

    def get_keys(self) -> DynamicArray:
        """
        This method return a DynamicArray w/ all the keys from the HashMap
        """
        # initialize DynamicArray
        keys = DynamicArray()

        # iterate through all buckets
        for index in range(0, self._capacity):
            llist = self._buckets.get_at_index(index)
            # get length of bucket (linkedList)
            for node in llist:
                keys.append(node.key)
        return keys

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function return a tuple containing a dynamicArray (containing mode) and an int (frequency) of the provided
    DynamicArray.
    """
    # Set up HashMap
    map = HashMap(da.length() // 3, hash_function_1)

    # get length of provided DynamicArray
    arr_length = da.length()
    # populate hash map with key (value from DynamicArray) and value (count of number of times) a value appears in
    # the DynamicArray
    for i in range(0, arr_length):
        # get key from DynamicArray
        key = da.get_at_index(i)
        # if key is not in HashMap, value = 1
        if map.contains_key(key) is False:
            value = 1
        # else value equals current value + 1
        else:
            value = 1 + int(map.get(key))
        # update HashMap
        map.put(key, value)

    # get all keys from HashMap
    all_keys = map.get_keys()
    # set up DynamicArray to store mode
    mode = DynamicArray()
    # initialize freq to none
    freq = None


    keys_total = all_keys.length()
    # iterate through keys
    for i in range(0, keys_total):
        # get key from all_keys
        key = all_keys.get_at_index(i)
        # get value for key from HashMap
        temp = map.get(key)
        # if freq is None, set freq = temp and add key to "mode" DynamicArray
        if freq is None:
            freq = temp
            mode.append(key)
        # else if freq = temp, add key to "mode" DynamicArray
        elif freq == temp:
            mode.append(key)
        # else if temp is greater than freq, re-initialize mode DynamicArray, add key to that DynamicArray and set
        # freq = temp
        elif temp > freq:
            mode = DynamicArray()
            mode.append(key)
            freq = temp
    return mode, freq





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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
