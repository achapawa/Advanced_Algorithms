# Pawan Acharya
# CS4412
# 3/1/2022
# Project #3: Network Routing
# Reference: https://runestone.academy/ns/books/published/pythonds/Trees/BinaryHeapImplementation.html
# REFERENCE: https://www.geeksforgeeks.org/binary-heap/


# priority queue data implementation using heap for implementing Dijkstra’s and empirically verify their differences.
class HeapQueue:
    # Instantiation
    def __init__(self, node_list):
        # Creating two empty lists
        self.heap_list = []
        self.reference_array = []

        # Looping through all the list
        for node in node_list:
            self.reference_array.append(-1) # append
            self.Insert_node(node, float('inf'))

    # determine the parent, left child, and right child.

    # REFERENCE: https://www.geeksforgeeks.org/binary-heap/
    def Parent(self, i):
        return (i - 1) // 2     # Returns the parent node

    def left_child(self, i):    # Returns the left child node
        return 2 * i + 1

    def right_child(self, i):   # Returns the right child node
        return 2 * i + 2

    def Size(self):
        return len(self.heap_list)

    # remove min node from the heap_list we have declared
    def delete_min(self):
        if self.Size() == 0:
            return None
        min_node = self.heap_list[0]
        self.heap_list[0] = self.heap_list[-1]
        del self.heap_list[-1]
        self.min_heap(0)
        return min_node

    # sort to see the min node
    def min_heap(self, index):

        j=self.Size()

        left = self.left_child(index)
        right = self.right_child(index)
        if left <= j - 1 and self.heap_list[left][1] < self.heap_list[index][1]:
            min = left
        else:
            min = index
        if right <= j - 1 and self.heap_list[right][1] < self.heap_list[min][1]:
            min = right
        if (min != index):
            self.swap_positions(min, index)
            self.min_heap(min)

    # percolating a node down the tree needs decreaseKey method.
    # Reference: https://runestone.academy/ns/books/published/pythonds/Trees/BinaryHeapImplementation.html
    def decreaseKey(self, node_id, key):
        nodeIndex = self.reference_array[node_id]
        self.heap_list[nodeIndex][1] = key

        while self.heap_list[nodeIndex][1] < self.heap_list[self.Parent(nodeIndex)][1] and self.Parent(nodeIndex)>=0:
            self.swap_positions(nodeIndex, self.Parent(nodeIndex))
            nodeIndex = self.Parent(nodeIndex)

    # to swap the positions
    def swap_positions(self, i, j):
        self.heap_list[i], self.heap_list[j] = self.heap_list[j], self.heap_list[i]
        self.reference_array[self.heap_list[i][0].node_id], self.reference_array[self.heap_list[j][0].node_id] = self.reference_array[self.heap_list[j][0].node_id], self.reference_array[self.heap_list[i][0].node_id]

    # Inserting into the heap_list from given node and key using python append method.
    def Insert_node(self, node, key):
        dist = self.Size()
        self.heap_list.append([node, key])
        self.reference_array[node.node_id] = dist

        while (dist != 0):
            parent_n = self.Parent(dist)
            if self.heap_list[parent_n][1] < self.heap_list[dist][1]:
                self.swap_positions(parent_n, dist)

            dist = parent_n