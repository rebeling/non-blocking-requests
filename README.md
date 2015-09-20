# Non-blocking-requests


This project validates non-blocking / async requests for performance.

Initial problem was: we switched in a project from tornado to flask - for
the sake of simplicity - and later in time the client ask for special
behavior: we need to call an elasticsearch with information from
the search result before. For 20 search result items it meant  20 extra requests - before the final result could be responded.

Getting rid of tornado kind of closed the option for async httpclient
requests. We can still use it, but I was interested in what else use
of non-blocking strategies is out there and what about the  performances.


## Test setup:

1. create an elasticsearch index

  * number\_of\_shards 5

  * with one million documents (see create_index.py)

  * document consist of two fields title, content filled wiht loremipsum

2. request the elasticsearch in non-blocking fashion

  * use different tasks: asyncio, grequests, requests-futures, ... and tornado (see requests_test.py and task/)
  * get the strings from documents content field

  * time it and evaluate


## On the way

### Blasting fast locally

Interesting observation is the serial time running it loacally. The bottleneck
for sure is the internet connection: open, call, close again and again.
But with a local setup, even the serial approach compared to the async methods
is not as slow as expected.

Requests-futures 1000 > thread.error: can't start new thread

### The other side of the table

Elasticsearch ... number of shards performance measures
... extrem fast response. Spawn to shards initially  is pretty handy.

### Loosing data

It seems to be to fast sometimes or to many jobs in parallel and if not
finished happened in ThreadPoolExecutor bulk indexing the data with 20 max_workers. 800000 in 80s
Reduced to 10 989.999 in (Finished in 91.8s). But with 5 it creted the million.
Changed to mp Pool result was Pool(processes=80)  230.000 (230.000) docs after 43.4s
 20 589.999 69.2s]

speed up the bulk indexing refresh_interval" : -1,
and when done a
POST /requests-testing/_optimize?max_num_segments=5

[Finished in 65.0s]


turn of refresh interval
20 workers
[Finished in 74.4s] super fast but 989.999 (989.999) missing 10.000 ...done

turn of refresh interval
10 workers
Finished in between 69.7s - 78.5s  ...worked. Know how much data you expect
with same result.

## Results

Fastest:


| Tasks | Seria | Grequ | ReqFu | cfThr | mpPoo | Async | Torna |
|:---|---:|---:|---:|---:|---:|---:|---:|
| 1     | 0.019 | 0.004 | 0.001 | 0.010 | 0.029 | 0.006 | 0.008 |
| 20    | 0.086 | 0.053 | 0.037 | 0.113 | 0.194 | 0.083 | 0.034 |
| 50    | 0.217 | 0.127 | 0.144 | 0.183 | 0.083 | 0.180 | 0.093 |
| 100   | 0.489 | 0.277 | 0.313 | 0.380 | 0.162 | 0.382 | 0.234 |
| 500   | 2.393 | 1.473 | 1.692 | 2.258 | 0.818 | 2.188 | 0.922 |
| 1000  | 3.938 | 2.865 |  -    | 3.695 | 1.685 | 4.354 | 2.082 |




---------------------------------------

## Sources:


[1] [Asynchronous Servers in Python](http://nichol.as/asynchronous-servers-in-python)

[2] [Feature comparison of Python non-blocking I/O libraries](http://ptspts.blogspot.de/2010/05/feature-comparison-of-python-non.html)

[3] [Tulip – Python async I/O with coroutines](http://codetrips.com/2014/01/24/tulip-python-async-io-with-coroutines)
