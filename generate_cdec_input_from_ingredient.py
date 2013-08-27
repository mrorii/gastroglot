#!/usr/bin/env python

import argparse
from itertools import izip

import utils

def main():
    parser = argparse.ArgumentParser(description='Generate cdec input from ingredients')
    parser.add_argument('ja', help='tokenized ja json')
    parser.add_argument('en', help='tokenized en json')
    args = parser.parse_args()

    recipes_ja = utils.load_data(args.ja)
    recipes_en = utils.load_data(args.en)

    for recipe_ja, recipe_en in izip(recipes_ja, recipes_en):
        assert(recipe_ja['id'] == recipe_en['id'])
        if len(recipe_ja['ingredients']) != len(recipe_en['ingredients']):
            continue

        for ing_ja, ing_en in zip(recipe_ja['ingredients'], recipe_en['ingredients']):
            print('{0} ||| {1}'.format(ing_ja['name'].encode('utf8'),
                                       ing_en['name'].encode('utf8')))
            print('{0} ||| {1}'.format(ing_ja['quantity'].encode('utf8'),
                                       ing_en['quantity'].encode('utf8')))

if __name__ == '__main__':
    main()
