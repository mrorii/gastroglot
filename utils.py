#!/usr/bin/env python

import json

def load_data(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield json.loads(line.strip())
