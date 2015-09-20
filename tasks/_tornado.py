#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado import ioloop, httpclient
from utils import get_content
import json

i = 0
toresult = []


def handle_request(response):
    global i, toresult
    toresult.append(get_content(json.loads(response.body)))
    i -= 1
    if i == 0:
        ioloop.IOLoop.instance().stop()


def call_tornado(queries, ES_URL):

    global i, toresult
    toresult = []
    http_client = httpclient.AsyncHTTPClient()
    request = httpclient.HTTPRequest(url=ES_URL, method='POST', body=None)

    for query in queries:
        i += 1
        request.body = query
        http_client.fetch(request, handle_request)

    ioloop.IOLoop.instance().start()
    return toresult
