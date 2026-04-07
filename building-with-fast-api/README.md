# README

> **Building with Fast API book** (with extras)
> I've used my personal [coding style](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style) in this repo and the book has errors I've tried to fix.

**App architecture and APIs have an _insane_ amount to think about;** take it slowly and build incrementally. A FastAPI quick [reference book](https://www.oreilly.com/library/view/fastapi/9781098135492/) will help; I find it's documentation style hard to read. Coding is a massive timesink, but (in my opinion) 3rd-party tools give you less control over data, and Ai-gen is best used with popular languages and tools, where context and documentation is properly set up. Ai brain rot is a serious problem! Here's my current approach:

- Learn the basics well (data structures are important)
- API by hand with [paper prototyping](https://www.sciencedirect.com/book/monograph/9781558608702/paper-prototyping) (frontend with [tooling](https://www.pencil.dev))
- Focus on sales to quickly validate an idea (you can rebuild later)
- Cherry-pick learning and confidently code (just-in-time)

**It takes a considerable amount of time to switch ORMs.** Is the alternative 10x faster/better?[^1] It isn't? So learn one well and stick with it! Alternatively, ditch the ORM and [just use data](https://gist.github.com/reborg/dc8b0c96c397a56668905e2767fd697f#should-i-use-a-namespace-to-bundle-functions-to-model-a-domain-object-like-a-customer-or-product).




## 🧞 A wishlist never ends!

> At some point you've just got to 🚢 ship it!

**Learning is never-ending:** there's always some new feature or bug to squash! Your job is to stick with one idea long enough to validate it, but don't prematurely optimise. Be brutal. Cut code down. Release!

1. **🐌 Queries with a few hundred rows run really slow (2-3secs)**
    - **`Serial` + Text `UUID` might be the better combination**
    - Are lookups on text columns slow even if indexed?
    - Better understand lookup and query speed for different types
2. When should filtering or query-like lookups be done on the client?
    - SQL is quicker for most data tasks? What about for text columns?
3. Cursory check of [security](#-security) and [errors](#️-errors)
4. Look up [FastAPI's current JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) setup and consider using it (for [security risk](https://github.com/fastapi/fastapi/discussions/9587))
5. Research `auth:oauth2` for secured routes.
    - https://stackoverflow.com/a/28503265
    - I don't think we need `client_secret` for a self-owned API
    - Might want to add rate limit, `client_id`, IP limit, etc.
6. Why does Rich Hickey dislike ORMs?
    - Are there any routes we can use plain SQL?
7. Consider adding more user details, such as a [`Profile`](https://piccolo-orm.readthedocs.io/en/latest/piccolo/authentication/baseuser.html#extending-baseuser) column
8. `WAL` mode is fine to use up to around `-c 75` concurrent connections
    - Do we bother using it? Does it actually help to non-block reads?
9. Running two Bombardier commands (one write, one read) is VERY slow (15mins+).
    - `bombardier -c 10 -n 5000 http://localhost:8000/events/`
    - `bombardier -c 10 -n 5000` with `http://localhost:8000/events/` POST
10. Test out [piccolo admin](https://github.com/piccolo-orm/piccolo_admin)
11. Test with [Locust](https://locust.io/) for concurrency with same [scenarios](https://github.com/coding-yogi/bombardier)
    - How many users can it handle?


## 🚀 Setup

```zsh
# Activate the virtual environment, then run the app
# which also sets up the database with `Event` table
uv run main.py

# Run the app in earlier chapters
uv run uvicorn api:app -- port 8000 --reload

# Setup the user table
piccolo migrations forwards user
# Create the first user (follow the prompts)
# See `../bruno/collection.bru` for user details
piccolo user create

# Populate the database in sqlite3
open -a TextEdit /sqlite.md

# Command for `GET`
curl http://localhost:8000/events/

# Compare `X-Process-Time` to actual response time
curl -kv -w '\n* Response time: %{time_total}s\n' http://localhost:8000/events/

# Command for `POST`
curl --request POST \
'http://localhost:8000/events/new' \
-H 'accept: application/json' \
-H 'authorization: Bearer [Generate a JWT token with Bruno]' \
-H 'content-type: application/json' \
-d '{"creator": null, "title": "Pyramid Stage", "image": "https://tinyurl.com/ed-sheeran-with-shakira", "description": "Ed Sheeran sings with Shakira at Glastonbury!", "location": "Glastonbury", "tags": [ "music", "adults", "event" ]}'

# Stress test a single API endpoint (should be 96% successful)
bombardier -c 100 -n 10000 -t 10s \
-H "Authorization: Bearer [Generate a JWT token with Bruno]" \
-H 'accept: application/json' -H 'content-type: application/json' --method=POST \
-b '{"creator": null,"title": "Pyramid Stage","image": "https://tinyurl.com/ed-sheeran-with-shakira","description": "Ed Sheeran sings with Shakira at Glastonbury!","location": "Glastonbury","tags": ["music","adults","event"]}' \
http://localhost:8000/events/

# Optionally stress test multi-users
https://locust.io/

# Backup your events with `sqlite-utils` and pretty print
sqlite-utils planner.db "select * from event" | python -m json.tool

# Cleanup Python files not tracked in `.gitignore`
# -d recursively, -e excluding, -i interactive mode
git clean -dx -e .env -i
```

## 📖 Book chapters

> **Completed up to chapter 8 (the focus of this readme)**
> Two last chapters removed as I dislike Docker and unit testing.

 See `chapter_` folders for comments and `#commit`s. I'm a fan of _barely testing_ while prototyping (easier with statically typed languages) but always [fix errors](#️-errors) as you find them, check your types, and use _just-in-time_ learning. Bruno handles [error checking](https://docs.usebruno.com/testing/automate-test/manual-test) manually (or use any GUI or CLI tool you prefer).

1. ~~Hello World~~
2. Routing (`1.6.0` — `1.6.6`)
3. Response models and error handling (`1.7.0` — `1.7.4`)
4. Templating with Jinja (`1.8.0` — `1.8.2`)
    — Json-only version (`1.8.1`)
5. Structuring FastAPI applications (`1.9.0` — `1.9.1`)
6. Working with the database
    - SQLModel (`1.10.0` — `1.10.6`)
    - ~~MongoDB~~[^2] (I'm sticking with SQLite)
7. Securing FastAPI applications (`1.11.0` — `1.11.9`)
    - Hash and compare passwords
    - Generating JWT tokens
    - Securing routes (with authentication)
    - CORS policy (middleware)
8. Planner app with testing (`1.12.0` - `1.12.18`)
    - Authentication, cherry-picking ORMs, error checking, refined JWT
    - ~~SQLModel (original version)~~ (`1.12.4`)
    - ~~Peewee (modified version)~~ (`1.12.11`)
    - Piccolo (my ORM of choice) (`1.12.18`)


### 📖 Chapter 8 (with extras)

> **My version of the [final chapter](./chapter_08/) covers more than the book.**
> Can be used as a base for other APIs and will try to keep up-to-date.

1. API testing with Bruno app (documents bugs)
2. `BaseUser.login()` to handle sign-in and hashing 
3. Better error checking, with data entry and JWT claims (security upgrade)
4. Piccolo-friendly folder structure with helpful comments
5. `/user/me` endpoint (a specific user's events)
6. `.returning()` instead of `select()` guards
    - `Event.creator` with `ID` of current user
    - [Non-optional](https://github.com/piccolo-orm/piccolo/issues/1319#issuecomment-3705946732) for update functions that allow it!


### 📝 Book errata

> Technical writing is tough, but there's lots of errors in this book!

1. `NewUser` model is mentioned but not created
2. `User` fields are not yet used (`List Int`)
3. `users.py` referred to as `user.py`
4. Dependencies are sometimes not properly introduced
5. `python-jose` [security risk](https://github.com/fastapi/fastapi/discussions/9587) (at the very least, use [`[cryptography]`](https://github.com/mpdavis/python-jose#cryptographic-backends))
5. Outdated packages and syntax, for example:
    - ~~`@app.on_event("startup")`~~ is now app lifecycle ...
    - which requires understanding `contextlib` and is tricky to learn!
6. `grant_type=` missing the `password` keyword in the authentication `curl` call
7. Double check your routes are properly formatted
8. More errata not listed ...



## 🔍 Documentation

> See comments and `localhost:8000/docs` for full documentation.

**Docs should live in one place and be kept up-to-date.** See file comments for API instructions, errors, types, and so on; Bruno ([manually](https://docs.usebruno.com/testing/automate-test/manual-test)) tests the API and documents some bugs. A helpful book, _[APIs you won't hate](https://leanpub.com/build-apis-you-wont-hate-2)_, goes into more detail on errors, design, schema, and documentation guides.

[Bombardier](https://github.com/codesenberg/bombardier) and [Locust](https://locust.io/) can be used to test for speed, and you may prefer unit testing for a production app. I've avoided documentation techniques such as `Annotated[]` and `"json_schema_extra"`, as they make for messy code.



## 🐍 Dependencies

The `pyproject.toml` is a bit messy: see `dependencies` group for `chapter_08` app. For a live production app you'll want as few dependencies as possible!



## ⏱ Performance

> It's folly to prematurely optimise! Do you have customers? Are you selling?

Premature optimization is the devil’s volleyball! Worry when you have reproducable and sustained bottlenecks. See the [performance](./PERFORMANCE.md) documentation for tips on managing API with SQLite. [Response size](#-response-size) is also very important (large responses take longer in Bruno than Curl, for example)!

### Middleware

> 🔍 Middleware effect on performance (compare and check!)

I've added an example timer header, which is very handy for the client! I think Bruno's response times have some latency; CURL is quite similar. It's a CPU clock speed.

Beware! Middleware can significantly degrade FastAPI performance, with standard `BaseHTTPMiddleware` reducing throughput by `26.81%` to `41.64%` and increasing request latency by approximately `19ms` to `37ms` per layer. This performance impact can be virtually eliminated by using a Pure ASGI middleware (Starlette-style) instead of `BaseHTTPMiddleware` (using FastAPI's decorator).

### 🐌 Response size

#### 🚀 Return less data!

> **Only return the essential data:** limit rows and columns.

Returning less data (e.g: all `Event.title`s) reduces the speed to `673ms` (Bruno)! This might mean on your `/events/` url you display partial `Event`s and clicking through to `/events/{id}` shows full details.

#### ⚠️ Lots of rows and columns = slow performance

> Lookup for lots of rows can have slow performance! Clients have latency!

1000+ rows with current Piccolo + SQLite setup (all columns):

- ~2.16s+ (Bruno)
- ~1.651628s (Curl)
- ~0.153s (sqlite3 real)

Tests so far show similar performance for `Serial` and `UUID` (Bruno, 10003 rows).

1. `UUID` is stored as text (may have slow performance)
2. `Serial` integer _should_ be faster ...
3. `Event.raw` doesn't seem to make any difference?

It may be better to use _both_ `Serial` and `UUID` for private and public facing. Joins should be faster with an `Int` type. Shorter `UUID`s might also be [advisable](./testing/uuid/shortcodes.py) as shorter text may speed up lookups (at expense of more potential collisions).



## 🔐 Security

> **Security is a bitch.** Production API needs to protect itself from all sorts of hacks.

Out of scope for this repo, but here's some suggestions. What are the major threats?

1. **Assure that all routes that should be protected _are_ protected**
    - A user should never be able to edit or delete another user's items
    - A users sensitive information should never be exposed
    - Destructive actions (especially bulk) should be removed unless they're
      absolutely essential.
2. Use `python-jose[cryptography]` latest version
    - `python-jose` version in the book is [unsafe](https://security.snyk.io/package/pip/python-jose)
    - OpenSSL 3.0.0 [doesn't support](https://cryptography.io/en/latest/faq/#installing-cryptography-with-openssl-older-than-3-0-0-fails) Older MacOS, but your server should
3. Prevent common attacks such as XSS and DDoS
    - Exclude off-domain requests to the API with `app.add_middleware()`
    - Restrict headers (such as CURL) or by IP address
    - Rate limit or create hard-to-guess `client_id` and `client_secret`s
4. Never allow anyone else to [inject SQL](https://security.berkeley.edu/education-awareness/how-protect-against-sql-injection-attacks) into your queries

Have a professional check over your code, or research thoroughly.[^3] Nothing is foolproof; you'll want to watch your server logs and database for signs of tampering.



## ⛔️ Errors

> FastAPI errors generally use a `HTTPException`.

**According to _[APIs you won't hate](https://leanpub.com/build-apis-you-wont-hate-2)_ a `HTTPException` might not be good enough.** You'd have to create your own `Error` Pydantic type, or use a [plugin](https://github.com/NRWLDev/fastapi-problem) for standards like [rfc9457](https://www.rfc-editor.org/rfc/rfc9457.html). `String`ly typed errors (especially if variable in a single endpoint) are a bad idea, but can be used with Elm's `Json.Decode.oneOf` as a temporary measure.

### ✅ Common errors

> ⚠️ SQLite errors are difficult to catch with `try`/`except` blocks. Your best bet is to [add logging](https://betterstack.com/community/guides/logging/logging-with-fastapi/) to a file in production to view bottlenecks and errors. Some errors have been handled properly.

Tick should be resolved / serious problem in bold. List errors as they come up! 

1. **SQLite errors**
    - [ ] **`sqlite.IntegrityError`** for `null` / `duplicate` values (won't insert)
    - [x] **`sqlite3.OperationalError` database locked** (`-c 10` or less)
        - [ ] `SQLITE_BUSY` is a timeout error (hard to fix)
2. **Input errors**
    - [x] Email is not a proper email (handled by Pydantic only, not Piccolo)
    - [ ] `TEXT` contains HTML or other non-plain text values
    - [ ] Password field is not secure enough (currently `> 6` characters)
3. [ ] **Response errors**
    - [x] Endpoint gives `422` Unprocessable Content (make sure `-H`eaders are set)
    - [x] Endpoint redirects instead of resolving (see `307` redirects below)
    - [x] No DB results for query (`is not None` seems like enough)
    - [ ] Response giving away sensitive data (vague is better, not 100% handled)
4. [ ] **Type errors**
    - [ ] `POST` values validate when they shouldn't (`{ "creator": null }` passes)
    - [x] Type too permissive (e.g: `create_pydantic_model` uses `Any` type)
5. [ ] **User errors**
    - [ ] Account not approved by admin (you can handle this internally)
    - [x] User is able to delete data that doesn't belong to them

#### ⚾️ Catch and throw

**You can either "catch" or "throw" an error.** Think of it like baseball, whereby catching the ball allows us to handle or examine an error (`try`/`except`), and a throw sends a helpful error to our user (`raise`). It seems that _throwing_ an error is more performant than _catching_ it first.

#### 🔐 Impossible routes

> If it's destructive or hackable, consider leaving it out!

Rather than having a live `piccolo-admin`, `DELETE` all endpoint, or user roles, do it locally on a secure device; same goes for `piccolo user create` while you're prototyping. There's no need to do bulk destructive actions early on. Hire a professional to build out a secure platform.

#### `307` redirects (trailing slash error)

> FastAPI treats `/events` and `/events/` as two distinct endpoints.
> You'll need to do a reverse proxy with your server setup with [`/` redirects](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#redirects-with-https).

This stumped me for ages. Testing endpoints was returning a `307` because my endpoint was setup _without_ a trailing slash and I'm including it (or vice-versa). For some reason Bruno didn't seem to have this problem! Also make sure you're calling the API with the correct method (e.g: `POST`).

#### 🤩 Authenticated routes

> I'm not 100% sure if `/user/signup` is free from "database locked" error.

We must fetch `BaseUser.id` from `authenticate()` and that _could_ be a read then a write. See "SQLite and Async problems" in `planner/tables.py`. There's a lot of debate over which value should be stored in a JWT (the less user info revealed the better), but ideally we'd have `id` at hand.



## ⚙️ Tooling


### 💾 Piccolo

> A great [little ORM](https://piccolo-orm.readthedocs.io/en/latest/piccolo/getting_started/playground.html) that doesn't require `open()` and `close()`ing the database.

Piccolo takes a while to get into, but it's very capable. SQLite async is problematic for [concurrent writes](https://piccolo-orm.readthedocs.io/en/1.1.1/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html), so try not to [read/write](https://github.com/piccolo-orm/piccolo/issues/1319) in the same endpoint (`> 10` people inserting is a struggle)! Write-ahead logging mode (`WAL`) helps a bit, and take care with inserts (remember, SQLite [isn't type safe](https://github.com/piccolo-orm/piccolo/issues/1187) without strict mode).


### 💾 SQLite

> 🌎 The most widely deployed database in the world!

**Gives great control over data and easy to backup or manipulate with [`sqlite-utils`](#-sqlite-utils).** SQLite is not running in strict mode, as this limits column types that Piccolo handles for us. To make sure `Any` types can't infect our database, be sure to add _at least_ an `EventDataIn` Pydantic class for the API layer! Need strict types in the database? Use Postgres. Heavy concurrent writes? [Turso](https://github.com/tursodatabase/turso) is on the way as a drop-in replacement.

- Pragmas can be added directly once the app is running
    - E.g: [`PRAGMA journal_mode=WAL`](https://sqlite.org/wal.html)[^4]
- Piccolo defaults to `not null` columns, and `distinct` primary keys
    - SQLite _does_ check these and will throw an error

I'm not a big fan of migrations (support for these are limited anyway), and prefer GUI tools ([SQLite Browser](https://sqlitebrowser.org/), [Enso](https://ensoanalytics.com/), etc). The aforementioned `sqlite-utils` comes in very handy, and [`piccolo-admin`](https://piccolo-admin.readthedocs.io/en/latest/) is another option.

#### 💾 Models

> See `tables.py`. Make sure models accurately reflect your needs.

**As your app evolves, `planner.tables` and `planner.db` will need updating.** To change a column, such as adding `null` or `unique` constraints, the original table and data must be migrated. I'll be  doing this manually, and JQ and `sqlite-utils` come in handy. For a safe way to manually update a column, you could:

1. Backup all data
2. Create a new column (with SQL or Piccolo)
3. Copy data over from old column to the new one
4. `DROP` the old column (and remove from `tables.py`)

Small, incremental changes to `planner.tables` are better than big bulk ones. It's also wise to mock a local database and test any changes before pushing them live.

Other aspects of the model could be better designed; a many-to-many `Tags` table might be preferrable to `List[string]` for example (each user's tags are currently independent of each other), making them easier to share between different `Event`s. Look up "database normalization" for more info.[^5]

Raw SQL is an option with Piccolo, but you'll need to map the data to your own Pydantic classes.

#### 🛠 SQLite Utils

> **Very handy for testing, preparing, and backing up data!**
> Can be used in combination with [JQ](https://jqlang.org/) or [JSON Server](https://marketplace.visualstudio.com/items?itemName=sarthikbhat.json-server) for mocking.

[SQLite Utils](https://sqlite-utils.datasette.io) can format data from `json`, `csv` files in memory, or from/to `.sqlite` files. You could take a 3rd-party Tally Form → export to `.csv` → then [create a SQLite database](https://alexwlchan.net/notes/2024/use-sqlite-utils-to-convert-csv-to-sqlite/) ...

```terminal
sqlite memory form.csv "select * from form" | python -m json.tool
```


### 🤝 API testing

#### 🐶 Bruno

> Bruno could be the "high level viewpoint" of your API

Bruno is not suited for documentation, but it's great for manual testing! `../bruno/collection/chapter-*` files can be loaded into Bruno to test endpoints for each chapter. Go to `Collection settings -> Auth` to generate an authentication JWT token. There's also a VS Code [plugin](https://marketplace.visualstudio.com/items?itemName=bruno-api-client.bruno). Errors and bugs _could_ be logged with Bruno (with QA), but it's easy for docs to get out of sync. 

#### 💣 Bombardier

> ⚠️ Never prematurely optimise your prototype! Wait for bottlenecks to appear.

**All things being (more or less) equal, prefer the easiest-to-read, most consistent, simplest design route.** Bombardier is handy for checking which design routes are more performant (and which slow us down).

It's more important that code is understood and easy to maintain, over a [few `ms` bump](https://www.reddit.com/r/dotnet/comments/1hgmwvj/what_would_you_considered_a_good_api_response_time/) in speed. See the file `chapter_08/testing/bombardier` for results; we've stress tested our API with Bombardier.



## 🚢 Deploy with `UV`

> Server must be compatible with Async FastAPI.
> Hosting options include Hostinger VPS and Python Anywhere.

You can `pip install uv` on an Ubuntu live server, use a package manager (like Mise), or install the binary with `curl` instead. Initialise the project with `uv sync`, activate Python's virtualenv  `source .venv/bin/activate`, then run the app. It's possibly easier to setup UV manually, but [Github Actions](https://docs.astral.sh/uv/guides/integration/github/) is also an option (example below).

```yaml
steps:
  - uses: actions/checkout@v6

  - name: Install uv
    uses: astral-sh/setup-uv@v7

  - name: Set up Python
    run: uv python install

  - name: Install the project
    run: uv sync --locked --all-extras --dev

  - name: Run something
    run: uv run python3 some_script.py
```

You'll also need to setup `uvicorn` to run with HTTPS secure connection.








[^1]: Choosing an ORM was particularly difficult with FastAPI as it's async. No every ORM supports this and I tried both SQLModel (didn't like the documentation) and [PeeWee](http://docs.peewee-orm.com/en/latest/) (great but no async). [IceAxe](https://github.com/piercefreeman/iceaxe) is another nice looking option (very young and Postgres only), and there's a ton of synchronous ORMs like [Pony](https://ponyorm.org). To be honest though, I'd probably choose a better designed language ([Roc](https://www.roc-lang.org) looks interesting) for a big speed bump. Python is a handy scripting language, but it's errors and style ain't the best.

[^2]: I tried and failed to get MongoDB working. I found it an absolute arse to setup (especially for beginners) and more hassle than SQLite (or even Postgres, I imagine). The book's `chapters` from `_06/` or `_07/` onwards uses MongoDB; I decided to part ways with the book and use SQLite instead.

[^3]: If you're a great programmer, or don't mind suffering through the pain of low-level learning, then do it yourself. My goals are quite distinct and I simply don't have the time to learn everything.

[^4]: All processes using a database must be on the same host computer; WAL does not work over a network filesystem.

[^5]: Joins are easier to maintain than lists. In the book, the latter chapters use MongoDB, which is unstructured data. Here, we're trying to keep data atomic and [normalised](https://youtube.com/watch?v=GFQaEYEc8_8) with SQLite, so it's easier to search for (and `JOIN user ON event.creator = user.id`) later.
