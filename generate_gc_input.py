#!/usr/bin/env python

import argparse
import json

import utils

def main():
    parser = argparse.ArgumentParser(description='Generate Gale-Church input')
    parser.add_argument('recipes', help='tokenized json')
    args = parser.parse_args()

    recipes = utils.load_data(args.recipes)

    for recipe in recipes:
        # print '# {0}-name'.format(recipe['id'])
        print recipe['name'].encode('utf8')
        print

        # print '# {0}-description'.format(recipe['id'])
        for desc in recipe['description']:
            print desc.encode('utf8')
        print

        # ingredients = recipe['ingredients']
        # ingredients_name = map(lambda ing: ing['name'], ingredients)
        # ingredients_quantity = map(lambda ing: ing['quantity'], ingredients)
        # print '# {0}-ingredient-name'.format(recipe['id'])
        # for ingredient_name in ingredients_name:
        #     print ingredient_name.encode('utf8')
        # print '# {0}-ingredient-quantity'.format(recipe['id'])
        # for ingredient_quantity in ingredients_quantity:
        #     print ingredient_quantity.encode('utf8')

        # print '# {0}-advice'.format(recipe['id'])
        for adv in recipe['advice']:
            print adv.encode('utf8')
        print

        # print '# {0}-history'.format(recipe['id'])
        for hist in recipe['history']:
            print hist.encode('utf8')
        print

if __name__ == '__main__':
    main()
