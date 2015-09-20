#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
# import json
from multiprocessing import Process, Pool
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

from utils import eval_time
from utils import create_urls_set
from utils import get_query_set
from utils import prettyprinteval

from tasks.utils import get_content

from tasks._grequests import call_grequests
from tasks._requests_futures import call_requests_futures
from tasks._asyncio import call_asyncio
from tasks._tornado import call_tornado

from copy import copy

ES_URL = 'http://localhost:9200/requests-testing/document/_search'


def http_get(query):
    res = requests.post(ES_URL, data=query)
    return get_content(res.json())


pool = Pool(processes=20)
tpool = ThreadPoolExecutor(max_workers=20)
ppool = ProcessPoolExecutor(max_workers=20)

alldata = []

calls = [1, 20, 50, 100, 500]
tasks = 7
queries = get_query_set(sum(calls) * tasks, total=999999)


def split_(queries, index):
    return queries[-index:], queries[:-index]


for samplesize in calls:

    # use 1 to warm up elasticsearch
    print samplesize

    thiswalk = []
    # SAMPLES = samplesize


    # Serial - blocking I/O

    this_queries, queries = split_(queries, samplesize)
    start = time.time()
    sresult = []
    sresult_append = sresult.append
    for query in this_queries:
        res = requests.post(ES_URL, data=query)
        sresult_append(get_content(res.json()))
    thiswalk.append(["Seria", sresult, time.time()-start])


    # Grequests
    # requests and gevent - not supported anymore

    # this_queries, queries = split_(queries, samplesize)
    # start = time.time()
    # gresult = call_grequests(this_queries, ES_URL)
    # thiswalk.append(["Grequ", gresult, time.time()-start])


    # # Requests-futures
    # # https://github.com/ross/requests-futures

    this_queries, queries = split_(queries, samplesize)
    start = time.time()
    rfresult = call_requests_futures(this_queries, ES_URL, samplesize)
    thiswalk.append(["ReqFu", rfresult, time.time()-start])


    # concurrent.futures ThreadPoolExecutor

    # this_queries, queries = split_(queries, samplesize)
    # start = time.time()
    # cftresult = list(tpool.map(http_get, this_queries))
    # thiswalk.append(["cfThr", cftresult, time.time()-start])


    # # concurrent.futures ProcessPoolExecutor

    # again not running?!

    # this_queries, queries = split_(queries, samplesize)
    # start = time.time()
    # cfpresult = list(ppool.map(http_get, this_queries))
    # thiswalk.append(["cf Process", cfpresult, time.time()-start])


    # multiprocessing Pool

    # this_queries, queries = split_(queries, samplesize)
    # start = time.time()
    # mppresult = pool.map(http_get, this_queries)
    # thiswalk.append(["mpPoo", mppresult, time.time()-start])


    # # Asyncio - backported to 2.7 with trollis

    # this_queries, queries = split_(queries, samplesize)
    # start = time.time()
    # aresult = call_asyncio(this_queries, ES_URL)
    # thiswalk.append(["Async", aresult, time.time()-start])


    # tornado

    # this_queries, queries = split_(queries, samplesize)
    # start = time.time()
    # tresult = call_tornado(this_queries, ES_URL)
    # thiswalk.append(["Torna", copy(tresult), time.time()-start])


    alldata.append((samplesize, thiswalk))
    print 'done'


prettyprinteval(alldata)


# try to close all open pools and workers
try:
    pool.close() #we are not adding any more processes
    pool.join() #tell it to wait until all threads are done before going on
except Exception, e:
    raise e

try:
    ppool.shutdown()
except Exception, e:
    raise e

try:
    tpool.shutdown()
except Exception, e:
    raise e
