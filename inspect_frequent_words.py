#!/usr/bin/env python

import argparse
from collections import Counter

import utils
from preprocessing import sent_tokenize, word_tokenize

def sent_word_tokenize(text, lang):
    sentences = sent_tokenize(text, lang)
    return map(lambda sent: word_tokenize(sent, lang), sentences)

def main():
    parser = argparse.ArgumentParser(description='Inspect top N frequent words')
    parser.add_argument('recipes', help='recipes as json lines')
    parser.add_argument('--lang', choices=('en', 'ja'))
    parser.add_argument('--n', help='N', type=int, default=1000)
    args = parser.parse_args()

    counter = Counter()

    def increment_by_sent(sentences):
        for sentence in sentences:
            for word in sentence.split(' '):
                counter[word] += 1

    def increment_by_word(words):
        for word in words.split(' '):
            counter[word] += 1

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

        increment_by_word(name)
        increment_by_sent(description)
        # increment_by_sent(ingredients_name)
        for instruction in instructions:
            increment_by_sent(instruction)
        increment_by_sent(advice)
        increment_by_sent(history)

    for word, count in counter.most_common(args.n):
        print('{}\t{}'.format(word.encode('utf8'), count))

if __name__ == '__main__':
    main()
