# Performance

> ⚠️ Sustained high concurrent writes are a big problem

Given two design routes with similar results, prefer the simplest, most consistent, easiest-to-read version! Consider also using Tally forms and bulk writes, to assure all reads happen correctly.

- Async SQLite is more than 50% faster handling multiple connections[^1]
- If you've got heavy writes, reads will get blocked by default
    - Using two Bombardier commands at the same time is slow as hell
    - Using [`WAL` mode](https://sqlite.org/wal.html) should help a little
    - Go to  SQLite repl and enter `PRAGMA journal_mode=WAL`
- `Exception` when handled does not raise a `400` (or rarely does)
    - Endpoints with `try`/`except` blocks seem to get ignored
    - Both `Exception` and `sqlite3.OperationalError` don't get catched


## 🙋‍♀️ Do you have customers yet?

> ⚠️ Don't optimise too early and keep concurrency reasonable.

No? Worry about it when you've got more than `-c 30` concurrent connections!


## 👆 Performance upgrades

> ⏱ If you've reached the point where concurrency and traffic is getting high ...

1. Check where bottlenecks are and calculate the risk
2. Hire a network professional or outsource the problem
3. SQLite plugin like [Litestream](https://litestream.io/how-it-works/) or [queue handler](https://codeandcortex.medium.com/the-surprising-way-i-used-sqlite-to-scale-a-side-project-to-100k-users-1295dccf1212)
4. SQLite [Remote copy](https://sqlite.org/rsync.html) or [LiteFS](https://fly.io/docs/litefs/) for 2nd read-only database
5. Postgres using a connection pool (max 100 concurrent writes)

### Other options for handling load

- FastAPI [queue handling](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat)
- [Remote copy](https://sqlite.org/rsync.html) for 2nd read-only database
- SQLite-specific like [Forq](https://forq.sh)
- 3rd party service like [Cloudflare](https://www.cloudflare.com/en-gb/application-services/products/waiting-room/) or [Queue It](https://www.queue-it.com)
- More [unusual ways](https://www.reddit.com/r/programming/comments/gpibz8/scaling_sqlite_to_4m_qps_on_a_single_server_ec2/) to scale with SQLite (requires a good server, also on Y Combinator)


## ⛔️ Timeout and broken pipe

> `timeout=1000` does not help in the way you'd expect!

SQLite `sqlite3.connect()` takes a timeout (in seconds). I'm not sure if this is a FastAPI, Piccolo, or SQLite problem. In tests `2xx` responses go _down_ in success rates, not up.

SQLite does not guarantee the order of insertion, so expect query log numbers to be out of sync (out of order).


## Catching and throwing `Exception`s

It's best wherever possible to avoid throwing an `Exception`. Some say exceptions should be [exceptional](https://dev.to/jpswade/exceptions-are-meant-to-be-exceptional-4e3l) and to refactor your code to avoid them, before trying to catch them. Is the exception happening [more than 1/8th](https://stackoverflow.com/questions/8107695/python-faq-how-fast-are-exceptions) of the time?

They can also be time expensive when thrown, but if they're thrown _anyway_ (for example `sqlite3.OperationalError`, it doesn't hurt to catch it and return a helpful error code to the end user.

A shorthand is `value | Exception`, but you'll probably want to throw different status codes as all exceptions aren't alike. Python's [`match`](https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/) [doesn't work](https://discuss.python.org/t/python-3-10-match-case-syntax-for-catching-exceptions/11076/22)** as I expected, so you can't quite `case` with branch error types like Elm.


## Is Async faster than Sync?

> Async over a network is 2x faster running `125` concurrent `GET` connections.

For an example, the max read time for concurrent synchronous `/event/` endpoint was `10.03s`! An (old) [source](https://stackoverflow.com/questions/39803746/peewee-and-peewee-async-why-is-async-slower) seems to say the opposite (faster reads with sync), which might be the case for single requests without concurrency. Max req/sec can be higher with sync concurrency, but all other metrics and throughput are worse, even with `-c 10` connections. Piccolo logs get a bit screwy using synchronous with high concurrency.

A basic test running SQLite in WAL mode with `run_sync()` is also very poor (dog slow) — the _opposite_ of what should happen! Writes almost certainly need async or WAL mode. These tests may differ from ORM-only (without a network).


[^1]: For a single-user application synchronous mode is probably fine. 