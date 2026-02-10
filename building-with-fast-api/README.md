# README


<!-- ***************************************************************************
     PRINT OUT AND REVISE: CUT OUT ANYTHING UNECESSARY
**************************************************************************** -->

> Currently SQLite struggles with concurrent writes.

This README is predominantly for `chapter_08/` but some information is relevant for earlier chapters. There really is an _insane_ amount to think about with APIs and app architecture. It's a real timesink. Keep it light for startup prototypes and hire later.


## Setup

> Setup `/chapter-08`, which is the most substantial code in the book

```bash
# Activate the virtual environment, then run the app
# Also sets up the database with `Event` table
uv run main.py

# Setup the user table
piccolo migrations forwards user
# Create the first user (follow the prompts)
# See `../bruno/collection.bru` for user details
piccolo user create

# Populate the database
open -a TextEdit /sqlite.md

# Stress test your API
bombardier -c 10 -n 10000 -H \
"Authorization: Bearer [Generate a JWT token with Bruno]" \
-H 'accept: application/json' -H 'content-type: application/json' --method=POST \
-b '{"creator": null,"title": "Pyramid Stage","image": "https://tinyurl.com/ed-sheeran-with-shakira","description": "Ed Sheeran sings with Shakira at Glastonbury!","location": "Glastonbury","tags": ["music","adults","event"]}' \
http://localhost:8000/event/new
```

## Book chapters

> Each step of the book is reflected in the tags. I've decided to ommit the final
> two chapters around testing and deployment, as I don't prefer that method.

You can use the REPL in early chapters. We're error checking with Bruno (lots of methods to [test](https://docs.usebruno.com/testing/automate-test/manual-test) APIs and I prefer GUIs or simple CLI tools). Generally with prototypes it's best not to prematurely optimise and fix errors "just-in-time".

1. Hello World
2. Routing (`1.6.0` — `1.6.6`)
3. Response models and error handling (`1.7.0` — `1.7.4`)
4. Templating with Jinja (`1.8.0` — `1.8.2`)
    — See `1.8.1` for our `json` version
