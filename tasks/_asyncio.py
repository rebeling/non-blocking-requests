#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://mackwerk.dk/posts/async-and-blocking-io-in-python/
import trollius
import requests

from utils import get_content


def _post(ES_URL, query):
    return get_content(requests.post(ES_URL, data=query).json())


def _do_calls(ES_URL, queries):
    loop = trollius.get_event_loop()
    futures = []
    futures_append = futures.append
    for query in queries:
        futures_append(loop.run_in_executor(None, _post, ES_URL, query))
    return futures


@trollius.coroutine
def call(ES_URL, queries):
    results = []
    results_append = results.append
    futures = _do_calls(ES_URL, queries)
    for future in futures:
        result = yield trollius.From(future)
        results_append(result)
    raise trollius.Return(results)


def call_asyncio(queries, ES_URL):
    loop = trollius.get_event_loop()
    return loop.run_until_complete(call(ES_URL, queries))
