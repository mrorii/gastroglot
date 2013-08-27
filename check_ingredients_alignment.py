#!/usr/bin/env python

import sys
import argparse
from itertools import izip

import utils

def main():
    parser = argparse.ArgumentParser(description='Check whether ja-en recipes '
                                                 'have same number of ingredients')
    parser.add_argument('ja', help='sorted ja recipes')
    parser.add_argument('en', help='sorted en recipes')
    args = parser.parse_args()

    recipes_ja = utils.load_data(args.ja)
    recipes_en = utils.load_data(args.en)

    for recipe_ja, recipe_en in izip(recipes_ja, recipes_en):
        assert(recipe_ja['id'] == recipe_en['id'])
        if len(recipe_ja['ingredients']) != len(recipe_en['ingredients']):
            print(recipe_ja['id'])

if __name__ == '__main__':
    main()
