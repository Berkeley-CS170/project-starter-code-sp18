# Released to students

import sys
sys.path.append('..')
sys.path.append('../..')
import os
import argparse
import utils
import networkx as nx
import numpy as np
from student_utils_sp18 import *

# Change these if you want to allow files with different names and/or graph sizes
RANGE_OF_INPUT_SIZES = [50, 100, 200]
VALID_FILENAMES = ['50.in', '100.in', '200.in']
MAX_NAME_LENGTH = 20


def validate_input(input_file, params=[]):
    print('Processing', input_file)
    message, error = tests(input_file, params)
    print(message)


def validate_all_inputs(input_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        validate_input(input_file, params=params)


def tests(input_file, params=[]):
    input_data = utils.read_file(input_file)
    number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)
    message = ''
    error = False

    file_basename = os.path.basename(input_file)
    if file_basename not in VALID_FILENAMES:
        message += f'Your file is named {file_basename}. The allowed file names are: {RANGE_OF_INPUT_SIZES}'
        error = True

    for i in range(len(RANGE_OF_INPUT_SIZES)):
        if file_basename == VALID_FILENAMES[i] and (int(input_data[0][0]) > RANGE_OF_INPUT_SIZES[i]):
            message += f'Your file is named {file_basename}, but the size of the input is {input_data[0][0]}\n'
            error = True

    if not len(list_of_kingdom_names) == number_of_kingdoms:
        message += f'The number of kingdom names you listed ({len(list_of_kingdom_names)}) differs from the number you gave on the first line ({number_of_kingdoms})\n'
        error = True

    if not len(adjacency_matrix) == len(adjacency_matrix[0]) == number_of_kingdoms:
        message += f'The dimensions of your adjacency matrix ({len(adjacency_matrix)} x {len(adjacency_matrix[0])}) do not match the number of kingdoms you provided ({number_of_kingdoms})\n'
        error = True

    if not all(entry == 'x' or (type(entry) is float and entry > 0 and entry <= 2e9 and decimal_digits_check(entry)) for row in adjacency_matrix for entry in row):
        message += f'Your adjacency matrix may only contain the character "x", or strictly positive integers less than 2e+9, or strictly positive floats with less than 5 decimal digits\n'
        error = True

    adjacency_matrix_numpy = np.matrix(adjacency_matrix)
    if not np.all(adjacency_matrix_numpy.T == adjacency_matrix_numpy):
        message += f'Your adjacency matrix is not symmetric\n'
        error = True
    
    if not len(set(list_of_kingdom_names)) == len(list_of_kingdom_names):
        message += 'Your kingdom names are not distinct\n'
        error = True
    
    if not all(name.isalnum() and len(name) <= MAX_NAME_LENGTH for name in list_of_kingdom_names):
        message += f'One or more of your kingdom names are either not alphanumeric or are above the max length of {MAX_NAME_LENGTH}\n'
        error = True

    if not starting_kingdom in list_of_kingdom_names:
        message += 'Your starting kingdom is not in the list of kingdom names\n'
        error = True

    G = adjacency_matrix_to_graph(adjacency_matrix)

    if not nx.is_connected(G):
        message += 'Your graph is not connected\n'
        error = True

    if not is_metric(G):
        message += 'Your graph is not metric\n'
        error = True

    message += "If you've received no other error messages, then your input is valid!\n\n\n"
    return message, error


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the input validator is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    if args.all:
        input_directory = args.input
        validate_all_inputs(input_directory, params=args.params)
    else:
        input_file = args.input
        validate_input(input_file, params=args.params)

