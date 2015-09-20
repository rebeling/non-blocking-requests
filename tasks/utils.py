#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_content(hit):
    try:
        return hit['hits']['hits'][0]['_source']['content']
    except Exception, e:
        print e
        return None
