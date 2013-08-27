#!/usr/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate input file for cdec')
    parser.add_argument('align', help='aligned text file from hunalign')
    args = parser.parse_args()

    stack_x = []
    stack_y = []

    with open(args.align, 'r') as f:
        for line in f:
            prob, sentence_x, sentence_y = line.strip('\n').split('\t')

            if sentence_x == '<p>' or sentence_y == '<p>':
                continue

            if not sentence_x or not sentence_y:
                if not sentence_x:
                    stack_y.append(sentence_y)
                if not sentence_y:
                    stack_x.append(sentence_x)
                continue

            if stack_x:
                sentence_x = '{0} {1}'.format(' '.join(stack_x), sentence_x)
                stack_x = []
            if stack_y:
                sentence_y = '{0} {1}'.format(' '.join(stack_y), sentence_y)
                stack_y = []
            print('{0} ||| {1}'.format(sentence_x, sentence_y))

if __name__ == '__main__':
    main()
