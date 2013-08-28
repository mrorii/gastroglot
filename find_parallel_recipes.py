#!/usr/bin/env python

import sys
import argparse
import json

import utils

def main():
    parser = argparse.ArgumentParser(description='Get parallel Japanese recipes')
    parser.add_argument('en', help='cookpad.en.json')
    parser.add_argument('ja', help='cookpad.ja.json')
    args = parser.parse_args()

    en_recipes = utils.load_data(args.en)
    en_recipe_ids = set(map(lambda recipe: recipe['id'], en_recipes))

    ja_recipe_ids = set()

    for ja_recipe in utils.load_data(args.ja):
        if ja_recipe['id'] in en_recipe_ids:
            print(json.dumps(ja_recipe))
        ja_recipe_ids.add(ja_recipe['id'])

    diff = en_recipe_ids - ja_recipe_ids
    if diff:
        sys.stderr.write('{0} corresponding parallel missing\n'.format(len(diff)))
        for recipe_id in sorted(diff):
            sys.stderr.write('{0}\n'.format(recipe_id))

if __name__ == '__main__':
    main()
