#!/usr/bin/python3
# Reference: https://www.geeksforgeeks.org/traveling-salesman-problem-using-branch-and-bound-2/
from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    ''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

    def greedy(self, time_allowance=60.0):
        pass

    ''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''

    # REFERENCE: https://www.geeksforgeeks.org/traveling-salesman-problem-using-branch-and-bound-2/
    # REFERENCE: https://iq.opengenus.org/travelling-salesman-branch-bound/
    # REFERENCE: https://www.geeksforgeeks.org/travelling-salesman-problem-greedy-approach/
    # REFERENCE: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html

    def branchAndBound(self, time_allowance=60.0):
        # results as an empty dictionary
        results = {}
        state = 1
        cities = self._scenario.getCities()
        numCities = len(cities)
        states = 1
        num_pruned = 0
        # Empty list
        node_queue = []
        max_q_size = 0
        count_updates = 0

        # Initial bssf from defaultRandomTour, that is a random tour
        bssf = self.defaultRandomTour().get("soln")

        start_time = time.time()
        matrix_cost = self.getInitialMatrix()
        reduction_cost, lower_bound = self._reducedMatrix(matrix_cost, 0)
        start_city = cities[0]
        visited_city = [start_city]
        unvisited_city = [city for i, city in enumerate(cities) if i != 0]
        city_path = [start_city]

        # Reference: https://docs.python.org/3/library/heapq.html
        heapq.heappush(node_queue,
                       (lower_bound, state, reduction_cost, start_city, visited_city, unvisited_city, city_path))

        while ((time.time() - start_time) < time_allowance) and (len(node_queue) > 0):
            if len(node_queue) == 0:
                break
            if (len(node_queue)) > max_q_size:
                max_q_size = len(node_queue)

            # popping the unvisited, that takes O(nlogn)
            curr = heapq.heappop(node_queue)

            # If the cost is above the current bssf
            if curr[0] > bssf.cost:
                num_pruned += 1
                continue

            # looping through visited ones and finding the new reduction cost and lower bound
            for i in curr[5]:
                new_reduced_cost, new_lower_bound = self._moveToCity(curr[2].copy(), curr[0], curr[3]._index, i._index)
                new_reduced_cost, new_lower_bound = self._reducedMatrix(new_reduced_cost, new_lower_bound)
                # deep copy of the both visited and unvisited
                new_visited_city = curr[4].copy()
                new_unvisited_city = curr[5].copy()
                new_visited_city.append(i)
                new_unvisited_city.remove(i)
                new_path = curr[6].copy()
                new_path.append(i)
                if new_lower_bound < bssf.cost:
                    state += 1
                    states += 1
                    heapq.heappush(node_queue, (
                        new_lower_bound, state, new_reduced_cost, i, new_visited_city, new_unvisited_city, new_path))
                else:
                    num_pruned += 1
            # To set a new bssf, if the len is zero for current node
            if len(curr[5]) == 0:
                if curr[0] + curr[3].costTo(cities[0]) < bssf.cost:
                    bssf = TSPSolution(curr[6])
                    count_updates += 1

        end_time = time.time()

        results['cost'] = bssf.cost if bssf is not None else np.inf
        results['time'] = end_time - start_time
        results['count'] = count_updates
        results['soln'] = bssf
        results['max'] = max_q_size
        results['total'] = states
        results['pruned'] = num_pruned
        print("Total No. of bssf updates " + str(count_updates))

        return results

    ''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

    def fancy(self, time_allowance=60.0):
        start_time =time.time()
        results ={}
        cities =self._scenario.getCities
        bssf = self.defaultRandomTour().get("soln")
        nCities =len(cities)
        if nCities <= 2:
            # no cycle possible
            return results, 0

        improved =True
        while improved:
            improved = False
            for i in range(n):
                for j in range(i+1, n+1):
                    if j-1 ==1:
                        continue
                    newRoute = self.swap(self._bssf.route)


        pass

    # Creating cost matrix with O(n^2) complexity
    # a new array of given shape and type, with zero
    def getInitialMatrix(self):
        cities = self._scenario.getCities()
        numCities = len(cities)
        cost_matrix = np.zeros((numCities, numCities))
        for i in range(numCities):
            for j in range(numCities):
                if i == j:
                    cost_matrix[i, j] = np.inf
                    # continue on the next iteration
                    continue
                cost_matrix[i, j] = cities[i].costTo(cities[j])
        return cost_matrix

    # reducing the cost matrix
    def _reducedMatrix(self, matrix, lower_bound):
        for i, row in enumerate(matrix):
            minVal = np.min(row)
            if minVal == np.inf:
                continue
            row = row - minVal
            matrix[i] = row
            lower_bound = lower_bound + minVal

        # The transposed array using numpy.list.T
        for j, col in enumerate(matrix.T):
            minVal = np.min(col)
            if minVal == np.inf:
                continue
            col = col - minVal
            matrix.T[j] = col
            lower_bound = lower_bound + minVal
        return matrix, lower_bound

    # return the new matrix and the lower-bound
    def _moveToCity(self, matrix, low_bound, in_city, out_city):
        low_bound = low_bound + matrix[in_city][out_city]
        matrix[in_city].fill(np.inf)
        matrix.T[out_city].fill(np.inf)
        matrix[out_city][in_city] = np.inf
        return matrix, low_bound

    def calculateTourLength(self, tour):
        pass
