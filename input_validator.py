# Released to students

import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import networkx as nx
import numpy as np
# from utils_sp18 import *
from student_utils_sp18 import *
# import planarity

RANGE_OF_INPUT_SIZES = range(201)
MAX_NAME_LENGTH = 20


def validate_input(input_file, params=[]):
    print('Processing', input_file)
    tests(input_file, params)
    return    


def validate_all_inputs(input_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        validate_input(input_file, params=params)


def tests(input_file, params=[]):
    input_data = utils.read_file(input_file)
    number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)

    if (int(input_data[0][0]) not in RANGE_OF_INPUT_SIZES):
        print(f'Your input does not belong to the valid range of input sizes ({RANGE_OF_INPUT_SIZES})')

    if not len(list_of_kingdom_names) == number_of_kingdoms:
        print(f'The number of kingdom names you listed ({len(list_of_kingdom_names)}) differs from the number you gave on the first line ({number_of_kingdoms})')

    if not len(adjacency_matrix) == len(adjacency_matrix[0]) == number_of_kingdoms:
        print(f'The dimensions of your adjacency matrix ({len(adjacency_matrix)} x {len(adjacency_matrix[0])}) do not match the number of kingdoms you provided ({number_of_kingdoms})')

    if not all(entry == 'x' or (type(entry) is float and entry > 0 and entry <= 2e9 and decimal_digits_check(entry)) for row in adjacency_matrix for entry in row):
        print(f'Your adjacency matrix may only contain the character "x", or strictly positive integers less than 2e+9, or strictly positive floats with less than 5 decimal digits')
    
    if not len(set(list_of_kingdom_names)) == len(list_of_kingdom_names):
        print('Your kingdom names are not distinct')
    
    if not all(name.isalnum() and len(name) <= MAX_NAME_LENGTH for name in list_of_kingdom_names):
        print(f'One or more of your kingdom names are either not alphanumeric or are above the max length of {MAX_NAME_LENGTH}')

    if not starting_kingdom in list_of_kingdom_names:
        print('Your starting kingdom is not in the list of kingdom names')

    G = adjacency_matrix_to_graph(adjacency_matrix)

    if not nx.is_connected(G):
        print('Your graph is not connected')

    if not is_metric(G):
        print('Your graph is not metric')

    print("If you've received no other error messages, then your input is valid!")

    # edge_list = utils.adjacency_matrix_to_edge_list(adjacency_matrix)
    # if not planarity.is_planar(edge_list):
    #     print(f'Your graph is not planar')


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

