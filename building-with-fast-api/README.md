# README

> This repo is my working copy of the book [Building Python APIs with FastAPI](https://www.packtpub.com/en-us/product/building-python-web-apis-with-fastapi-9781801074513)

**The book goes into detail on building a http server API with the [FastAPI](https://fastapi.tiangolo.com/).** In general it's a good book, but there's a lot of errors, or areas where you've got to interpret and fix things for yourself. FastAPI has also made a lot of changes since the book was published (dependency hell). It actually took me quite a bit of time (months) to get through, as I had to re-familiarise myself with Python, and FastAPI isn't always obvious.

As I've written before, I'm [not a huge fan](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style) of Python, but it's a handy scripting language and you get used to it. Errors and typing are _especially_ annoying — a simple typo, missing word, or rogue piece of code can torpedo your program and be _extremely_ difficult to track down with FastAPI and Python.


## My learning goals

> I'm always a fan of simplicity.

1. Simple is better
2. Smaller is better
3. Less is better (be brutalist!)
4. Human readable is better (documentation)
5. Boring is better! (aim for stability)

**If I can handle 3k users on a simple server, I'm happy.** I'm not out to build an all-singing, all-dancing app, and the goal is to validate a business model, then build out a technical team if it's successful! Things like queuing, sharding, email validation, and so on, are not my concern right now.

- **My learning frame** is a personal "do" and "don't do" list
- **Things I'm happy to take on (and learn);** stuff I don't add to my to-do list.

Learning to program is a _never-ending_ task. It can be quite overwhelming, so having a mentor to hold your hand and keep you right is super helpful. I don't enjoy low-level detail![^7]


## FastAPI pros and cons

> It seems quick, as advertised, but remember it's `async`!

1. It's `async`, for `async` tools.
    - An ORM like PeeWee [does not play nicely](https://github.com/fastapi/fastapi/discussions/8049) with it![^1]
2. It works well with SQLite.[^2] The beauty of SQLite as that it involves minimal production setup. It's just a file!
    - SQLite doesn't default to `async`. To add support, you'll need an ORM that supports [this package](https://github.com/omnilib/aiosqlite).

The downsides ...

1. Sometimes FastAPI documentation is not clear enough.
    - I'm not keen on combining SQL knowledge with SQLModel documentation.
    - It makes it way harder to scan the docs for query syntax, often longwinded.
2. Python error messages are shit. See "[coding style](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style)". Pydantic, PyLance, and PyRight help a bit with typing.
    - Long traceback error messages (often, but not always the last one tells the problem)
    - Cryptic errors and hard to pin down what's wrong


## Chapters

> The tags relate to important stages in our app's development ...
> Use the REPL to practice and discover functionality quickly!

1. Hello World
2. Routing (`1.60` — `1.6.6`)
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
8. Testing (`1.12.0` - ...)
    - Original version with SQLModel for database (`1.12.4`)
    - A partially finished PeeWee version (instead of SQLModel) (`1.12.10`)
    - Reverting to a different ORM (`...`, see ORMs below)


## Errata

> The book has quite a lot of errors ...
> And make sure your routes are properly formatted!

Here are a few I caught (there's more)

1. `NewUser` model is mentioned but not created
2. `User` fields are not yet used (`List Int`)
3. `users.py` is referred to as `user.py`

Also:

1. Make sure any required dependencies are introduced clearly!
    - `SQLModel` is imported but no download is mentioned
    - Which `jose` package do you mean? There's more than one in pypi!
2. Some upgrades are needed, but tricky to learn:
    - ~~`@app.on_event("startup")`~~ is now app lifecycle but requires an understanding of `contextlib`.
3. `grant_type=` missing the `password` keyword in the authentication `curl` call.

Be careful with your routes:

- `:id` (params) must be added to your Bruno path


## Commands

> [Some notes](https://github.com/astral-sh/uv/issues/10543#issuecomment-2587276856) on getting setup with `uv` and `venv`

```terminal
-- Create a new project
uv init
-- Run your program (from function)
uv run uvicorn api:app -- port 8000 --reload
-- Run your program (from file)
uv run main.py
-- Test types and errors
uv run pyright main.py
```

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

```sql
-- Chapter 07 code
SELECT u.email, e.title FROM user AS u
JOIN event AS e ON u.email = e.creator;
```

```python
# Inspect an object's properties
from pprint import pprint
pprint(vars(your_object))
```


## Keeping things simple
### The 5 finger rule

> The 5 finger rule is a bit like reading for kids. How much of it do I understand?

1. **Keep things as simple as possible.**
    - Your models, documentation, tooling, dependencies, etc.
    - Actively remove code and simplify processes where possible.
    - `.jinja` at scale can get messy, why not try Elm?[^3]
    - You might want to split your API layer from your DATA layer.
2. **If things are too complicated for you, hire.**[^4]
    - Have a professional look over your code ...
    - Or, have them do it for you, and treat things as a [black box](#a-black-box).
    - Stick to a narrow problem set that suits your capabilities.
3. **Pick tools where you understand 50-70% of the language.**
    - The 5 finger rule means avoiding texts that are too difficult for you.
4. **You don't have to understand everything ...**
    - It just needs to work. Write working code first, worry about it later.
5. **Try to stick to your [preferred coding style](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style).**
    - My background is Elm (Haskell-like) and I don't want to learn Pythonic code.
    - So `Class.methods`, `@decorators`, so on, use only when necessary.
    - Learn a subset of Python unless you write a lot of it. Be functional.


## A black box

> Some things can be set-and-forget.
> There's simply too much to learn with programming!

Some things I want to treat as an input and output: I don't want to worry about their internal mechanisms.

1. I don't want to learn some things (my learning frame)
2. I'd rather hand over a low-level task to a collegue (email validation)
3. `auth` and `database` are super important to get right (I don't trust myself)


## The user experience (UI)

> Remember the last time you deleted something by accident, or refreshed the page and lost all your form data?

We're not worrying about it too much in this book, but it's worthwhile mentioning that a `DELETE` should notify the user: "Are you _sure_ you want to do that?", which is a _frontend_ problem. I've removed the `/delete` route in later chapters, as it's something that should _never_ happen unless you're an admin!

All API architecture should consider the end-user and their needs/experience. Consider also which data points should be _public_ and which _private_. It might be fine to expose an `Event.id` but a `User.id` is better private. A data scraper can easily increment the `Event.id` however, so maybe a `shortuuid` is better.


## Choosing an ORM

> SQLModel is fine for single table `select()`s but a bit confusing for joins.

You might want to stick with SQLModel but there's a few reasons you might not:

1. **It could be better to separate concerns:**
    - **To split the API layer from the DATA layer (models)**
2. I didn't find the SQLModel documentation easy to query joins:
    - It's not very intuitive.
3. It's an abstraction of an abstraction:
    - It's built on top of SQLAlchemy, which I find too big and complicated.
4. There's better ORMs with more functionality and great documentation:
    - But beware that FastAPI is `async` and requires async tooling

Below are ORMs that'll work well with FastAPI. Alternatively, you might like to check out [Bottle](https://bottlepy.org) or [Sanic](https://sanic.dev) (WGSI). They both work with PeeWee and have data validation (not sure about `auth/`).

### It's good to have a picking criteria

> How do I make a decision on which ORM to use?
> Backend is difficult, and there's a lot that can go wrong!

A bit similar to the [5 finger rule](#keeping-things-simple)!

1. I can understand 50-70% of it (won't take long to learn)
2. Feels like using regular SQL (a `join` looks like a join!)
3. The code examples don't confuse or scare me (not overly complex)
4. The documentation is non-academic and done well (written for humans!)
5. Has availability for [SQLite strict mode](https://sqlite.org/stricttables.html) and [or any other concern you'd like]
6. Google(able) and easy to search for [your particular requirement]
7. Stable, or at least exciting enough to risk breaking changes.

### A few options

> I'd pick [PeeWee](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html) or [Pony](https://docs.ponyorm.org/) for a non-async framework. The main [problem with `async`](https://fastapi.tiangolo.com/async/#asynchronous-code) is having to [scatter your app](https://charlesleifer.com/blog/asyncio/) with `await` calls.

1. **Picallo** is great, but [not 100% async](https://piccolo-orm.readthedocs.io/en/1.1.1/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html)
2. **[Ormar](https://collerek.github.io/ormar/latest/)** works with SQLite async, but less mature than Picallo (at time of writing)
3. **Tortoise ORM** (feels a bit clunky to me, see [this example](https://tortoise.github.io/examples/fastapi.html))
4. **[SQLmodel](https://sqlmodel.tiangolo.com/)** is the obvious option for FastAPI, but I'm not a huge fan.
5. [IceAxe](https://github.com/piercefreeman/iceaxe) is also very interesting to me, but it's only Postgres. I like it's simplicity and similarity to raw SQL.

I'm sure there's more (or will be) but these seem a good fit. Also see Reddit's "[What is your go-to ORM?](https://www.reddit.com/r/FastAPI/comments/1fjta2e/what_is_your_goto_orm/)". The alternative to using asyncio is to choose [boring](https://mcfunley.com/choose-boring-technology) technology, and simplify your stack ([PeeWee](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html) and any compatible [framework](https://docs.peewee-orm.com/en/latest/peewee/database.html#framework-integration)!)

### RAW SQL and JOINs

> I might want to handle database creation and migration manually?
> But have a representation of it with the `User` and `Event` models.

For read-only code, you might want to use raw SQL queries, but you'll still need to map the data onto your `User` class, or a `dict`ionary. In the book, we also create a `List[int]` of `Event.id`s — we don't really need these!! Only store data like this if your [app architecture](https://openlibrary.org/dev/docs/api/covers) depends on it.

OpenLibrary, for instance, has `List[int]` of images which map to a `/covers` route, with `-S`mall, `-M`edium, and `-L`arge images. Our API is NOT publically consumed, so we likely want to deal with SQL `join`s and serve the full image paths within the `Event` object.

Remember, any data point on your API must be called from the database and maintained. That means anytime a `User` adds/removes an `Event`, you'd have to add/remove from that `List`. Don't do it if it's not needed![^5]

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

- You can **setup Bruno with [OAuth2](https://docs.usebruno.com/auth/oauth2/overview)** in your collection settings.
- Import your `/docs -> openapi.json` to a new collection in Bruno.

### Other tools

- [SQLite Utils](https://sqlite-utils.datasette.io) is great for preparing data.
    - This could be a great way to automatically populate a demo database!
- [JSON Server](https://marketplace.visualstudio.com/items?itemName=sarthikbhat.json-server) for VS Code (great for mocking)


## SQLite

> How to manage database migrations?

SQLite should be set to `STRICT TABLES`, `PRAGMA journal_mode=WAL`, `PRAGMA foreign_keys = ON`. You can also use `user_version` for migrations.

You could use a tool like [Alembic](https://alembic.sqlalchemy.org) to migrate changes in the database `.schema`, but it's probably a good idea to know how to do this manually. SQLite Utils also has `sqlite-migrate` for simple migrations. I'm sure there's plenty of databse tools too (such as [Enso](https://ensoanalytics.com/) or [Ai](https://medium.com/@timothyjosephcw/enhancing-data-migration-testing-with-ai-in-2024-454537440ab3)). Either way, it seems to be sensible to backup data, create a new (column, table) first; copy data over (from the old column); then drop the old column.

As always, practice with mock data first and be sure to back up! (demo/staging). It's likely better to think in terms of _small, incremental_ changes, rather than big bulk changes.


## Hosting

> Be careful that your stack is compatible with FastAPI

- I think Python Anywhere hosts files over the network?[^7]
- [AGSI](https://help.pythonanywhere.com/pages/ASGICommandLine) setup in Python Anywhere is now possible (I think).
- You'll need to setup `uvicorn` to run with [`https`](https://www.uvicorn.org/deployment/#running-with-https)** (it's not default)
- You might want parts of your app as `.jinja` html, rather than `json` (such as a login form)[^7]

  
[^1]: Which is a shame, because I like PeeWee's documentation and syntax. It'd be perfect for apps where there's not going to be (any/many) concurrent writes to the database.

[^2]: I tried and failed to get MongoDB working. I found it an absolute arse to setup (especially for beginners) and more hassle than SQLite (or even Postgres, I imagine). The book's `chapters` from `_06/` or `_07/` onwards uses MongoDB; I decided to part ways with the book and use SQLite instead.

[^3]: With a `json` server, this separation of concerns between frontend and backend could be slightly easier to maintain.

[^4]: If you're a great programmer, or don't mind suffering through the pain of low-level learning, then do it yourself. My goals are quite distinct and I simply don't have the time to learn everything.

[^5]: Joins are easier to maintain than lists. In the book, the latter chapters use MongoDB, which is unstructured data. Here, we're trying to keep data atomic and [normalised](https://youtube.com/watch?v=GFQaEYEc8_8) with SQLite, so it's easier to search for (and `JOIN user ON event.creator = user.id`) later.

[^6]: I found Postman to be too complicated for my taste.

[^7]: See [`WAL`](https://sqlite.org/wal.html) for SQLite: "All processes using a database must be on the same host computer; WAL does not work over a network filesystem"

[^8]: Jinja code adds quite a bit of complexity to your API code. It's great for small chunks of html, but for complex forms and UI could be a liability. You could also consider [htmx](https://htmx.org) for static code.
