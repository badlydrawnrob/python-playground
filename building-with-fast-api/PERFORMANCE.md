# Performance

> ✅ SQLite excels at high reads, low writes.<br>
> ⚠️ Sustained high concurrent writes are a big problem!

**SQLite is great for concurrent reads; sustained concurrent writes at scale has some big problems.** When you're nearing `-c 30` back-to-back writes, you may want to consider [other options](#-performance-upgrades). One option is using a database for inserts, then backing up and syncing changes to a separate read-only database.

If you have two design routes with similar results, always prefer the simplest, most consistent, easiest-to-read version!


## 🙋‍♀️ Do you have customers yet?

> ⚠️ Don't optimise too early and keep concurrency reasonable.

You don't? Well then, worry about it when you're getting `-c 30` concurrent connections!

Consider first 3rd-party tools like [Tally](https://tally.so) and [n8n](https://tally.so/help/n8n-integration) for prototyping and perform bulk writes (automatically or manually); your database could be read-only for the most part.


## Testing results

> **⏱ Timeouts only required when more than 10 concurrent writers.**

| Command         | Result |
| --------------- | ------ |
| `-c 10`         | 100% success |
| `-c 10 -t 5s`   | 99.9% success |
| `-c 75 -t 5s`   | 95% success |
| `-c 100 -t 10s` | 99% failure (with WAL mode) |
| `-c 100 -t 10s` | 99% success (without WAL mode) |

**A small atomic POST query on a single endpoint: not a fully fledged API load test!** It's a fine balance to get all parts working well with `aiosqlite`.

1. **SQLite is great for high concurrent reads!**
2. **SQLite writes one at a time and is blocking**
    - If a write is currently active, reads must wait (a problem at scale)
    - `WAL` mode helps unblock writes (with less than `-c 75`) but ...
    - `WAL` mode at scale (`-c 100`) can make success rates a lot worse!
3. SQLite struggles with sustained high concurrent writes (over `75`)
    - Higher concurrency generally requires a bigger timeout
    - Beware of concurrency over `-c 75` and `-t 10s`
        - It can start to become volatile and inconsistent
        - Failures happen between 50% to 90% at that scale (depending on setup)
4. **Bombardier with 2 commands running** (one of which back-to-back writes) ...
    - Both commands start running very slowly; further load testing is needed!
5. **Both client and server _must_ use `timeout=`s at scale, or writes fail badly**
    - Timeouts should be set on Bombardier requests, FastAPI, and SQLiteEngine!
    - Over 10 seconds gets diminishing returns and failures (keep all timeouts same)
6. Using more efficient queries will help a little bit
    - For example, insert with user `id` directly (instead of `authenticate()`)
7. **Exceptions are NOT reliably caught** (basically do nothing, e.g: `sqlite3.OperationalError`)
    - We cannot `try`/`except` to cancel the query and ask client to retry
    - Safer to just raise the timeout or potentially rollback a transaction
    - **Inserts can still happen, even if `5xx` and `other` errors are returned**
8. Postgres defaults to 100 concurrent connections (more can harm performance)


## 👆 Performance upgrades

> ⏱ It's generally a good sign if you've reached a point where concurrency and traffic is becoming a problem. You've got customers! It could be a good time to hire!

[Turso](https://github.com/tursodatabase/turso) is coming and might be a drop-in replacement.

1. Check where bottlenecks are and calculate the risk
2. Hire a network professional or outsource the problem
3. SQLite [Remote copy](https://sqlite.org/rsync.html) to create a read-only file
4. FastAPI [queue handling](https://fastapi.tiangolo.com/tutorial/background-tasks/#caveat)
5. Postgres using a connection pool (max 100 concurrent writes)

See also [when to use SQLite](https://sqlite.org/whentouse.html). Solutions when high load becomes a problem include [Litestream](https://litestream.io/how-it-works/) (backup and treat one database as read-only), [queuing](https://codeandcortex.medium.com/the-surprising-way-i-used-sqlite-to-scale-a-side-project-to-100k-users-1295dccf1212), or other 3rd-party tools ([LiteFS](https://fly.io/docs/litefs/), [Forq](https://forq.sh), [Cloudflare](https://www.cloudflare.com/en-gb/application-services/products/waiting-room/), [Queue It](https://www.queue-it.com)). More [unusual ways](https://www.reddit.com/r/programming/comments/gpibz8/scaling_sqlite_to_4m_qps_on_a_single_server_ec2/) with your own server setup have been done before.


## ⛔️ Timeout and broken pipe

> Timeouts occur because either the client or the server timeout is too little.

Timeouts have diminishing returns and more failures `> 10s`.

SQLite `sqlite3.connect()` takes a timeout (in seconds) and you must assure that all network connections that require a timeout have one set. SQLite does not guarantee the order of insertion, so expect query log numbers to be out of sync (out of order).


## Catching and throwing `Exception`s

It's best wherever possible to avoid throwing an `Exception`. Some say exceptions should be [exceptional](https://dev.to/jpswade/exceptions-are-meant-to-be-exceptional-4e3l) and to refactor your code to avoid them, before trying to catch them. Is the exception happening [more than 1/8th](https://stackoverflow.com/questions/8107695/python-faq-how-fast-are-exceptions) of the time?

They can also be time expensive when thrown, but if they're thrown _anyway_ (for example `sqlite3.OperationalError`, it doesn't hurt to catch it and return a helpful error code to the end user.

A shorthand is `value | Exception`, but you'll probably want to throw different status codes as all exceptions aren't alike. Python's [`match`](https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/) [doesn't work](https://discuss.python.org/t/python-3-10-match-case-syntax-for-catching-exceptions/11076/22)** as I expected, so you can't quite `case` with branch error types like Elm.


## Is Async faster than Sync?

> Async over a network is 2x faster running `125` concurrent `GET` connections.[^1]

For an example, the max read time for concurrent synchronous `/event/` endpoint was `10.03s`! An (old) [source](https://stackoverflow.com/questions/39803746/peewee-and-peewee-async-why-is-async-slower) seems to say the opposite (faster reads with sync), which might be the case for single requests without concurrency. Max req/sec can be higher with sync concurrency, but all other metrics and throughput are worse, even with `-c 10` connections. Piccolo logs get a bit screwy using synchronous with high concurrency.

A basic test running SQLite in WAL mode with `run_sync()` is also very poor (dog slow) — the _opposite_ of what should happen! Writes almost certainly need async or WAL mode. These tests may differ from ORM-only (without a network).


[^1]: For a single-user application synchronous mode is probably fine. 
