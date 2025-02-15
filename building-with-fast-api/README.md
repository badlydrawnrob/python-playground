# README

> A [brief overview](https://lyz-code.github.io/blue-book/fastapi/) of FastApi


## Learning method

> Coding in the [age of Ai](https://github.com/badlydrawnrob/anki/issues/92)
> Watch out for Ai hallucinations!

1. Copilot and ChatGPT (it works!)
2. **Ai generated flashcards** (human in the loop)
3. **Memorable examples (storify)**
4. **Readability** (simple language, <s>academic writing</s>)
    - Personally I find code hard to read at scale ...
    - Or when each function has lots going on (multi-coloured!)
5. **RRReduce the amount you learn** (or teach)
    - **The Python learning journey is f* endless ...**
    - Some things can be "they just are" without asking WHY.
    - Stay in the shallows? Deep dive? It depends.

Limit Ai to give a fun example of the code (block), with a view to create cards later, as well as clarifying things as a study partner. My general process is: read, make notes (per chapter), condense notes, generate flashcards, files and programs. Creating a small series of books could come later.

"Give me a fun example for scaffolded learning on ____"
"Give it to me as [draw!, missing, simple] data"

It's safe to say I'm not comfortable with backend and servers, so I want my experience and pleasant and simple as possible. SQLite is reasonable simple to use.


## Chapters

> [Some notes](https://github.com/astral-sh/uv/issues/10543#issuecomment-2587276856) on using `uv` and `venv` setup[^1]

1. Hello World
2. Routing (1.6.0 — 1.6.6)
3. Response models and error handling (1.7.0 — 1.7.4)
4. Templating with Jinja (1.8.0 — 1.8.2)
    — **1.8.1** for `json` version
5. Structuring FastApi applications (1.9.0 — 1.9.1)
6. Working with the database
    - SQLModel (1.10.0 — 1.10.6)
    - ~~MongoDB~~[^2] (I'm sticking with SQLite)


## Silly errors
### And things that don't work

> With SQLModel, some things that should be easy don't seem to be.

1. **`:id` not added** to the Bruno path parameters (getting `method not allowed`)
2. **`count()`** fails hard: the alternative is [`first()`](https://sqlmodel.tiangolo.com/tutorial/one/) with SQLModel


## Commands

1. `uv run uvicorn api:app --port 8000 --reload` (or run from `.venv`)
2. `uv run main.py` (if you've setup properly `__main__.py`)


## Errata

> **The major rule is to always BE CONSISTENT!**
> There's a lot of small mistakes and continuity errors ...
> So use ⚠️ `#!` style comments for major breaking code! 

For example, pg.131:

1. `NewUser` model is mentioned but not created
2. `User` fields are not yet used
3. `User.username` is used (`curl` example) but not created
4. `users.py` is referred to as `user.py`

Also 

1. Make sure any required dependencies are introduced clearly!
    - `SQLModel` is imported, but no download is mentioned.
2. Some "upgrades", such as ~~`@app.on_event("startup")`~~ take time to learn
    - The app lifecycle, for example, requires [understanding](https://github.com/PacktPublishing/Building-Python-Web-APIs-with-FastAPI/issues/12#issue-2843134599) of `contextlib`.


## Tools

You're going to need the following:

### Python

- [Pydantic](https://pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [VS Code Python plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [MyPy](https://mypy-lang.org/) (optional, runs slowly)

### [Bruno](https://www.usebruno.com/)

> A great API test kit for Mac.
> Much simpler than the alternatives (IMO)

The only _downsides_ to using Bruno is **you've got to manually write your documentation and tests**. FastApi comes with `/docs` and `/redoc` which are pretty handy, but the API testing isn't as nice. However, doing things in Bruno means we can easily switch to a different API framework and keep all our tests in place.

- Import `openapi.json` to a new collection

[Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client), [Postman](https://www.postman.com/)[^3], and [Insomnia](https://insomnia.rest/) are other options.

### SQLite

> My general opinion is:
> - Simple is better
> - Smaller is better
> - Less is better (dependencies)
> - Human readable is better (docs)
> - Boring is better (in general, stable)

1. How do I generate [`UUID`](https://iifx.dev/en/articles/101721447)s (and what about performance?)
2. How do I load secrets and [environment variables](https://stackoverflow.com/a/45267398)? with [Pydantic](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage)?
    - I think SQLite setup is a lot easier than Postgres
3. Is async desirable with SQLite? (NEVER pre-optimise, wait until there's a need)
    - The package is now deprecated, but there are 3rd party tools available.
    - You might also be better off with RabbitMQ or some other queuing/sharding.
4. Why would I use [Peewee over SQLAlchemy](https://www.reddit.com/r/Python/comments/4tnqai/comment/d5jyuug/) or SQLModel?

#### How do I do database migrations?

> Possibly better to do data migrations simply and often?
> Also may have to consider the `json` and client code (w/ business logic)
> Also handy is `user_version` which you can do [like this](https://github.com/sqlitebrowser/sqlitebrowser/issues/366).

- For simple changes, consider [manually migrating](https://stackoverflow.com/a/998652)
- You can also use [ORM tools](https://docs.peewee-orm.com/en/2.10.2/peewee/playhouse.html#migrate) or something like [alembic](https://alembic.sqlalchemy.org/en/latest/) (depending on what ORM you're using)
- GUIs like [Enso](https://ensoanalytics.com/) or [Ai](https://medium.com/@timothyjosephcw/enhancing-data-migration-testing-with-ai-in-2024-454537440ab3) might be helpful too!


## Paradigms

> I really don't want to use Python's OOP style very much.
> The book is a bit sloppy in places with conflicting instructions.

1. `json` is preferrable to `.jinja` (at scale)[^4] (just use Elm?)
2. Try to avoid "magic" Python that isn't transferable
    - Features like `@classmethod`, `response_model=` are handy but not portable
3. Aim to keep your models, SQL, data, and code as simple as possible
    - If you're unsure about something, possibly best to leave it out.


## Elm -vs- Python

Whereas Elm has a central `Model` (generally) to work from and uses modules and functions, Python has instances of classes which (I think) are stateful. It feels like Python adds a whole lot of mess to the code base.

A good example of this is FastAPI allows [generating API examples](https://tinyurl.com/fastapi-json-schema-extra) along with your models. I feel the model and **examples should be handled separately**, and Bruno does this perfectly:

```python
class ToDo(BaseModel):
    id: int
    item: Item

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "item": {
                        "item": "Grab some shopping for dinner",
                        "status": "to-do"
                    }
                }
            ]
        }
    }
```

### Self documentation

> `/docs` gives a JSON Schema documentation ...

But to implement it looks like messy code. Things like `Annotated[]`, `"json_schema_extra"`, and so on. I'm finding that Bruno is pretty nice to work (as an alternative) with and does most of what I'd need.


## Problems

> These are annoying and compared to Elm (where everything just works), not particularly user-friendly. You'd think you could just run commands once you're set up with a `venv` (virtual environment).

1. **Dot notation: how are values extracted?**
    - `dictionary.id` rather than `dictionary["id"]`
2. Module naming clashes and `venv`:**
    - `uv` commands require calling from the `venv` parent directory
    - `01` numbers cannot come first for module naming (`name_01` is ok)
3. **`uvicorn` command [won't run](https://stackoverflow.com/a/69322150)**
    - Preface it with `uv run` (equivalent to `python -m`)
    - Or, make sure you've `source .venv/bin/activate`d your environment
    - Also take care with modules, folders, and names.[^5]
4. **`uvicorn` doesn't [allow secure `https`](https://www.uvicorn.org/deployment/#running-with-https)** (by default)
5. Using Thonny as an IDE
    - I can get the version of Python running but the other stuff is harder
6. You might want to return `html` instead of `json`. You can [do both](https://tinyurl.com/fastapi-return-html-or-json)!


## Hosting

- [AGSI](https://help.pythonanywhere.com/pages/ASGICommandLine) setup in Python Anywhere


[^1]: "I would not recommend using directory names in `.python-version` files or using a custom virtual environment name in a project."

[^2]: MongoDB is a an arse to setup (especially for beginners), more hassle than SQLite (and possibly Postgres easier also). The code in chapters `06`/`07` and above also starts to get Pythonic (class methods rather than functional style) and I see diminishing returns from learning in the MongoDB style.

[^3]: I find Postman too flippin' complicated to use. Insomnia is another option.

[^4]: `jinja` code adds a bit more complexity to your API code. Seems great for small setups but could prove a liability with complicated forms and UI. For now, handle most of the complexity with Elm lang and look into HTMX or static site generators for blog posts and FAQs. Possibly handle `User` admin with FastApi.

[^5]: There's two ways to do this. Either call `uvicorn subfolder.file:app` and make sure your modules use `from subfolder.file` names, OR `cd` into the correct folder and run Uvicorn from there!
