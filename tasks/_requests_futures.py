#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import get_content
from requests_futures.sessions import FuturesSession


# helper
def bg_cb(sess, resp):
    # prepare item content
    resp.data = get_content(resp.json())


def call_requests_futures(queries, ES_URL, samplesize):

    session = FuturesSession(max_workers=samplesize)
    return map(lambda x: session.post(
        ES_URL, data=x, background_callback=bg_cb), queries)
