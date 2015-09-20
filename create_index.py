# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from loremipsum import get_sentences
import random
import json
from concurrent.futures import ThreadPoolExecutor
import time


# """
# Create an elasticsearch index and generate some data.
# number_of_shards effects test results
# """
# from tasks._grequests import call_grequests

es = Elasticsearch(timeout=30)
es.cluster.health(wait_for_status='yellow', request_timeout=1)


# ignore 404 and 400
es.indices.delete(index='requests-testing', ignore=[400, 404])

# ignore 400 cause by IndexAlreadyExistsException when creating an index
es.indices.create(
    index='requests-testing',
    ignore=400,
    body={"settings": {
            "index": {
                "refresh_interval": "-1",
                "number_of_shards": 5,
                "number_of_replicas": 1}}}
    )



bulksize = 10000
from_ = 1

fh = get_sentences(500)
rs = random.sample
ix = json.dumps({"create": {"_index": "requests-testing", "_type": "document", "_id": "x"}})




# for h in xrange(1, 11):
#     to_ = bulksize * h
#     # print from_, to_

#     data = []
#     data_append = data.append
#     for i in xrange(from_, to_):
#         # print '\t', i
# #         # print '\t', i
#         data_append(ix.replace('x', str(i)))
#         data_append(json.dumps({"title": rs(fh, 1), "content": rs(fh, 8)}))

#     # POST /_bulk
#     es.bulk(body=data, index="requests-testing")
#     # print h
#     from_ = bulksize * h



# bulksize = 30
# from_ = 1






# def index_data():
#     try:
#         while True:
#             data = (yield)
#             # POST /_bulk
#             es.bulk(body=data, index="requests-testing")

#     except GeneratorExit:
#         print "Kaboom!"

# r = index_data()
# r.next()


# for h in xrange(1, 11):
#     to_ = bulksize * h

#     data = []
#     data_append = data.append
#     for i in xrange(from_, to_):
#         data_append(ix.replace('x', str(i)))
#         data_append(json.dumps({"title": rs(fh, 1), "content": rs(fh, 8)}))

#     r.send(data)
#     from_ = bulksize * h

# r.close()


def _bulk((from_, to_)):

    global ix, rs, fh, es

    data = []
    data_append = data.append
    # print from_, to_
    for i in xrange(from_, to_):
        data_append(ix.replace('x', str(i)))
        data_append(json.dumps({"title": rs(fh, 1), "content": rs(fh, 8)}))

    try:
        es.bulk(body=data, index="requests-testing")
        return True
    except Exception, e:
        return e

    # res = requests.post(ES_URL, data=query)
    # return get_content(res.json())




# tpool = ThreadPoolExecutor(max_workers=30)
tpool = ThreadPoolExecutor(max_workers=10)

ids = []
ids_append = ids.append
for h in xrange(1, 101):
    to_ = bulksize * h
    print from_, to_
    ids_append((from_, to_))
    from_ = bulksize * h


start = time.time()
r = list(tpool.map(_bulk, ids))

print time.time()-start
# print r


try:
    tpool.shutdown()
except Exception, e:
    raise e
