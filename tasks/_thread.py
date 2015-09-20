#!/usr/bin/env python
# -*- coding: utf-8 -*-









# threads

# from threading import Thread, enumerate
# from urllib import urlopen
# from time import sleep

# UPDATE_INTERVAL = 0.01

# class URLThread(Thread):
#     def __init__(self,query):
#         super(URLThread, self).__init__()
#         self.query = query
#         self.response = None

#     def run(self):
#         self.request = urlopen(ES_URL, data=self.query)
#         self.response = self.request #.read()

# def multi_get(queries, timeout=0.0): #timeout=2.0):
#     def alive_count(lst):
#         alive = map(lambda x : 1 if x.isAlive() else 0, lst)
#         return reduce(lambda a,b : a + b, alive)

#     threads = [URLThread(query) for query in queries]

#     for thread in threads:
#         thread.start()
#     while alive_count(threads) > 0 and timeout > 0.0:
#         timeout = timeout - UPDATE_INTERVAL
#         sleep(UPDATE_INTERVAL)
#     return [x.response for x in threads]





    # # Pool
    # # http://lethain.com/parallel-http-requests-in-python/

    # random_samples, queries = create_urls_set(size=SIZE, samples=SAMPLES)
    # strategy = "threads"
    # start = time.time()

    # result = []
    # mg_requests = multi_get(queries, timeout=1.5)
    # for data in mg_requests:
    #     result.append(data)

    # filtered_result = filter(lambda x: x is not None, result)
    # took = time.time()-start
    # # eval_time(strategy, took, random_samples, result, filtered_result)
    # thiswalk.append([strategy, "%s/%s" % (len(filtered_result), len(result)), took])

