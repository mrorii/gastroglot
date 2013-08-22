#!/usr/bin/env python

import argparse
import json

import utils
from preprocessing import sent_tokenize, word_tokenize

def sent_word_tokenize(text, lang):
    sentences = sent_tokenize(text, lang)
    return map(lambda sent: word_tokenize(sent, lang), sentences)

def main():
    parser = argparse.ArgumentParser(description='Tokenize all')
    parser.add_argument('recipes', help='recipes.json')
    parser.add_argument('--lang', choices=('en', 'ja'))
    args = parser.parse_args()

    recipes = utils.load_data(args.recipes)

    for recipe in recipes:
        name = word_tokenize(recipe['name'], args.lang)
        description = sent_word_tokenize(recipe['description'], args.lang)

        ingredients_name = map(lambda ing_name: word_tokenize(ing_name, args.lang),
                               map(lambda ing: ing['name'], recipe['ingredients']))
        ingredients_quantity = map(lambda ing_qt: word_tokenize(ing_qt, args.lang),
                                   map(lambda ing: ing['quantity'], recipe['ingredients']))
        ingredients = map(lambda pair: {'name': pair[0], 'quantity': pair[1]},
                          zip(ingredients_name, ingredients_quantity))
        instructions = map(lambda inst: sent_word_tokenize(inst, args.lang),
                           recipe['instructions'])

        advice = sent_word_tokenize(recipe['advice'], args.lang)
        history = sent_word_tokenize(recipe['history'], args.lang)

        recipe = {
            'id': recipe['id'],
            'name': name,
            'description': description,
            'ingredients': ingredients,
            'instructions': instructions,
            'advice': advice,
            'history': history,
        }
        print(json.dumps(recipe))

if __name__ == '__main__':
    main()
