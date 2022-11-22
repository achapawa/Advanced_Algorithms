# Pawan Acharya
# CS4412
# 3/1/2022
# Project #3: Network Routing

# REFERENCES:
# Runestone Academy
# https://runestone.academy/ns/books/published/pythonds/BasicDS/ImplementingaQueueinPython.html#google_vignette
# https://algs4.cs.princeton.edu/24pq/IndexMinPQ.java.html

# Implementing priority Queue using python list
class ArrayQueue:
    # Instantiation
    def __init__(self, node_list):
        # An empty list
        self.Queue = []

        # Insert into the list of nodes
        for i in node_list:
            self.Insert_node(i, float('inf'))

    # get the size of the list using len
    def Size(self):
        return len(self.Queue)

    # To check empty or not
    def isEmpty(self):
        return self.Queue == []

    # Delete the minimum node from Queue
    def delete_min(self):
        if self.isEmpty():
            return None
        min = self.Queue.pop(0)
        return min

    # Now, decreasing the value of key
    def decreaseKey(self, node_id, key):
        for i, j in enumerate(self.Queue):
            # for all the nodes at their indices, check the nodeID.
            if node_id == j[0].node_id:
                self.Queue[i][1] = key
                index = i

        while self.Queue[index][1] < self.Queue[index - 1][1] and index-1 >= 0:
            self.swap_positions(index, index - 1)
            index = index - 1

    # to swap in the above function
    def swap_positions(self, initial, decreased):
        self.Queue[initial], self.Queue[decreased] = self.Queue[decreased], self.Queue[initial]

    # insert the node
    def Insert_node(self, NODE, KEY):
        i = self.Size()
        self.Queue.append([NODE, KEY])

        while self.Queue[i][1] < self.Queue[i - 1][1] and i - 1 >= 0:
            self.swap_positions(i, i - 1)
            i = i - 1