# Released to students

import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils_sp18 import *
import input_validator


def validate_output(input_file, output_file, params=[]):
    print('Processing', input_file)
    
    input_data = utils.read_file(input_file)
    output_data = utils.read_file(output_file)

    input_message, input_error = input_validator.tests(input_file)
    cost, message = tests(input_data, output_data, params=params)
    message = 'Comments about input file:\n\n' + input_message + 'Comments about output file:\n\n' + message

    print(message)
    return input_error, cost, message


def validate_all_outputs(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, '.in')
    output_files = utils.get_files_with_extension(output_directory, '.out')

    all_results = []
    for input_file in input_files:
        output_file = utils.input_to_output(input_file)
        print(input_file, output_file)
        if output_file not in output_files:
            print(f'No corresponding .out file for {input_file}')
            results = (None, None, f'No corresponding .out file for {input_file}')
        else:
            results = validate_output(input_file, output_file, params=params)

        all_results.append((input_file, results))
    return all_results


def tests(input_data, output_data, params=[]):
    number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)
    G = adjacency_matrix_to_graph(adjacency_matrix)

    kingdom_tour = output_data[0]
    conquered_kingdoms = output_data[1]
    message = ''
    cost = -1

    if not all([kingdom in list_of_kingdom_names for kingdom in kingdom_tour]):
        message += 'At least one name in your tour is not in the list of kingdom names\n'
        cost = 'infinite'

    if (kingdom_tour[0] != starting_kingdom):
        message += "Your tour must start at the specified starting kingdom\n"
        cost = 'infinite'

    if not all([kingdom in kingdom_tour for kingdom in conquered_kingdoms]):
        message += 'At least one name in your conquered set does not belong to the tour\n'
        cost = 'infinite'

    kingdom_tour = convert_kingdom_names_to_indices(kingdom_tour, list_of_kingdom_names)
    conquered_kingdoms = convert_kingdom_names_to_indices(conquered_kingdoms, list_of_kingdom_names)

    if (kingdom_tour[0] != kingdom_tour[-1]):
        message += "Your tour must start and end at the same kingdom\n"
        cost = 'infinite'
    
    if cost != 'infinite':
        cost, solution_message = cost_of_solution(G, kingdom_tour, conquered_kingdoms)
        message += solution_message

    return cost, message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the output validator is run on all files in the output directory. Else, it is run on just the given output file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output', type=str, help='The path to the output file or directory')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    if args.all:
        input_directory, output_directory = args.input, args.output
        validate_all_outputs(input_directory, output_directory, params=args.params)
    else:
        input_file, output_file = args.input, args.output
        validate_output(input_file, output_file, params=args.params)
