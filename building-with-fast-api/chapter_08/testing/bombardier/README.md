# Bombardier

> ⏱ Examples give rough idea of speed and concurrency ...
> ❌ `sqlite3.OperationalError: database is locked` is going to be a problem!

This is a test in theory, but not always in practice. Running the same bombardier call can differ in it's results; bombardier with `-c 125` and `-n 10000000` (as in docs) takes a _really_ long time and it's unlikely a startup prototype will need more than `10` concurrent connections.

1. Do you have enough customers to worry about concurrency?
2. How likely is it that your endpoint will have bulk concurrent hits?
3. Which areas of your application are significant bottlenecks?
4. At what stage is it worth considering performance optimizations?

Given two design routes with similar results, prefer the simplest, most consistent, easiest-to-read version!


## To do

> Bombardier command is not designed to hit more than one endpoint at a time.
> 2 terminals hitting different endpoints with `-c 10` and `-n 10000` runs very, very, slow.

You may need to try [scenarios](https://github.com/coding-yogi/bombardier) or [Locust](https://locust.io/) instead.

1. Run multiple bombardier commands at the same time.
2. What's the max capacity when running different users?
3. What's the max capacity for traffic hitting different endpoints?


## Is Async faster than Sync?

> Async is about twice as fast when using `125` concurrent `GET` connections.

For an example, the max read time for concurrent synchronous `/event/` endpoint (`-c 125`) was `10.03s`! An (old) [source](https://stackoverflow.com/questions/39803746/peewee-and-peewee-async-why-is-async-slower) seems say the opposite (faster reads with sync), which might be the case for single requests without concurrency. Max req/sec can be higher with sync concurrency, but all other metrics and throughput are worse, even with `-c 10` connections. Writes almost certainly need async or WAL mode.

Piccolo logs get a bit screwy using synchronous with high concurrency.


## `/event/new`

> There's a moderate improvement if you use `id` directly in the SQL (rather than fetching `authenticate()`), but not a whole lot.

`sqlite3.OperationalError: database is locked` error but recovered with 50% success rate. Insertion order is not guaranteed and Piccolo query logs stop working properly after a while.

**Changing to `-c 10` connections almost resolves the problem (99% success).**

```text
Bombarding http://localhost:8000/event/new with 10000 request(s) using 125 connection(s)
 10000 / 10000 [==========================================] 100.00% 119/s 1m23s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       120.27     110.36    5143.13
  Latency         1.03s   777.08ms      2.10s
  HTTP codes:
    1xx - 0, 2xx - 5531, 3xx - 0, 4xx - 0, 5xx - 0
    others - 4469
  Errors:
       timeout - 4469
  Throughput:    83.73KB/s
```

With `timeout=` set (even to `300`) the first few 1000 return `200` status code but then problems start with Bombardier broken pipe or closed connection errors, even though rows are still being added.


## `/event/`

### Each branch using full query

> Speed difference is negligible between partial query and full query in branches.
> Stored query has more consistent results; full queries in each branch more Req/sec.

Tests below store `query = data.Event.select()` then extend it in each branch.

#### Round 1

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

#### Round 2

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


## `/event/?q=location`

**⚠️ PATH MUST BE EXACT (`/event?q=location` won't work)**

### Each branch running it's own full query

#### Round 1

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

#### Round 2

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

### Stored query which is extended in each branch

#### Round 1

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

#### Round 2

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
