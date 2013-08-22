#!/usr/bin/env python

import argparse
import json

import utils

def main():
    parser = argparse.ArgumentParser(description='Sort recipes')
    parser.add_argument('recipes', help='recipes.json')
    args = parser.parse_args()

    recipes = utils.load_data(args.recipes)
    for recipe in sorted(recipes, key=lambda recipe: recipe['id']):
        print(json.dumps(recipe))

if __name__ == '__main__':
    main()
