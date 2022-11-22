#!/usr/bin/python3

# Pawan Acharya
# CS4412
# 3/1/2022
# Project #3: Network Routing

# Reference: https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/


from ArrayQueue import ArrayQueue
from HeapQueue import HeapQueue
from CS4412Graph import *
import time




class NetworkRoutingSolver:
    def __init__( self):

        # Creating empty dictionary
        self.pointDist = {}
        self.path_dist = {}
        self.prev = {}


    def initializeNetwork( self, network ):
        assert( type(network) == CS4412Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        final_length = 0
        srcNode = self.network.nodes[self.source]

        # run till all the nodes are explored
        # Find the shortest path for destIndex
        while destIndex != srcNode.node_id:
            path_edges.append((self.network.nodes[self.prev[destIndex]].loc, self.network.nodes[destIndex].loc, '{:.0f}'.format(self.pointDist[destIndex])))
            final_length += self.pointDist[destIndex]
            destIndex = self.prev[destIndex]
        return {'cost':final_length, 'path':path_edges}

    # Now compute ShortestPaths
    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        # Calling the implemented classes on the nodes from the network of a graph.
        # If use_heap is specified, then using priority queue implementation of Heap from HeapQueue class.
        # Otherwise, using the priority queue implementation using List.
        if use_heap:
            priorityQueue = HeapQueue(self.network.getNodes())
        else:
            priorityQueue = ArrayQueue(self.network.getNodes())

        # using the empty dictionary we instantiated at the very first of this class.
        for i in self.network.getNodes():
            self.path_dist[i.node_id] = float('inf')
            self.prev[i.node_id] = None

        # Reference specified using path_dist
        self.path_dist[srcIndex] = 0

        # Now decrease key
        priorityQueue.decreaseKey(srcIndex, 0)

        # Till it is not empty
        while priorityQueue.Size() != 0:
            d_node = priorityQueue.delete_min()[0]

            # For all the neighbours iterate and find the path distance
            for i in d_node.neighbors:

                if self.path_dist[i.dest.node_id] > self.path_dist[d_node.node_id] + i.length:
                    self.path_dist[i.dest.node_id] = self.path_dist[d_node.node_id] + i.length
                    self.prev[i.dest.node_id] = d_node.node_id
                    priorityQueue.decreaseKey(i.dest.node_id, self.path_dist[i.dest.node_id])
                    self.pointDist[i.dest.node_id] = i.length

        t2 = time.time()
        return (t2 - t1)
