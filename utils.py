# -*- coding: utf-8 -*-
"""
Purpose : Different Helpers for the module.
"""

import codecs
import json 

def read_list(file_path):
    with codecs.open(file_path, "r", encoding='utf-8') as f:
        l = [line.strip() for line in f.readlines()]
    return l


def write_to_json(json_file_path, data):
    """ add data (one item per line) to json file """
    with codecs.open(json_file_path, "a", encoding='utf-8') as f:
        f.write("{}\n".format(json.dumps(data)))


def join_keywords(l):
    """ join a list of keywords with '+' for BingSearch """
    return u'+'.join(l)
