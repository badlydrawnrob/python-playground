# Bombardier

> ⏱ Examples give rough idea of speed and concurrency ...
> ❌ `sqlite3.OperationalError: database is locked` is going to be a problem!

This is a test in theory, but not always in practice. Running the same bombardier call can differ in it's results; bombardier with `-c 125` and `-n 10000000` (as in docs) takes a _really_ long time and it's unlikely a startup prototype will need more than `10` concurrent connections.

Given two design routes with similar results, prefer the simplest, most consistent, easiest-to-read version!


## TL;DR

> Don't optimise too early and keep concurrency reasonable.
> Migrate data to Postgres or Turso if the server errors too often.

Writes are the big problem as they can block reads.

1. **Do you have enough customers to worry about concurrency?**
2. No? Then try to never go over `-c 30` concurrent connections!
3. You can't handle `Exception`s within the endpoint (Bombardier ignores them)
4. If you've reached the point where concurrency and traffic is getting high:
    - Check where the bottlenecks are and calculate the risk
    - Hire a network professional or outsource the problem
    - Use a connection pool with Postgres
5. Other options for handling load:
    - SQLite-specific like [Forq](https://forq.sh)
    - Use a [queue handler](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat) to fix the problem
    - 3rd party service like [Cloudflare](https://www.cloudflare.com/en-gb/application-services/products/waiting-room/) or [Queue It](https://www.queue-it.com)


## To do

> Bombardier can only run one endpoint at a time.
> You can run two Bombardier commands in different terminals.

What's the max capacity for SQLite?

1. Write endpoints are blocking. Read endpoints are not.
2. Running two Bombardier commands (one write, one read) is VERY slow (15mins+).
    - `bombardier -c 10 -n 5000 http://localhost:8000/event/`
    - `bombardier -c 10 -n 5000` with `http://localhost:8000/event/new` POST
3. Test with [Locust](https://locust.io/) for concurrency with same [scenarios](https://github.com/coding-yogi/bombardier)
    - How many users can it handle?


## Is Async faster than Sync?

> Async over a network is about twice as fast when using `125` concurrent `GET` connections.

For an example, the max read time for concurrent synchronous `/event/` endpoint was `10.03s`! An (old) [source](https://stackoverflow.com/questions/39803746/peewee-and-peewee-async-why-is-async-slower) seems to say the opposite (faster reads with sync), which might be the case for single requests without concurrency. Max req/sec can be higher with sync concurrency, but all other metrics and throughput are worse, even with `-c 10` connections. Piccolo logs get a bit screwy using synchronous with high concurrency.

A basic test running SQLite in WAL mode with `run_sync()` is also very poor (dog slow) — the _opposite_ of what should happen! Writes almost certainly need async or WAL mode. These tests may differ from ORM-only (without a network).


## `/event/new`

> TL;DR: high concurrent connections with lots of traffic is very unpredictable (`-c 125`). 
> It fails A LOT at that scale. Depending on circumstances 50%-95% failure rate!

**✅ Concurrent connections of `-c 10`—`-c 30` gets around 99% success (resolves issue).** After that, best case scenario is 50% success with a bunch of "other: timeout" errors that I can't figure out how to properly handle (and send failure back to the client). There's a very slight improvement inserting with an `id` directly, rather than using the `authenticate()` function to get it.

- **⛔️ Exceptions are NOT caught** with a `try/except` block
    - I've tried `sqlite3.OperationalError` (database locked)
    - I've tried `Exception` master type (still no joy)
- **⛔️ Timeouts seem unavoidable at scale**
    - The most reliable error is `ERROR: Exception in ASGI application` with a long stack trace `sqlite3.OperationalError: database is locked`
    - My _hunch_ is that FastAPI returns the timeout error (not Piccolo)
    - I can't find a way to handle it properly and return a `4xx` failure.
- **⛔️ Insertion order is not guaranteed** with SQLite when database locked
    - Piccolo query logs stop working properly after a while too
- **⛔️ SQLite `timeout=` setting has proved unsuccsessful in tests**
    - Drops performance from 50% success (`-c 125`) to 80%+ failure
- **⛔️ Timeouts do not stop some inserts from happening!**
    - E.g: `2xx - 5901` and error `others - 4099` but `6524` rows created.
- Other errors that happen at scale:
    - At my local library connected to open wifi many `5xx` errors
    - At home (and my local library)
        - "the server closed connection before returning the first response byte. Make sure the server returns 'Connection: close' response header before closing the connection"
        - dial tcp 127.0.0.1:8000: connect: connection reset by peer - 326
        - write tcp 127.0.0.1:60723->127.0.0.1:8000: write: broken pipe
    - When trying two Bombardier commands at the same time
        - dial tcp 127.0.0.1:8000: i/o timeout
        - dial tcp 127.0.0.1:8000: connect: connection reset by peer


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
