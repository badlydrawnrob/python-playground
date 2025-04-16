# README

> This repo is my working copy of the book [Building Python APIs with FastAPI](https://www.packtpub.com/en-us/product/building-python-web-apis-with-fastapi-9781801074513)

The book goes into detail on building a http server API with the [FastAPI](https://fastapi.tiangolo.com/). In general it's a good book, but there's a lot of errors, or areas where you've got to interpret and fix things for yourself. FastAPI has also made a lot of changes since the book was published (dependency hell). It actually took me quite a bit of time (months) to get through, as I had to re-familiarise myself with Python, and FastAPI isn't always obvious.

As I've written before, I'm [not a huge fan](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style) of Python, but it's a handy scripting language and you get used to it.


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
> Use the REPL to practice and discovery functionality quickly!

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
    - A partially finished PeeWee version (instead of SQLModel) (`1.12.9`)
    - Reverting to a different ORM (`...`, see ORMs below)


## Commands

> [Some notes](https://github.com/astral-sh/uv/issues/10543#issuecomment-2587276856) on getting setup with `uv` and `venv`

```terminal
-- Create a new project
uv init
-- Run your program
uv run main.py
```
  

## Keeping things simple
### The 5 finger rule

> The 5 finger rule is a bit like reading for kids. How much of it do I understand?

1. **Keep things as simple as possible.**
    - Your models, documentation, tooling, dependencies, etc.
    - Actively remove code and simplify processes where possible.
2. **If things are too complicated for you, hire.**[^3]
    - Have a professional look over your code ...
    - Or, have them do it for you, and treat things as a [black box](#!black-box).
    - Stick to a narrow problem set that suits your capabilities.
3. **Pick tools where you understand 50-70% of the language.**
    - The 5 finger rule means avoiding texts that are too difficult for you.
4. **You don't have to understand everything ...**
    - It just needs to work. Write working code first, worry about it later.
5. **Try to stick to your [preferred coding style](https://github.com/badlydrawnrob/python-playground?tab=readme-ov-file#coding-style).**
    - My background is Elm (Haskell-like) and I don't want to learn Pythonic code.
    - So `Class.methods`, `@decorators`, so on, use only when necessary.
    - Learn a subset of Python unless you write a lot of it. Be functional.


## Choosing an ORM

> SQLModel is fine for single table `select()`s but a bit confusing for joins.

You might want to stick with SQLModel but there's a few reasons you might not:

1. It could be better to separate concerns:
    - To split the API layer from the DATA layer (models)
2. I didn't find the SQLModel documentation easy to query joins:
    - It's not very intuitive.
3. It's an abstraction of an abstraction:
    - It's built on top of SQLAlchemy, which I find too big and complicated.
4. There's better ORMs with more functionality and great documentation:
    - But beware that FastAPI is `async` and requires async tooling

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

> If I was using an non-async framework, I'd pick [PeeWee](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html) or [Pony](https://docs.ponyorm.org/). The main [problem with `async`](https://fastapi.tiangolo.com/async/#asynchronous-code) is having to [scatter your app](https://charlesleifer.com/blog/asyncio/) with `await` calls.

1. **Picallo** is great, but [not 100% async](https://piccolo-orm.readthedocs.io/en/1.1.1/piccolo/tutorials/using_sqlite_and_asyncio_effectively.html)
2. **[Ormar](https://collerek.github.io/ormar/latest/)** works with SQLite async, but less mature than Picallo (at time of writing)
3. **Tortoise ORM** (feels a bit clunky to me, see [this example](https://tortoise.github.io/examples/fastapi.html))
4. **[SQLmodel](https://sqlmodel.tiangolo.com/)** is the obvious option for FastAPI, but I'm not a huge fan.
5. [IceAxe](https://github.com/piercefreeman/iceaxe) is also very interesting to me, but it's only Postgres. I like it's simplicity and similarity to raw SQL.

I'm sure there's more (or will be) but these seem a good fit. Also see Reddit's "[What is your go-to ORM?](https://www.reddit.com/r/FastAPI/comments/1fjta2e/what_is_your_goto_orm/)". The alternative to using asyncio is to choose [boring](https://mcfunley.com/choose-boring-technology) technology, and simplify your stack ([PeeWee](https://docs.peewee-orm.com/en/latest/peewee/quickstart.html) and any compatible [framework](https://docs.peewee-orm.com/en/latest/peewee/database.html#framework-integration)!)

### A (better?) language?

The nuclear option is to ditch Python completely, and pick a different language. [Ocaml](https://aantron.github.io/dream/), [Elixir](https://phoenixframework.org/), [Roc](https://github.com/roc-lang/basic-webserver), or any other statically typed functional language.

Alas, you're looking at 2-3 months to change tools, so just get something out there and worry about that later. Don't over optimise before you've proven your business model!







  
[^1]: Which is a shame, because I like PeeWee's documentation and syntax. It'd be perfect for apps where there's not going to be (any/many) concurrent writes to the database.

[^2]: I tried and failed to get MongoDB working. I found it an absolute arse to setup (especially for beginners) and more hassle than SQLite (or even Postgres, I imagine). The book's `chapters` from `_06/` or `_07/` onwards uses MongoDB; I decided to part ways with the book and use SQLite instead.

[^3]: If you're a great programmer, or don't mind suffering through the pain of low-level learning, then do it yourself. My goals are quite distinct and I simply don't have the time to learn everything.