5. Structuring FastApi applications (`1.9.0` — `1.9.1`)
6. Working with the database
    - SQLModel (`1.10.0` — `1.10.6`)
    - ~~MongoDB~~[^2] (I'm sticking with SQLite)
7. Securing FastApi applications (`1.11.0` — `1.11.9`)
    - Hash and compare passwords
    - Generating JWT tokens
    - Securing routes (with authentication)
    - CORS policy (middleware)
8. Testing (`1.12.0` - `1.12.14`)
    - Picking an ORM, authentication, JWTs, and error checking
    - ~~SQLModel (original version)~~ (`1.12.4`)
    - ~~Peewee (modified version)~~ (`1.12.11`)
    - Piccolo (chosen version)
        - API testing with Bruno app (documents bugs)
        - `BaseUser.login()` to handle sign-in and hashing (`1.12.12`)
        - Tidying up errors, data entry, and JWT claims
        - Piccolo-friendly folder structure with helpful comments
        - A `/user/me` endpoint (for username and settings)


## Documentation

> I use comments as documentation which can be found in `localhost:8000/docs`.

This seems to be the best way to handle docs for types and API instructions. There's also `/redoc`, although I don't prefer it's layout.

- See _[APIs you won't hate](https://leanpub.com/build-apis-you-wont-hate-2)_ for error, design, schema, and documentation guides
- FastAPI comes with an OpenAPI.json way to document your API endpoints ...
- The book uses `/doc` code annotations which I prefer not to use (feels messy)
- I prefer to use docstring comments (`""" """`) within functions for documentation.

### Bruno

> Bruno could be the "high level viewpoint" of your API

Ideally, Bruno can be kept for error checking and logging bugs only. You can load the `../bruno/collection/chapter-*` files into Bruno to test out endpoints for each chapter. For most routes you'll need to generate a JWT token at `Collection settings -> Auth`. It doesn't seem a good idea to re-write documentation in the Bruno endpoint READMEs.

In this repo I'm [_manually_ checking](https://docs.usebruno.com/testing/automate-test/manual-test) endpoints but in production you'd probably want to automate this (either unit testing or a GUI/Ai).


## Models

> As your app evolves, make sure models accurately reflect your needs.

As your app evolves, you'll need to update the `planner.tables` model. For example, if you add `null` or `unique` constraints to certain fields, you'll have to update or replace your original tables. This can be helped along with `sqlite-utils` and JQ.


## Security

> Production API needs to protect itself from XSS and DDoS, or other hacks.

This is out of scope for this repo.


## Errors

> FastApi errors generally use a `HTTPException`.
> See also [APIs you won't hate](https://leanpub.com/build-apis-you-wont-hate-2) by Phil Sturgeon.

According to _APIs you won't hate_, a `HTTPException` might not be good enough. You'd have to create your own `Error` Pydantic type, or use a [plugin](https://github.com/NRWLDev/fastapi-problem) for standards like [rfc9457](https://www.rfc-editor.org/rfc/rfc9457.html).

### Common errors

> We're currently not handling errors "correctly" but I dislike `try/except` blocks.
> You can add logging to a file in production and catch errors there as well.

List errors as they come up: errors marked with ✅ should be resolved, and marked **Bold** is a serious problem.

1. ✅ **SQLite database is locked error** (async and concurrent connections)
2. [ ] **API timeout** due to (1) (immediately returns a `SQLITE_BUSY` error)
3. [ ] **`sqlite.IntegrityError` for `null`** and duplicate values (won't insert)
4. ✅ No DB results for query (`is not None` seems like enough)
5. [ ] Response giving away sensitive data (vague is better, not 100% handled)
6. [ ] `TEXT` contains HTML or other non-plain text values
7. ✅ User is able to delete data that doesn't belong to them
8. ✅ Email is not a proper email (handled by Pydantic only, not Piccolo)
9. [ ] Password field is not secure enough (currently `> 6` characters)
10. [ ] Account not approved by admin (you can handle this internally)
11. [ ] `POST` values validate when they shouldn't (`{ "creator": null }` passes)
12. ✅ Endpoint redirects instead of resolving (see `307` redirects below)
13. ✅ Endpoint gives `422` Unprocessable Content (make sure `-H`eaders are set)
14. ✅ Type too permissive (e.g: `create_pydantic_model` uses `Any` type)

### Impossible routes

> If there's anything destructive or hackable, consider leaving it out!

You can do admin stuff offline with `sqlite-utils`, GUI, or no-code. Wait until you can hire a professional to build out a secure platform (with roles). `piccolo-admin` and `piccolo user create` are good examples of this, and  `DELETE` all `Event`s is a terrible idea and not necessary.

### `307` redirects (trailing slash error)

> If your endpoint url has `/no-ending-slash`, do **not** include it in API call. FastAPI treats paths with and without trailing slashes as distinct endpoints by default.

It took me ages to figure out that Bombardier and CURL were returning `307` because my endpoint was setup _without_ a trailing slash and I'm including it. For some reason Bruno doesn't seem to have this problem? See also [NGINX proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#redirects-with-https) for redirects.

Also make sure you're calling the API with the correct method (e.g: `POST`).

### Authenticated routes

> I'm not 100% sure if `/user/signup` is free from "database locked" error.

We must fetch `BaseUser.id` from `authenticate()` and that _could_ be a read then a write. See "SQLite and Async problems" in `planner/tables.py`. There's a lot of debate over which value should be stored in a JWT (the less user info revealed the better), but ideally we'd have `id` at hand.

### Performance

> It's folly to prematurely optimise! Are you selling? Do you have customers?
> Some [error checking](https://realpython.com/python-exceptions/) methods can potentially be slow (like `try`/`except` blocks).

1. **Catching errors can be time-expensive;** throwing them is cheap and fast
2. Elm's `OneOf` could catch stringly `detail` types, but that's bad practice
3. **Python's [`match`](https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/) [doesn't work](https://discuss.python.org/t/python-3-10-match-case-syntax-for-catching-exceptions/11076/22)** in the way you'd expect (unlike Elm's `case`)
4. Shorthand is `value | Exception` but different status codes may be needed
5. **SQLite is not very good at _sustained_ high load concurrent writes**

You can either "catch" or "throw" an error. Think of it like baseball, whereby catching the ball allows us to handle or examine an error (`try`/`except`), and a throw sends a helpful error to our user (`raise`). It seems that _throwing_ an error is more performant than _catching_ it first.

#### Timeout and broken pipe

> ⛔️ Contrary to what I expected, `timeout=200` does NOT improve things.

SQLite `sqlite3.connect()` takes a timeout (in seconds). The query logs were all out of whack and (I don't think) response numbers in order of operation.


## Tooling

### Bombardier

> Never prematurely optimise your prototype! We can stress test our API with Bombardier.
> Handy for checking which design routes are more performant (and which slow us down).

See `testing/bombardier` for results. If all things are (more or less) equal, always use the easiest-to-read, most consistent, simplest design route. It's more important that code is understood and easy to maintain, over a [few `ms` bump](https://www.reddit.com/r/dotnet/comments/1hgmwvj/what_would_you_considered_a_good_api_response_time/) in speed. Here's an example:


-----

## Intro

> This repo is my working copy of the book [Building Python APIs with FastAPI](https://www.packtpub.com/en-us/product/building-python-web-apis-with-fastapi-9781801074513)

**There's so much to think about when writing an API and considering your app architecture** and it can feel very overwhelming, even with the small examples in this book. There's a tendency to have a lot of questions and a big old wishlist of things you'd like to add, but try and keep it simple wherever possible. Make working code first. Understand it thoroughly later (or never). There's lots of things that can go wrong, and tackling them (and learning) just-in-time is perhaps a saner approach.

**It also takes a considerable amount of time to switch ORMs** so try to learn one thoroughly and stick to it! Is the alternative 10x faster/better? No? Stick to what you know then!

**The book goes into detail on building a http server API with the [FastAPI](https://fastapi.tiangolo.com/).** In general it's a good book, but there's a lot of errors, or areas where you've got to interpret and fix things for yourself. FastAPI has also made a lot of changes since the book was published (dependency hell). It actually took me quite a bit of time (months) to get through, as I had to re-familiarise myself with Python, and FastAPI isn't always obvious.

As I've written before, I'm [not a huge fan](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style) of Python, but it's a handy scripting language and you get used to it. Errors and typing are _especially_ annoying — a simple typo, missing word, or rogue piece of code can torpedo your program and be _extremely_ difficult to track down with FastAPI and Python.


## My learning goals

> Learning to program is a _never-ending_ task and there's a ton of ways your app can go wrong.
> I'm a fan of simplicity: focus your learning frame, cut down code, and reduce your burden.

1. Simple is better
2. Smaller is better
3. Less is better (be brutalist!)
4. Human readable is better (documentation)
5. Boring is better! (aim for stability)
6. Brutal is better! (see the Brutalist movement)

**If I can handle 3k users on a simple server, I'm happy.** I'm not out to build an all-singing, all-dancing app, and the goal is to validate a business model, then build out a technical team if it's successful! Things like queuing, sharding, email validation, and so on, are not my concern right now. It's always good to have a mentor, or to outsource for more complex and mission-critical tasks.

- **My learning frame** is a personal learning "do" and "don't do" list
- **The [5 finger rule](#the-5-finger-rule)** to choose books, tuts, and packages
- **Shallow learning is (mostly) ok** as programming knowledge is a gigantic rabbit hole.
- **Some things can be a [black box](#a-black-box)** that are set and forget (or outsource)
- **I don't enjoy low-level detail** so will avoid that kind of work[^1]


## FastAPI pros and cons

> It seems quick, as advertised, but remember it's `async`!

1. **It's `async`, for `async` tools** (this isn't always needed).
    - PeeWee [does not play nicely](https://github.com/fastapi/fastapi/discussions/8049) with it![^2]
2. **It works well with SQLite.**[^3]
    - SQLite is great as it's easy to migrate and setup. It's just a file!
    - SQLite doesn't default to `async`: you'll need an ORM that supports [`aiosqlite`](https://github.com/omnilib/aiosqlite)

The downsides ...

1. **FastAPI documentation is not always clear enough.**
    - SQLModel documentation is longwinded, and gets combined with SQL tutorials ...
    - This makes it way harder to scan documentation for query syntax, etc.
2. **Python error messages are shit** (see [coding style](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style)).
    - Pydantic, PyLance, and PyRight help a bit with typing.
    - Long traceback error messages (often the last message points to the problem)
    - Cryptic errors and hard to pin down what's wrong





## Errata

> The book has quite a lot of errors ...
> And make sure your routes are properly formatted!

Here are a few I caught (there's more)

1. `NewUser` model is mentioned but not created
2. `User` fields are not yet used (`List Int`)
3. `users.py` is referred to as `user.py`
4. Dependencies are sometimes not introduced clearly!
    - `SQLModel` is imported but no download is mentioned
    - Which `jose` package do you mean? There's more than one!
5. Some packages and syntax are outdated and need updated copy:
    - ~~`@app.on_event("startup")`~~ is now app lifecycle ...
    - Which requires an understanding of `contextlib` and is tricky to learn!
6. `grant_type=` missing the `password` keyword in the authentication `curl` call.


## Dependencies

> Always keep your dependencies to a minimum ...

The `pyproject.toml` dependencies file is a mess. It holds all dependencies for chapters of the book, as well as some chapters which have different versions (such as MongoDB or Peewee ORM). Your app dependencies should be kept to an absolute minimum and regularly pruned and maintained.


## Commands

### Using `uv`

> [Some notes](https://github.com/astral-sh/uv/issues/10543#issuecomment-2587276856) on getting setup with `uv` and `venv`. `uv run` (without `source .venv/bin/activate`) will activate the virtual environment then run the command.

```terminal
-- Create a new project
uv init

-- Run your program (from function)
uv run uvicorn api:app -- port 8000 --reload

-- Run your program (from file)
uv run main.py

-- Test types and errors
uv run pyright main.py

-- Add to your .zshrc or .bash_profile
alias activate='source .venv/bin/activate'
```

### Deploying with `uv`

You can `pip install uv` on a live server (like Ubuntu), or `curl` install. You can either `uv run` or `source .venv/bin/activate` to start using the Python virtualenv (for a Github Action that probably doesn't matter, but locally it's definitely better). Deploy with [Github Actions](https://docs.astral.sh/uv/guides/integration/github/)!

```yaml
steps:
  - uses: actions/checkout@v4

  - name: Install uv
    uses: astral-sh/setup-uv@v6

  - name: Set up Python
    run: uv python install

  - name: Install the project
    run: uv sync --locked --all-extras --dev

  - name: Run something
    run: uv run python3 some_script.py
```

### API and CURL

```terminal
-- Curl is a `GET` by default
curl http://localhost:8000/todo
{"todos": []}

-- `POST` an entry to the to-do list
-- Quotes inside `json` must be escaped or inside `''` single quotes
curl -X 'POST' \
  'http://localhost:8000/todo; \
  -H 'accept: application/json' \
  -H 'Content-type: application/json \
  -d '{"id: 1, "item": "First to-do is to finish this book!" }'

-- Create a JWT token at `/signin`
curl -X 'POST' \                                        
  'http://localhost:8000/user/signin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=[email]&password=[password]&scope=&client_id=string&client_secret=string'
```

### SQL

```sql
-- Chapter 07 code
SELECT u.email, e.title FROM user AS u
JOIN event AS e ON u.email = e.creator;
```

### Misc

```python
# Inspect an object's properties
from pprint import pprint
pprint(vars(your_object))
```


## Keeping things simple

1. **Keep things as simple as possible.**
    - Your models, documentation, tooling, dependencies, etc.
    - Actively remove code and simplify processes where possible.
    - `.jinja` at scale can get messy, why not try Elm?[^4]
    - You might want to split your API layer from your DATA layer.
2. **If things are too complicated for you, hire.**[^1]
    - Have a professional look over your code ...
    - Or, have them do it for you, and treat things as a [black box](#a-black-box).
    - Stick to a narrow problem set that suits your capabilities.
3. **Write working code first, worry about the finer details later.**
    - Minimal use of `Class.methods`, `@decorators` and so on (only when necessary).
    - I don't like Python as a language much, so only learn what I must!
4. **🌟 Let the code do the talking, where possible**
    - I've got copious amounts of comments and wishlists in some chapters.
    - Aim to cut these down to the bare necessities (lean on documentation).

### The 5 finger rule

> A bit like reading for kids: how much of it do I understand?

1. **I can understand 50-70% of the language used** (tool or package documentation)
    - The 5 finger rule avoids texts that are too difficult for you!
2. **It feels like my regular language that I know quite well** (familiarity)
    - You don't have to understand everything, but you have to write working code.
    - Try to stick to your [preferred coding style](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style) as it reduces cognitive load (Elm-like)
3. **The code examples don't confuse or scare me** (not overly academic or complex)
    - Documentation is well written, in plain english, for humans not automatons!
4. **Plenty of helpful guides from Google, StackOverflow, etc** (well known)
    - A niche language is going to be tricky if it's light on tutorials
5. **A friendly, helpful, patient, community**
    - Elm is great! Python seems generally OK.
6. **Boring. Stable. Not going to blow up**
    - Or at least exciting and stable enough to risk breaking changes.


## A black box

> Some things can be set-and-forget.
> There's simply too much to learn with programming!

Some things I want to treat as an input and output: I don't want to worry about their internal mechanisms.

1. I don't want to learn some things (my learning frame)
2. I'd rather hand over a low-level task to a collegue (email validation)
3. `auth` and `database` are super important to get right (I don't trust myself!)


## User experience, architecture, and privacy

> `/delete` is something that should _never_ happen unless you're an admin! I've removed this option in later chapters; user auth and permissions is an advanced feature and should be handled with care (and experience).

Be mindful of the customer journey, what does and doesn't make sense for a particular user. Remember the last time you deleted something by accident, or refreshed the page and lost all your form data? Those kind of things.

- `DELETE` should notify the user: "Are you _sure_ you want to do that?"
- There's _frontend_ problems: a nice experience and notifying users of changes.
- There's _backend_ problems: making sure one user doesn't tank other user's data!

When designing your API architecture, consider the end-user: their needs and experience. Is it better to have a dedicated endpoint to edit an event, or do it from the `/events` route? Do you want the `book_id` url [mushed together](https://www.goodreads.com/book/show/33396914-assassin-s-quest) with the name? How do you match a [user's list of books](https://www.goodreads.com/review/list/79624791-michael-wilkinson?shelf=to-read) in the database and the route? Go and see how other apps are doing it.

Also consider security. Which data points should be _public_ (an `Event.id`)? Which _private_ (a `User.id`)? If `User.id` was public, a data scraper can easily increment the url path: a `shortuuid` might be better (you can always have this column next to the _real_ `user_id`. Do you publically expose a user profile and their lists, or make that private?!


## Choosing an ORM

> SQLModel is fine for single table `select()`s but I found it confusing for joins, and the documentation could be a lot better. I didn't find it very intuitive.

Feel free to use [SQLmodel](https://sqlmodel.tiangolo.com/), but there are reasons not to:

1. ~~SQLModel tightly couples it's models~~ (shares models with API)
    - **Better to decouple your models: API layer and DATA layer** (model for each)
3. ~~An abstraction of an abstraction~~ ([SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/) is narly, huge, complicated)
    - A lighter ORM that's been built from the ground up could be preferable
4. ~~Merges SQL tutorials with SQLModel documentation~~ (verbose and difficult to pinpoint)
    - A smaller ORM with the [5 finger rule](#the-5-finger-rule) is better (must be `async`)

Below are ORMs that'll work well with FastAPI. Alternatively, you might like to check out [Bottle](https://bottlepy.org) or [Sanic](https://sanic.dev) (WGSI). They both work with PeeWee and have data validation (you'll have to check if they support `auth/` in a similar way).

### It's good to have a picking criteria

> How do I make a decision on which ORM to use?
> Backend is difficult, and there's a lot that can go wrong!

Use the [5 finger rule](#the-5-finger-rule) first, but be aware of things that are useful: for example, does it allow setting PRAGMAS for [SQLite strict mode](https://sqlite.org/stricttables.html) and other concerns?


### A few options

> I'd pick [PeeWee](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html) or [Pony](https://docs.ponyorm.org/) for a non-async framework. The main [problem with `async`](https://fastapi.tiangolo.com/async/#asynchronous-code) is having to [scatter your app](https://charlesleifer.com/blog/asyncio/) with `await` calls.

1. **Picallo** is great but [isn't 100% async](https://piccolo-orm.readthedocs.io/en/1.1.1/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html).
    - 🚀 **See [the playground](https://piccolo-orm.readthedocs.io/en/latest/piccolo/getting_started/playground.html) before you get started.**
    - You'll also have to [validate your types](https://github.com/piccolo-orm/piccolo/issues/1187) 
2. **[Ormar](https://collerek.github.io/ormar/latest/)** with SQLite async, but less mature than Picallo (2025).
    - Unfortunately it's another abstraction of an abstraction (built on SQLAlchemy)
    - More tightly integrated with FastAPI and Pydantic than [encode orm](https://github.com/encode/orm)
3. **Tortoise ORM** (feels clunky to me, see [this example](https://tortoise.github.io/examples/fastapi.html))
5. **[IceAxe](https://github.com/piercefreeman/iceaxe)** looks a really nice option (but very young)
    - I like it's simplicity and similarity to raw SQL, but it's Postgres only ...
    - One to watch for when your app gets past a couple thousand users with SQLite
    

I'm sure there's more (or will be) but these seem a good fit. Also see Reddit's "[What is your go-to ORM?](https://www.reddit.com/r/FastAPI/comments/1fjta2e/what_is_your_goto_orm/)". The alternative to using asyncio is to choose [boring](https://mcfunley.com/choose-boring-technology) technology, and simplify your stack ([PeeWee](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html) and any compatible [framework](https://docs.peewee-orm.com/en/latest/peewee/database.html#framework-integration)!)

### RAW SQL, JOINs, app architecture, and mapping data

> I might want to handle database creation and migration manually?
> But have a representation of it with the `User` and `Event` models.

For read-only code you might want to use raw SQL queries, but you'll still need to map the data onto your `User` class, or a `dict`ionary. In the book, we also create a `List[int]` of `Event.id`s — we don't really need these!! Only store data like this if your [app architecture](https://openlibrary.org/dev/docs/api/covers) depends on it.

OpenLibrary, for instance, has `List[int]` of images which map to a `/covers` route, with `-S`mall, `-M`edium, and `-L`arge images. Our API is NOT publically consumed, so we likely want to deal with SQL `join`s and serve the full image paths within the `Event` object.

Remember, any data point on your API must be called from the database and maintained. That means anytime a `User` adds/removes an `Event`, you'd have to add/remove from that `List`. Don't do it if it's not needed![^5]

### Migrations

**I'm not worrying about migrations** in this repository, but make updates manually.

### Choose a (better?) different language?

The nuclear option is to ditch Python completely, and pick a different language. [Ocaml](https://aantron.github.io/dream/), [Elixir](https://phoenixframework.org/), [Roc](https://github.com/roc-lang/basic-webserver), or any other statically typed functional language.

Alas, you're looking at 2-3 months to change tools, so just get something out there and worry about that later. Don't over optimise before you've proven your business model! Honestly, getting through this book has been a slow process, so don't take that journey lightly.


## Documentation

> I'm using [Bruno](https://usebruno.com) to test and document my API.

FastAPI gives us `localhost:8000/docs` and `/redoc` for documentation, but I like Bruno as a simple way to test your API. You can use `Annotated[]` and `"json_schema_extra"` to format your `/docs`, but it makes for messy and verbose code. Stick to Bruno!


## Tooling

> Your production app should look like this by `chapter_08` ...
> This repo's `pyproject.toml` contains all chapter packages, so it's a bit of a mess. Don't do that in production.

In your `pyproject.toml`:

- [Pydantic](https://pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [Python plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.python) for VS Code
- [PyRight](https://microsoft.github.io/pyright/) (CLI in [strict mode](https://github.com/jackgene/reactive-word-cloud-python/blob/b48306f94e1038c26c7c70ab56337ab26fa2b719/pyproject.toml#L21-L23), Pylance for VS Code)
- Your ORM of choice!
    - Take care with [raw SQL](https://www.youtube.com/watch?v=Cp3bXHYp-bY)!

### Bruno

> A great API test kit for Mac.[^6]

For your tooling, you might like to use Bruno. I prefer Bruno's way of writing documentation, but you must write it out manually (whereas `/docs` are automatic). The benefit of Bruno is that we can _easily switch out to another API framework_, and keep all our tests in place!

- **[OAuth2](https://docs.usebruno.com/auth/oauth2/overview)** can be setup in your collection settings.
- FastApi `/docs` can be saved as `.json` file and added as a new collection to speed things up.
- Take care with your routes: `:id` (params) must be added to your Bruno path!
- [VS Code plugin](https://marketplace.visualstudio.com/items?itemName=bruno-api-client.bruno) also available (call endpoints directly in the app)

### SQLite Utils

> Could be really handy for testing/preparing data!
> Perhaps populate a demo database automatically?

[SQLite Utils](https://sqlite-utils.datasette.io) has a lot of helpful functions for formatting data from `json`, `csv`, and `.db` SQLite files. For example, you have a [Tally Form](https://tally.so/) that exports as `.csv` ...

```terminal
-- Activate the virtual environment
> activate

-- Install the python package and CLI
> uv add sqlite-utils

-- Output a list of `json` dictionaries (one for each entry)
-- Add `| python -m json.tool` to pretty print the `json`
sqlite-utils memory event.csv "select * from event"
```

And you could could generate a database from the `json` or [`.csv`](https://alexwlchan.net/til/2024/use-sqlite-utils-to-convert-csv-to-sqlite/)! Or input the values with your own schema design.

### Other tools

- [JQ](https://jqlang.org/) is handy for manipulating `json` data
    - Eg: convert `{ list: [] }` -> `[]` (similar to Elm's `Decoder.at`)
[JSON Server](https://marketplace.visualstudio.com/items?itemName=sarthikbhat.json-server) for VS Code (great for mocking)


## SQLite

> How to manage database migrations?
> How to avoid locked database "connection already open"?

SQLite should be set to `STRICT TABLES`, `PRAGMA journal_mode=WAL`, `PRAGMA foreign_keys = ON`. You can also use `user_version` for migrations.

**⚠️ The only problem with Piccolo is there's no PRAGMA settings available** so we have to be extra careful with our Pydantic models and verify data before inserting or updating. Piccolo should respect `NULL` values and foreign keys and you might want to set the timeout for SQLite. In general Piccolo and a lot of ORMs tend to prefer (or have more options for) Postgres.

You could use a tool like [Alembic](https://alembic.sqlalchemy.org) to migrate changes in the database `.schema`, but it's probably a good idea to know how to do this manually. SQLite Utils also has `sqlite-migrate` for simple migrations. I'm sure there's plenty of databse tools too (such as [Enso](https://ensoanalytics.com/) or [Ai](https://medium.com/@timothyjosephcw/enhancing-data-migration-testing-with-ai-in-2024-454537440ab3)). Either way, it seems to be sensible to backup data, create a new (column, table) first; copy data over (from the old column); then drop the old column.

As always, practice with mock data first and be sure to back up! (demo/staging). It's likely better to think in terms of _small, incremental_ changes, rather than big bulk changes.

Database locking is [something to consider](https://piccolo-orm.readthedocs.io/en/1.3.2/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html) with Piccolo but so long as you don't combine read and writes within the same endpoint connection, it shouldn't be something to worry about.


## Hosting

> Be careful that your stack is compatible with FastAPI

- I think Python Anywhere hosts files over the network?[^7]
- [AGSI](https://help.pythonanywhere.com/pages/ASGICommandLine) setup in Python Anywhere is now possible (I think).
- You'll need to setup `uvicorn` to run with [`https`](https://www.uvicorn.org/deployment/#running-with-https)** (it's not default)
- You might want parts of your app as `.jinja` html, rather than `json` (such as a login form)[^8]

  
[^1]: If you're a great programmer, or don't mind suffering through the pain of low-level learning, then do it yourself. My goals are quite distinct and I simply don't have the time to learn everything.

[^2]: Which is a shame, because I like PeeWee's documentation and syntax. It'd be perfect for apps where there's not going to be (any/many) concurrent writes to the database.

[^3]: I tried and failed to get MongoDB working. I found it an absolute arse to setup (especially for beginners) and more hassle than SQLite (or even Postgres, I imagine). The book's `chapters` from `_06/` or `_07/` onwards uses MongoDB; I decided to part ways with the book and use SQLite instead.

[^4]: With a `json` server, this separation of concerns between frontend and backend could be slightly easier to maintain.

[^5]: Joins are easier to maintain than lists. In the book, the latter chapters use MongoDB, which is unstructured data. Here, we're trying to keep data atomic and [normalised](https://youtube.com/watch?v=GFQaEYEc8_8) with SQLite, so it's easier to search for (and `JOIN user ON event.creator = user.id`) later.

[^6]: I found Postman to be too complicated for my taste.

[^7]: See [`WAL`](https://sqlite.org/wal.html) for SQLite: "All processes using a database must be on the same host computer; WAL does not work over a network filesystem"

[^8]: Jinja code adds quite a bit of complexity to your API code. It's great for small chunks of html, but for complex forms and UI could be a liability. You could also consider [htmx](https://htmx.org) for static code.
