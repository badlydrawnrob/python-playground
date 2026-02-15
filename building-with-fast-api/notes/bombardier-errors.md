
# BUGS

## Commands

```
bombardier -c 125 -n 10000 -H \
"Authorization: Bearer [GENERATE JWT WITH BRUNO]" \
-H 'accept: application/json' -H 'content-type: application/json' --method=POST \
-b '{"creator": null,"title": "Pyramid Stage","image": "https://tinyurl.com/ed-sheeran-with-shakira","description": "Ed Sheeran sings with Shakira at Glastonbury!","location": "Glastonbury","tags": ["music","adults","event"]}' \
http://localhost:8000/event/new
```

```
curl --request POST \
  --url http://localhost:8000/event/new \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'authorization: Bearer [GENERATE JWT WITH BRUNO]' \
  --data '{"creator": null,"title": "Pyramid Stage","image": "https://tinyurl.com/ed-sheeran-with-shakira","description": "Ed Sheeran sings with Shakira at Glastonbury!","location": "Glastonbury","tags": ["music","adults","event"]}'
```


## Alternative JWT `sub` with default `timeout`.

```
Bombarding http://localhost:8000/event/new with 10000 request(s) using 125 connection(s)
 10000 / 10000 [==========================================] 100.00% 139/s 1m11s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       140.00     104.77    4110.76
  Latency         0.88s   804.49ms      2.07s
  HTTP codes:
    1xx - 0, 2xx - 6097, 3xx - 0, 4xx - 0, 5xx - 0
    others - 3903
  Errors:
       timeout - 3903
  Throughput:    98.30KB/s
```

### With the `timeout` set

With `timeout` set it seems Bombardier doesn't fully complete (or more errors)
However, SQLite says it has `6000`+ rows when Bombardier reads:

1xx - 0, 2xx - 3392, 3xx - 0, 4xx - 0, 5xx - 1845
    others - 4763


## Default `timeout`

```
Query 29815 response:
[{'creator': 1,
  'description': 'Ed Sheeran sings with Shakira at Glastonbury!',
  'id': UUID('f929d652-7ec2-4f1a-af03-7717b5822a23'),
  'image': 'https://tinyurl.com/ed-sheeran-with-shakira',
  'location': 'Glastonbury',
  'tags': ['music', 'adults', 'event'],
  'title': 'Pyramid Stage'}]
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 416, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1135, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/applications.py", line 107, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/middleware/cors.py", line 85, in __call__
    await self.app(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/routing.py", line 736, in app
    await route.handle(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 115, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 101, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 355, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 243, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/chapter_08/planner/routes/events.py", line 217, in create_event
    query = await (
            ^^^^^^^
    ...<4 lines>...
    )
    ^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/piccolo/query/base.py", line 193, in run
    return await self._run(node=node, in_pool=in_pool)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/piccolo/query/base.py", line 175, in _run
    results = await engine.run_querystring(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        querystrings[0], in_pool=in_pool
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/piccolo/engine/sqlite.py", line 795, in run_querystring
    response = await self._run_in_new_connection(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
    )
    ^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/piccolo/engine/sqlite.py", line 728, in _run_in_new_connection
    async with connection.execute(query, args) as cursor:
               ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/aiosqlite/context.py", line 41, in __aenter__
    self._obj = await self._coro
                ^^^^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/aiosqlite/core.py", line 223, in execute
    cursor = await self._execute(self._conn.execute, sql, parameters)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/aiosqlite/core.py", line 160, in _execute
    return await future
           ^^^^^^^^^^^^
  File "/Users/rob/Sites/GitHub/python-playground/building-with-fast-api/.venv/lib/python3.13/site-packages/aiosqlite/core.py", line 63, in _connection_worker_thread
    result = function()
sqlite3.OperationalError: database is locked

Query 29663 response:
[{'creator': 1,
  'description': 'Ed Sheeran sings with Shakira at Glastonbury!',
  'id': UUID('d69eae93-3142-4483-ab25-5593a9a31c9d'),
  'image': 'https://tinyurl.com/ed-sheeran-with-shakira',
  'location': 'Glastonbury',
  'tags': ['music', 'adults', 'event'],
  'title': 'Pyramid Stage'}]

Query 29791 response:
[{'creator': 1,
  'description': 'Ed Sheeran sings with Shakira at Glastonbury!',
  'id': UUID('b1822ccf-9c49-48db-95d0-59f96564d3bb'),
  'image': 'https://tinyurl.com/ed-sheeran-with-shakira',
  'location': 'Glastonbury',
  'tags': ['music', 'adults', 'event'],
  'title': 'Pyramid Stage'}]

Query 29950 response:
[{'creator': 1,
  'description': 'Ed Sheeran sings with Shakira at Glastonbury!',
  'id': UUID('3dbb24b5-6028-4430-b852-473e21df6e48'),
  'image': 'https://tinyurl.com/ed-sheeran-with-shakira',
  'location': 'Glastonbury',
  'tags': ['music', 'adults', 'event'],
  'title': 'Pyramid Stage'}]

Query 29844 response:
[{'creator': 1,
  'description': 'Ed Sheeran sings with Shakira at Glastonbury!',
  'id': UUID('f418d057-5917-47ee-9521-9773afc3e430'),
  'image': 'https://tinyurl.com/ed-sheeran-with-shakira',
  'location': 'Glastonbury',
  'tags': ['music', 'adults', 'event'],
  'title': 'Pyramid Stage'}]

Query 29958 response:
[{'creator': 1,
  'description': 'Ed Sheeran sings with Shakira at Glastonbury!',
  'id': UUID('da07fced-13ba-4fec-94ed-e63e29b65bd2'),
  'image': 'https://tinyurl.com/ed-sheeran-with-shakira',
  'location': 'Glastonbury',
  'tags': ['music', 'adults', 'event'],
  'title': 'Pyramid Stage'}]
```


