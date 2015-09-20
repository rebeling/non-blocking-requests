#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grequests


def call_grequests(queries, ES_URL):

    grs = (grequests.post(ES_URL, data=q) for q in queries)
    return grequests.map(grs)
