from mrjob.job import MRJob
from itertools import groupby
from functools import reduce
#-------------------------------------------------------------------------
'''
    Problem 4:
    In this problem, you will use mapreduce framework to implement matrix multipication.
    You could test the correctness of your code by typing `nosetests test4.py` in the terminal.
'''

#--------------------------
class MatMul(MRJob):
#--------------------------
    '''
        Given a matrix A and a matrix B, compute the product A*B = C
    '''

    #----------------------
    @staticmethod
    def parse_line(line):
        '''
            parse one line of text from the data file.
            Input:
                    line: one line of text of a data record
            return:
                    matrix_name: 'A' or 'B'
                    i: row index, an integer (note, the index starts from 1)
                    j: column index (note, the index starts from 1)
                    v: the value of the entry;
                    nr: number of rows in the matrix C
                    nc: number of columns in the matrix C
        '''
        #########################################
        ## INSERT YOUR CODE HERE
        def cast_proper_dtypes(args):
            elem, dtype = args
            return dtype(elem)

        dtypes = [str] + [int] * 2 + [float] + [int] * 2
        line_info = zip(line.split(','), dtypes)
        matrix_name, i, j, v, nr, nc = map(cast_proper_dtypes, line_info)

        #########################################
        return matrix_name, i,j,v, nr, nc

    #----------------------
    def mapper(self, in_key, in_value):
        '''
            mapper function, which process a key-value pair in the data and generate intermediate key-value pair(s)
            Input:
                    in_key: the key of a data record (in this example, can be ignored)
                    in_value: the value of a data record, (in this example, it is a line of text string in the data file, check 'matrix.csv' for example)
            Yield:
                    (out_key, out_value) :intermediate key-value pair(s). You need to design the format and meaning of the key-value pairs. These intermediate key-value pairs will be feed to reducers, after grouping all the values with a same key into a value list.
        '''

        # parse one line of text data
        matrix_name,  i,j,v, nr, nc = self.parse_line(in_value)

        #########################################
        ## INSERT YOUR CODE HERE

        # generate output key-value pairs
        is_matrix_A = matrix_name == 'A'
        multiplier = nc if is_matrix_A else nr

        yield from [ (('C', i if is_matrix_A else x, x if is_matrix_A else j), (matrix_name, i, j, v)) for x in range(1, multiplier+1)]


        #########################################

    #----------------------
    def reducer(self, in_key, in_values):
        '''
            reducer function, which processes a key and value list and produces output key-value pair(s)
            Input:
                    in_key: an intermediate key from the mapper
                    in_values: a list (generator) of values , which contains all the intermediate values with the same key (in_key) generated by all mappers
            Yield:
                    (out_key, out_value) : output key-value pair(s).
        '''
        #########################################
        ## INSERT YOUR CODE HERE

        def format_indices(x):
            matrix_name, i, j, v = x
            if matrix_name == 'B':
                temp_ = j
                j = i
                i = temp_
            return matrix_name, i, j, v

        in_values = map(format_indices, in_values)

        def get_group_key(x):
            matrix_name, i, j, v = x
            return '-'.join(map(str, [i,j]))

        groups = []
        in_values = sorted(in_values, key=get_group_key)
        for k, g in groupby(in_values, get_group_key):
            groups.append(list(g))

        value_pairs = [[v for matrix_name, i, j, v in sublist] for sublist in groups]
        out_value = reduce(lambda x, y: x+y, [reduce(lambda x, y: x*y, sublist) for sublist in value_pairs])

        yield in_key, out_value

        #########################################