## `timeout=60`

### Attempt 1

```
rob@Robs-MacBook-Pro ~ % bombardier -c 125 -n 10000 -H \
"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb3ZlbHlidW0iLCJleHAiOjE3NzA2NzY2NTcuMDk5NTA5fQ.iZb17UnN_W9n8p2vslEZv8NNGyrhtedv7NnDGK4edYI" \
-H 'accept: application/json' -H 'content-type: application/json' --method=POST \
-b '{"creator": null,"title": "Pyramid Stage","image": "https://tinyurl.com/ed-sheeran-with-shakira","description": "Ed Sheeran sings with Shakira at Glastonbury!","location": "Glastonbury","tags": ["music","adults","event"]}' \
http://localhost:8000/event/new
```

```
Bombarding http://localhost:8000/event/new with 10000 request(s) using 125 connection(s)
 10000 / 10000 [===========================================] 100.00% 96/s 1m43s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       103.00     136.16    4083.49
  Latency         1.28s      0.88s      4.01s
  HTTP codes:
    1xx - 0, 2xx - 2390, 3xx - 0, 4xx - 0, 5xx - 1097
    others - 6513
  Errors:
       timeout - 4896
    the server closed connection before returning the first response byte. Make sure the server returns 'Connection: close' response header before closing the connection - 1032
    dial tcp 127.0.0.1:8000: connect: connection reset by peer - 326
    dial tcp 127.0.0.1:8000: i/o timeout - 238
    write tcp 127.0.0.1:60723->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59592->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:58752->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59017->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:60561->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:62438->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:62474->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:62486->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:58539->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:58732->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59502->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:60070->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:60325->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:60330->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59898->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59850->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:58714->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:58903->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:58934->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59101->127.0.0.1:8000: write: broken pipe - 1
    write tcp 127.0.0.1:59089->127.0.0.1:8000: write: broken pipe - 1
  Throughput:    56.77KB/s
```

### Attempt 2 (with `PRAGMA journal_mode=WAL`)

```
Bombarding http://localhost:8000/event/new with 10000 request(s) using 125 connection(s)
 10000 / 10000 [============================================] 100.00% 309/s 32s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       319.05    1076.76   21542.65
  Latency      382.21ms   624.08ms      2.03s
  HTTP codes:
    1xx - 0, 2xx - 2475, 3xx - 0, 4xx - 0, 5xx - 340
    others - 7185
  Errors:
    the server closed connection before returning the first response byte. Make sure the server returns 'Connection: close' response header before closing the connection - 5686
       timeout - 1499
  Throughput:   188.47KB/s
```


## `timeout=200`

```
rob@Robs-MacBook-Pro ~ % bombardier -c 125 -n 10000 -H \
"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb3ZlbHlidW0iLCJleHAiOjE3NzA2NzY2NTcuMDk5NTA5fQ.iZb17UnN_W9n8p2vslEZv8NNGyrhtedv7NnDGK4edYI" \
-H 'accept: application/json' -H 'content-type: application/json' --method=POST \
-b '{"creator": null,"title": "Pyramid Stage","image": "https://tinyurl.com/ed-sheeran-with-shakira","description": "Ed Sheeran sings with Shakira at Glastonbury!","location": "Glastonbury","tags": ["music","adults","event"]}' \
http://localhost:8000/event/new
Bombarding http://localhost:8000/event/new with 10000 request(s) using 125 connection(s)
 10000 / 10000 [==========================================] 100.00% 131/s 1m15s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       135.11     123.61    4488.67
  Latency         0.93s   746.63ms      3.14s
  HTTP codes:
    1xx - 0, 2xx - 2730, 3xx - 0, 4xx - 0, 5xx - 2117
    others - 5153
  Errors:
       timeout - 3061
    the server closed connection before returning the first response byte. Make sure the server returns 'Connection: close' response header before closing the connection - 2084
    dial tcp 127.0.0.1:8000: connect: connection reset by peer - 7
    write tcp 127.0.0.1:52555->127.0.0.1:8000: write: broken pipe - 1
  Throughput:    85.17KB/s
```


### Resetting the `.db` then `timeout=200`

```
Bombarding http://localhost:8000/event/new with 10000 request(s) using 125 connection(s)
 10000 / 10000 [==========================================] 100.00% 140/s 1m11s
Done!
Statistics        Avg      Stdev        Max
  Reqs/sec       141.74     134.82    5094.90
  Latency         0.88s   740.19ms      2.02s
  HTTP codes:
    1xx - 0, 2xx - 3392, 3xx - 0, 4xx - 0, 5xx - 1845
    others - 4763
  Errors:
       timeout - 3016
    the server closed connection before returning the first response byte. Make sure the server returns 'Connection: close' response header before closing the connection - 1747
```
