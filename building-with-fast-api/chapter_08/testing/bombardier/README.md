# Bombardier

> ⏱ Examples give rough idea of speed and concurrency ...
> ❌ `sqlite3.OperationalError: database is locked` is a big problem at scale!

This is a test in theory, but not always in practice. Running the same bombardier call can differ in it's results; bombardier with `-c 125` and `-n 10000000` (as in docs) takes a _really_ long time and it's unlikely a startup prototype will need more than `10` concurrent connections.

Bombardier can only run one endpoint at a time, but you can run two Bombardier commands in different terminals.


## TL;DR

> **Don't optimise too early** and keep concurrency reasonable.

1. **See scaling SQLite in [performance](../../../PERFORMANCE.md) doc**
    - Start scaling with a `timeout=` for FastAPI, SQLiteEngine, and Bombardier.
2. Exceptions seem to be difficult to handle (such as database is locked)
3. Sometimes failures are higher than other times (with same request)
    - E.g: home -vs- library when it shouldn't make a difference!
4. Migrate data to Postgres or Turso if the server errors too often.


## `/event/new`

> TL;DR: high concurrent connections with lots of traffic is very unpredictable (`-c 125`) without all timeouts set. After 100 concurrency expect it to fail A LOT (like 50%-95%).

1. When `timeout=` _is_ set you get ~99% success with up to `-c 100` connections
2. When `timeout=` _is not_ you get ~99% success with `-c 30` connections and less only

Bombarding your endpoint with back to back writes will fuck up your reads and run very slowly. Enabling `WAL` mode with very high concurrency (`-c 100`) can result in _worse_ results and more errors. See [`PERFORMANCE.md`](../../../PERFORMANCE.md) for more info.

Here's an example with no `timeout=` and 125 concurrent connections.

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

A list of potential errors, depending on setup:

- **⛔️ Exceptions are NOT caught** with a `try/except` block
    - I've tried `sqlite3.OperationalError` (database locked)
    - I've tried `Exception` master type (still no joy)
- **⛔️ Timeouts seem unavoidable at scale**
    - The most reliable error is `ERROR: Exception in ASGI application` with a long stack trace `sqlite3.OperationalError: database is locked`
    - My _hunch_ is that FastAPI returns the timeout error (not Piccolo)
    - I can't find a way to reliably handle it and return a `4xx` failure.
- **⛔️ Insertion order is not guaranteed** with SQLite when database locked
    - Piccolo query logs stop working properly after a while too
- **⛔️ SQLite database locked or API timeout is unavoidable if ...**
    - More than `timeout=60` (make sure to set all timeouts)
    - Concurrency of `-c 101` or more (50% and more failure)
- **⛔️ Inserts can still happen even if database locked or timeout errors!**
    - E.g: `2xx - 5901` and error `others - 4099` but `6524` rows created.
- Other errors that happen at scale:
    - At my local library connected to open wifi many `5xx` errors
        - `sqlite3.OperationalError: unable to open database file`
    - At home (and my local library)
        - "the server closed connection before returning the first response byte. Make sure the server returns 'Connection: close' response header before closing the connection"
        - dial tcp 127.0.0.1:8000: connect: connection reset by peer - 326
        - write tcp 127.0.0.1:60723->127.0.0.1:8000: write: broken pipe
    - When trying two Bombardier commands at the same time
        - dial tcp 127.0.0.1:8000: i/o timeout
        - dial tcp 127.0.0.1:8000: connect: connection reset by peer


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
