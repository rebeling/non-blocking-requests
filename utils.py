
ES_URL = 'http://localhost:9200/torial/user/_search'

import requests
import random
import json

def eval_time(strategy, took, random_samples, result, filtered_result):
    print "%s: took %.3f seconds" % (strategy, took)
    print len(result), random_samples[0], len(filtered_result)
    print "%s/%s" % (len(filtered_result), len(result))
    print # "%.3f" % took, strategy
    # print "%.3f" % took, len(filtered_result)
    # print strategy


def get_query_set(size=None, total=None):
    random_samples = random.sample(xrange(0, total), size)
    queries = []
    for x in random_samples:
        queries.append(json.dumps({"query": {"ids": {"values": [x]}}, "_source": ["title", "content"]}))
    return queries


def create_urls_set(size=None, samples=None):
    """ Query for ids """
    # query = {"fields": ["_id"], "size": size}
    # r = requests.post(ES_URL, json=query)
    # ids = map(lambda x: x['_id'], r.json()['hits']['hits'])
    # random_samples = random.sample(ids, samples)
    random_samples = random.sample(xrange(0,100000), samples)
    queries = []
    for x in random_samples:
        queries.append(json.dumps({"query": {"ids": {"values": [x]}}, "_source": ["content_de"]}))
    return random_samples, queries



import itertools
from prettytable import PrettyTable

def prettyprinteval(alldata):

    # print alldata
    firstline = "Tasks"

    def fi(l):
        lf = len(filter(lambda x: x is not None, l))
        lr = len(l)
        return "%s/%s" % (lf, lr)


    r = []
    for samplesize, d in alldata:
        if not r:
            r.append([[firstline], map(lambda x: [x[0]], d)])

        # r.append([[str(samplesize)], map(lambda x: ["%s %s" % (fi(x[1]), ("%.5f" % x[2])) ], d)])
        r.append([[str(samplesize)], map(lambda x: ["%s" % ("%.3f" % x[2]) ], d)])


    for i,l in enumerate(r):
        if i == 0:
            merged = list(itertools.chain.from_iterable(l[1]))

            x = PrettyTable( l[0] + merged )
            x.align[firstline] = "l" # Left align city names

            for y in merged:
                x.align[y] = "r"
            x.padding_width = 1 # One space between column edges and contents (default)

        else:
            merged = list(itertools.chain.from_iterable(l[1]))
            # print "%s\t\t%s" % (l[0][0], "\t".join(merged))
            x.add_row( l[0] + merged )

    table = x.get_string().split('\n')[1:-1]
    length = len(table[1].split('+'))

    table[1] = "".join(["|:---|"] + (["---:|"] * (length-3)))

    # table[1][1] = ":" + table[1][1]
    # table[1] = ":|".join(table[1])
    # table[1] = table[1][1:]

    print "\n".join(table)
