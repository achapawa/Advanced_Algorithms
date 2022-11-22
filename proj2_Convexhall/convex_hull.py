from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF, QObject
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import math

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        # TODO: SORT THE POINTS BY INCREASING X-VALUE
        sorted_points = sorted(points, key=lambda x: x.x())

        t2 = time.time()

        t3 = time.time()
        # this is a dummy polygon of the first 3 unsorted points
        polygon = self.div_conquer(sorted_points, pause, view)
        # TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        All_convex_points = [QLineF(polygon[point], polygon[(point + 1) % len(polygon)])
                    for point in range(len(polygon))]
        self.showHull(All_convex_points, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    # this is the method that we call at line 74 for finding convex hall of sorted points by divide and conquer algorithm.
    def div_conquer(self, points, recursion, solve):

        # Base case: if the length of points is just one, then that represents a convex hall, no need to solve further
        length_points = len(points)
        if length_points == 1:
            return points

        # Divide all the points in two halves as: at_right and at_left halls
        half = length_points // 2
        left_hull = self.div_conquer(points[:half], recursion, solve)
        right_hull = self.div_conquer(points[half:], recursion, solve)
        # Reference: https://stackoverflow.com/questions/752308/split-list-into-smaller-lists-split-in-half

        # If both the halls have one each points then, directly combine them to make a convex hall
        if len(left_hull) == 1 and len(right_hull) == 1:
            left_hull.extend(right_hull)
            return left_hull

        # finding leftmost and rightmost in the two halves
        left_most = left_hull.index(max(left_hull, key=lambda left: left.x()))
        right_most = right_hull.index(min(right_hull, key=lambda right: right.x()))

        l = left_most
        r = right_most
        y2 = right_hull[r].y()
        y1 = left_hull[l].y()
        x2 = right_hull[r].x()
        x1 = left_hull[l].x()
        """
                Slope(gradient) = Y2-Y1 / X2-X1
                
        """
        prev_slope = (y2 - y1) / (x2 - x1)
        at_left = True
        at_right = True
        while at_right or at_left:
            at_left = False
            at_right = False
            while True:
                new_y2 = right_hull[r].y()
                new_x2 = right_hull[r].x()
                new_y1 = ((l - 1) % len(left_hull))
                new_x1 = ((l - 1) % len(left_hull))
                new_slope = (new_y2 - left_hull[new_y1].y()) / (new_x2 - left_hull[new_x1].x())
                if prev_slope > new_slope:          # check to see if the new slope is less than prev slope
                    at_left = True
                    prev_slope = new_slope
                    l = ((l - 1) % len(left_hull))
                else:
                    break
            while True:
                next_y2 = ((r + 1) % len(right_hull))
                next_x2 = ((r + 1) % len(right_hull))
                new_slope = (right_hull[next_y2].y() - left_hull[l].y()) / (right_hull[next_x2].x() - left_hull[l].x())
                if new_slope > prev_slope:    # check to see if the new slope is less than prev slope
                    at_right = True
                    prev_slope = new_slope
                    r = ((r + 1) % len(right_hull))
                else:
                    break
        upper_tangent = (l, r)

        l = left_most
        r = right_most
        y2 = right_hull[r].y()
        y1 = left_hull[l].y()
        x2 = right_hull[r].x()
        x1 = left_hull[l].x()
        """
        Slope(gradient) = Y2-Y1 / X2-X1
        """
        prev_slope = (y2 - y1) / (x2 - x1)
        at_left = True
        at_right = True
        while at_right or at_left:
            at_left = False
            at_right = False
            while True:
                Y1 = ((l + 1) % len(left_hull))
                X1 = ((l + 1) % len(left_hull))
                new_slope = (right_hull[r].y() - left_hull[Y1].y()) / (
                        right_hull[r].x() - left_hull[X1].x())
                if new_slope > prev_slope:          # check to see if the new slope is less than prev slope
                    at_left = True
                    prev_slope = new_slope
                    l = (l + 1) % len(left_hull)
                else:
                    break
            while True:
                next_Y2 = ((r - 1) % len(right_hull))
                next_X2 = ((r - 1) % len(right_hull))
                new_slope = (right_hull[next_Y2].y() - left_hull[l].y()) / (right_hull[next_X2].x() - left_hull[l].x())
                if new_slope < prev_slope:          # check to see if the new slope is less than prev slope
                    at_right = True
                    prev_slope = new_slope
                    r = (r - 1) % len(right_hull)
                else:
                    break
        lower_tangent = (l, r)

        # Now that we have found upper and lower tangent, when user selects recursion then:
        if recursion:
            self.hit_recursion(left_hull, right_hull, upper_tangent, lower_tangent)

        # Merge the two hulls to get the total Convex-hall
        Convex_list = list()  # empty list that stores convex hall points
        cur_Index = lower_tangent[0]
        upper_left = upper_tangent[0]
        Convex_list.append(left_hull[cur_Index])

        # Check the lower tangent and upper tangent at index 0
        # starting at the leftmost point of this hull, move clockwise until we reach the upperLeft point
        while cur_Index != upper_left:
            cur_Index = (cur_Index + 1) % len(left_hull)
            Convex_list.append(left_hull[cur_Index])

        cur_Index = upper_tangent[1]
        lower_right = lower_tangent[1]
        Convex_list.append(right_hull[cur_Index])

        # Check the lower tangent and upper tangent at index 1
        #  add points from upperRight to lowerRight
        while cur_Index != lower_right:
            cur_Index = (cur_Index + 1) % len(right_hull)
            Convex_list.append(right_hull[cur_Index])
        return Convex_list

    def hit_recursion(self, left_hull, right_hull, upper_tangent, lower_tangent):
        left_lines = [QLineF(left_hull[l], left_hull[(l + 1) % len(left_hull)]) for l in range(len(left_hull))]
        right_lines = [QLineF(right_hull[r], right_hull[(r + 1) % len(right_hull)]) for r in range(len(right_hull))]
        uppert_show = QLineF(left_hull[upper_tangent[0]], right_hull[upper_tangent[1]])
        lowert_show = QLineF(left_hull[lower_tangent[0]], right_hull[lower_tangent[1]])
        self.showHull(right_lines, RED)
        self.showHull(left_lines, RED)
        self.showTangent([uppert_show, lowert_show], RED)
        self.eraseHull(left_lines)
        # one of the lines still shows up, might be a bug in my code, it doesn't erase idk why
        self.eraseHull(right_lines)
        self.eraseTangent([uppert_show, lowert_show])
