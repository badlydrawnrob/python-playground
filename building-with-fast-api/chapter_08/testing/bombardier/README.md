# Bombardier

> ⏱ This gives a rough idea of speed and concurrency ...

But running bombardier a few times can have quite different results; running `-c 125` and `-n 10000000` (as in docs) takes a _really_ long time and is very unlikely for a startup prototype. Also worth considering is how likely your endpoint will have concurrent (or bulk) hits: this is a test in theory, but not always in practice.

If results are similar for different setups, prefer the simplest, most consistent, easiest-to-read version.


## `/event/`

### Each branch using full query

> Writing the full SQL statement in each branch

Round 1

```text
Bombarding http://localhost:8000/event/ with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 275/s 36s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       277.24     225.03    1808.60
  Latency      452.03ms    88.78ms      2.52s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   256.33KB/s
```

Round 2

```text
Bombarding http://localhost:8000/event/ with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 255/s 39s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       257.48     244.90    2080.82
  Latency      486.53ms   123.21ms      2.76s
  HTTP codes:
    1xx - 0, 2xx - 9961, 3xx - 0, 4xx - 0, 5xx - 39
    others - 0
  Throughput:   237.58KB/s
```

### Each branch using stored query

> Stored `query = data.Event.select()` then extend in each branch

Round 1

```text
Bombarding http://localhost:8000/event/ with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 268/s 37s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       269.91     216.61    1615.12
  Latency      463.63ms    86.03ms      1.96s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   249.94KB/s
```

Round 2

```text
Bombarding http://localhost:8000/event/ with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 266/s 37s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       269.01     241.61    1865.82
  Latency      465.73ms    87.34ms      1.97s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   248.87KB/s
```


## `/event?=location`

### Each branch using full query

Round 1

```text
Bombarding http://localhost:8000/event/?q=location with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 266/s 37s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       268.88     224.54    1628.10
  Latency      465.94ms    85.24ms      1.90s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   251.62KB/s
```

Round 2

```text
Bombarding http://localhost:8000/event/?q=location with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 230/s 43s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       232.99     224.64    1795.33
  Latency      538.08ms   248.61ms      5.35s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   217.83KB/s
```

### Each branch using stored query

Round 1

```text
Bombarding http://localhost:8000/event/?q=location with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 259/s 38s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       260.48     244.29    2102.43
  Latency      480.52ms   101.58ms      2.00s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   244.00KB/s
```

Round 2

```text
Bombarding http://localhost:8000/event/?q=location with 10000 request(s) using 125 connection(s)
 10000 / 10000 [=============================================] 100.00% 258/s 38s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       261.28     225.03    2703.96
  Latency      480.36ms    73.02ms      1.84s
  HTTP codes:
    1xx - 0, 2xx - 10000, 3xx - 0, 4xx - 0, 5xx - 0
    others - 0
  Throughput:   243.89KB/s
```
