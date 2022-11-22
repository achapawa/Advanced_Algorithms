#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


class GeneSequencing:

    def __init__(self):
        self.alignment2 = None
        self.alignment1 = None

    # This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
    # handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
    # you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
    # how many base pairs to use in computing the alignment

    def align(self, sequences, table, banded, align_length):
        self.banded = banded
        self.max_char = align_length
        results = []

        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):

                if self.banded:
                    cost = self.banded_Align(sequences[i], sequences[j])
                else:
                    cost = self.full_Align(sequences[i], sequences[j])

                if j < i:
                    s = {}
                else:
                    ###################################################################################################
                    # your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
                    score = cost
                    alignment1 = self.alignment1.format(i + 1,
                                                        len(sequences[i]), align_length, ',BANDED' if banded else '')
                    alignment2 = self.alignment2.format(j + 1,
                                                        len(sequences[j]), align_length, ',BANDED' if banded else '')
                    ###################################################################################################
                    s = {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
                    table.item(i, j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.update()
                jresults.append(s)
            results.append(jresults)
        return results

    # look up in the 2D array
    def Array_pair(self, array, track_array, i, j, char):
        # upper, left and the diagonal array
        upper = array[i - 1][j]
        left = array[i][j - 1]
        diagonal = array[i - 1][j - 1]
        # Look for the character, if yes
        if char:
            new_num = diagonal + MATCH
            track_array[i][j] = "D"
        else:
            new_num = diagonal + SUB
            track_array[i][j] = "D"
        # Check the new number obtained above
        if new_num > (left + INDEL):
            new_num = left + INDEL
            track_array[i][j] = "L"

        if new_num > (upper + INDEL):
            new_num = upper + INDEL
            track_array[i][j] = "A"
        # Return the number
        return new_num

    # solve the alignment, and set no alignment possible for i,j which are none.
    def solve_sequence(self, top, side, back_reference):
        i = None
        j = None
        char_top = len(top)
        char_side = len(side)
        # loop through the top and side.
        while back_reference[char_side][char_top] is not None:
            source = back_reference[char_side][char_top]
            if source == "D":
                if i is not None:
                    i += top[char_top - 1]
                else:
                    i = top[char_top - 1]

                if j is not None:
                    j += side[char_side - 1]
                else:
                    j = side[char_side - 1]
                char_top -= 1
                char_side -= 1

            elif source == "L":
                if i is not None:
                    i += top[char_top - 1]
                else:
                    i = top[char_top - 1]

                if j is not None:
                    j += "-"
                else:
                    j = "-"

                char_top -= 1

            elif source == "A":
                if i is not None:
                    i += "-"
                else:
                    i = "-"
                if j is not None:
                    j += side[char_side - 1]
                else:
                    j = side[char_side - 1]

                char_side -= 1

        if i is None:
            self.alignment1 = "No Alignment Possible"
        else:
            i = i[::-1]
            self.alignment1 = i[:100]

        if j is None:
            self.alignment2 = "No Alignment Possible"
        else:
            j = j[::-1]
            self.alignment2 = j[:100]

    # Populate the scoring and path matrix using this full align 
    # time O(n*m) where n is the length of seq1 and m is the length of seq2
    def full_Align(self, seq1, seq2):
        align_max = self.max_char
        top_Seq = list(seq1)
        side_Seq = list(seq2)

        if len(seq1) > align_max:
            n = align_max
            top_Seq = list(seq1[:align_max])
        else:
            n = len(seq1)

        # check the size of column array
        if len(seq2) > align_max:
            m = align_max
            side_Seq = list(seq2[:align_max])
        else:
            m = len(seq2)

        column = n + 1 
        row = m + 1

        sc_matrix = [[0 for i in range(column)] for j in range(row)]
        sc_matrix[0][0] = 0
        back_point = [["-" for i in range(column)] for j in range(row)]
        back_point[0][0] = None

        for i in range(1, row):
            sc_matrix[i][0] = i * INDEL
            back_point[i][0] = "A"

        for j in range(1, column):
            sc_matrix[0][j] = j * INDEL
            back_point[0][j] = "L"

        # time complexity O(nm)
        for i in range(1, row):
            for j in range(1, column):
                char1 = side_Seq[i - 1]
                char2 = top_Seq[j - 1]
                characters = char1 == char2
                sc_matrix[i][j] = self.Array_pair(sc_matrix, back_point, i, j, characters)
        self.solve_sequence(top_Seq, side_Seq, back_point)
        return sc_matrix[row - 1][column - 1]

    # For banded align
    def banded_matrix(self, array_m, pointer, top, side, i, j):
        result = math.inf
        if j == 0:
            left = math.inf
            diag = array_m[i - 1][j]
            upper = array_m[i - 1][j + 1]
        elif j == 6:
            upper = math.inf
            diag = array_m[i - 1][j]
            left = array_m[i][j - 1]
        else:
            diag = array_m[i - 1][j]
            left = array_m[i][j - 1]
            upper = array_m[i - 1][j + 1]

        if diag is not math.inf:
            if i - (4 - j) > len(top) - 1:
                return math.inf
            else:
                if top[i - (4 - j)] == side[i - 1]:
                    result = diag + MATCH
                    pointer[i][j] = "D"
                else:
                    result = diag + SUB
                    pointer[i][j] = "D"

        if left is not math.inf:
            if result > (left + INDEL):
                result = left + INDEL
                pointer[i][j] = "L"

        if upper is not math.inf:
            if result > (upper + INDEL):
                result = upper + INDEL
                pointer[i][j] = "A"
        return result


    def bandedCompute_Seq(self, top_Seq, side_Seq, backtrack, row, col):
        index_i = None  # O(1)
        index_k = None  # O(1)

        while backtrack[row - 1][col] is not None:
            source = backtrack[row - 1][col]

            if source == "D":
                if index_i is not None:
                    index_i += top_Seq[row - (4 - col) - 1]
                else:
                    index_i = top_Seq[row - (4 - col) - 1]

                if index_k is not None:
                    index_k += side_Seq[row - 2]
                else:
                    index_k = side_Seq[row - 2]

                row -= 1

            elif source == "L":
                if index_i is not None:
                    index_i += top_Seq[row - (4 - col) - 1]
                else:
                    index_i = top_Seq[row - (4 - col) - 1]

                if index_k is not None:
                    index_k += "-"
                else:
                    index_k = "-"

                col -= 1

            elif source == "A":
                if index_i is not None:
                    index_i += "-"
                else:
                    index_i = "-"
                if index_k is not None:
                    index_k += side_Seq[row - 2]
                else:
                    index_k = side_Seq[row - 2]

                row -= 1
                col += 1

        if index_i is None:
            self.alignment1 = "No Alignment Possible"
        else:
            index_i = index_i[::-1]
            self.alignment1 = index_i[:100]

        if index_k is None:
            self.alignment2 = "No Alignment Possible"
        else:
            index_k = index_k[::-1]
            self.alignment2 = index_k[:100]

    # Here the overall time complexity and space complexity is O(kn) where k is 7 and
    # n is the shortest size between top_Seq and side_Seq
    def banded_Align(self, seq1, seq2):
        maximum_Alig = self.max_char
        top_Seq = list(seq1)
        side_Seq = list(seq2)

        # checking what is the size of column n in 2D arry which runs in O(1)
        if (len(seq1) > maximum_Alig):
            n = maximum_Alig
            top_Seq = list(seq1[:maximum_Alig])
        else:
            n = len(seq1)

        # checking what is the size of column m in 2D arry which runs in O(1)
        if (len(seq2) > maximum_Alig):
            m = maximum_Alig
            side_Seq = list(seq2[:maximum_Alig])
        else:
            m = len(seq2)

        cols = n + 1
        row = m + 1

        difference = cols - row

        if difference > MAXINDELS or difference < -MAXINDELS:
            self.alignment1 = "No Alignment Possible"
            self.alignment2 = "No Alignment Possible"
            return math.inf

        if len(top_Seq) > len(side_Seq):
            big_seq = True
        else:
            big_seq = False

        diff_length = abs(len(top_Seq) - len(side_Seq))

        if (big_seq):
            row = len(side_Seq) + 1 + diff_length
            temp = top_Seq
            top_Seq = side_Seq
            side_Seq = temp

        else:
            row = len(top_Seq) + 1 + diff_length

        col = (2 * MAXINDELS) + 1

        arry = [["nil" for i in range(col)] for j in range(row)]
        backtrack = [["-" for i in range(col)] for j in range(row)]

        # Setting the base cases of arrays which runs in o(1)
        arry[0][3] = 0
        arry[0][4] = 5
        arry[0][5] = 10
        arry[0][6] = 15

        arry[1][2] = 5
        arry[2][1] = 10
        arry[3][0] = 15

        backtrack[0][3] = None
        backtrack[0][4] = "L"
        backtrack[0][5] = "L"
        backtrack[0][6] = "L"

        backtrack[1][2] = "A"
        backtrack[2][1] = "A"
        backtrack[3][0] = "A"

        # Setting the upper_side and lower triangle which are not in the array
        arry[0][0] = math.inf
        arry[0][1] = math.inf
        arry[0][2] = math.inf
        arry[1][0] = math.inf
        arry[1][1] = math.inf
        arry[2][0] = math.inf
        arry[row - 1][6] = math.inf
        arry[row - 1][5] = math.inf
        arry[row - 1][4] = math.inf
        arry[row - 2][6] = math.inf
        arry[row - 2][5] = math.inf
        arry[row - 3][6] = math.inf

        for i in range(0, row):
            for j in range(0, col):
                if arry[i][j] == "nil":
                    arry[i][j] = self.banded_matrix(arry, backtrack, top_Seq, side_Seq, i, j)

        cols = MAXINDELS
        while arry[row - 1][cols] is math.inf:
            cols -= 1
        self.bandedCompute_Seq(top_Seq, side_Seq, backtrack, row, cols)
        return arry[row - 1][cols]
