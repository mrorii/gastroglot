#!/usr/bin/env python

import argparse
import os
from itertools import izip

import utils

def get_filename(prefix, i, suffix):
    return os.path.abspath('{0}.{1}.{2}'.format(prefix, i, suffix))

def print_item_to_file(f, item, heading='<p>'):
    f.write('{0}\n'.format(heading))
    f.write('{0}\n'.format(item.encode('utf8')))

def print_items_to_file(f, items, heading='<p>'):
    f.write('{0}\n'.format(heading))
    for item in items:
        f.write('{0}\n'.format(item.encode('utf8')))

def print_itemss_to_file(f, itemss, heading='<p>'):
    f.write('{0}\n'.format(heading))
    for items in itemss:
        for item in items:
            f.write('{0}\n'.format(item.encode('utf8')))

def main():
    parser = argparse.ArgumentParser(description='Generate input files for hunalign')
    parser.add_argument('ja', help='tokenized ja json')
    parser.add_argument('en', help='tokenized en json')
    parser.add_argument('prefix', help='output prefix')
    parser.add_argument('batchfile', help='output batchfile')
    parser.add_argument('--b', help='approximate batch size', type=int, default=5000)
    args = parser.parse_args()

    recipes_ja = utils.load_data(args.ja)
    recipes_en = utils.load_data(args.en)

    iteration = 1
    langs = ('ja', 'en')
    num_lines = [0 for _ in langs]  # keep track of the number of lines printed out
    output_filenames = [get_filename(args.prefix, iteration, lang) for lang in langs]
    output_files = [open(filename, 'w') for filename in output_filenames]

    batchfile_output = [(output_filenames[0], output_filenames[1],
                         get_filename(args.prefix, iteration, 'align'))]

    for recipes in izip(recipes_ja, recipes_en):
        for index, lang in enumerate(langs):
            recipe = recipes[index]
            output_file = output_files[index]

            print_item_to_file(output_file, recipe['name'])
            print_items_to_file(output_file, recipe['description'])
            print_itemss_to_file(output_file, recipe['instructions'])
            print_items_to_file(output_file, recipe['advice'])
            print_items_to_file(output_file, recipe['history'])

            num_lines[index] += (1 + # name
                                 len(recipe['description']) +
                                 sum(map(lambda inst: len(inst), recipe['instructions'])) +
                                 len(recipe['advice']) +
                                 len(recipe['history']))


        if any(map(lambda num_line: num_line > args.b, num_lines)):
            for output_file in output_files:
                output_file.close()

            # reset
            iteration += 1
            num_lines = [0 for _ in langs]
            output_filenames = [get_filename(args.prefix, iteration, lang) for lang in langs]
            output_files = [open(filename, 'w') for filename in output_filenames]

            batchfile_output.append((output_filenames[0], output_filenames[1],
                                     get_filename(args.prefix, iteration, 'align')))

    for output_file in output_files:
        output_file.close()

    with open(args.batchfile, 'w') as f:
        for output in batchfile_output:
            f.write('{0}\t{1}\t{2}\n'.format(*output))

if __name__ == '__main__':
    main()
