# README

> A [brief overview](https://lyz-code.github.io/blue-book/fastapi/) of FastApi
> For prototyping, keep things simple, get a professional to check your code ...
> and delegate the hard stuff if you're not comfortable with it.

FastApi is a decent `http` server that's quick (other languages are faster). The book uses MongoDB in later chapters, but I found it uncomfortable and painful to setup and use. For that reason, I prefer SQLite.

## The programming style

I'm not a fan of the Python style however; the FastApi (or SQLModel) documentation can be longwinded, at times unclear, a bit complicated to figure out how to get things done. Going from [an article like this](https://fastapi.tiangolo.com/tutorial/security/get-current-user/), understanding the types, grasping it's component parts (inputs, outputs, dependency functions) and migrating that code to a version using SQLModel is confusing to me. The fact SQLModel is an abstraction of an abstraction (SQLAlchemy) is also worrying.

The FastApi book is a good high-level view, but has many errors and continuity issues, so you'll have to fix things and check documentation. It's also fast becoming outdated (dependency hell) as FastApi evolves, so watch out for changes and updates. Authentication is easy(ish) to use (with guidance) but email notifications aren't baked in, and other nice-to-haves can be difficult.

### Black box

> I prefer to treat parts of this http server as a "black box".
> That is to say, areas where I don't have to understand how it works!

Some things can be set-and-forget. They involve a lot of domain knowledge and low-level detail, which I'm personally not 100% comfortable with. It's wise to find an experienced developer to mentor you and double-check code.

`/auth`, `/database` modules are especially important to get right!

### Errors

> Compared to Elm, Python's error messaging is AWFUL.

Python error messaging is particularly frustrating (cryptic, verbose, incomplete), but you can use Pydantic and Pyright to help out with types.

### Limitations

> "SQLModel is designed to have the best developer experience in a narrow set of very common use cases."

For that reason, you might find yourself better off with a different ORM. SQLAlchemy is too complicated for my preferences, so I'd plum for something which is easier and as close to SQL as possible. [Peewee](https://docs.peewee-orm.com/en/latest/index.html) seems to fit this bill.


## Setting yourself boundaries

> Have a clear goal, a clear learning frame
> Use [BORING technology](https://boringtechnology.club/) wherever possible!

I think it's wise to provide yourself **a clear learning frame**, by which I mean **drawing a clear line between what you're prepared to learn, and what you're not**. For example, getting a working and reliable email confirmation script is non-trivial!

Personally, I'd prefer someone else to handle things like that, so unless there's a well-documented and stable plugin, I'm going to hire a professional. **I prefer things as simple as possible;** SQLite and FastApi routes are easy enough to understand the basics, but there can be a lot of moving parts! There's many ways to build out your app architecture, and I'm not sure there's a book out there that covers the best way to do things for _your_ app.

There's so much to learn with programming it's good to set your own boundaries!


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
7. Securing FastApi applications (1.11.0 — 1.11.9)
    - Hash and compare passwords
    - Generating JWT tokens
    - Securing routes (with authentication)
    - CORS policy (middleware)
8. Testing (1.12.0 - ...)


## Helful Commands

1. `uv run uvicorn api:app --port 8000 --reload` (or run from `.venv`)
2. `uv run main.py` (if you've setup properly `__main__.py`)
    - Or, `fastapi dev main.py` (seems to essentially be the same)
3. `uv run pyright main.py` (run in strict mode, Pylance in VS Code)

```terminal
curl -X 'POST' \                                        
  'http://localhost:8000/user/signin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=[email]&password=[password]&scope=&client_id=string&client_secret=string'
```

```sql
-- Chapter 07 code
SELECT u.email, e.title FROM user AS u
JOIN event AS e ON u.email = e.creator; -- inner join
```

## Your API is self-documenting (but use Bruno anyway)

> `/docs` gives a JSON Schema documentation ...
> `/redoc` provides alternative documentation.

To implement these properly leads to messy code! Things like `Annotated[]`, `"json_schema_extra"` metadata, and so on. I'm finding that Bruno is pretty nice to work with (as an alternative) and does most of what I'd need.


## Silly errors (and things that don't work)

> **The SQLModel documentation [isn't always great](https://github.com/badlydrawnrob/elm-playground/issues/45)**, and some things that should be easy enough, don't seem to be. Elm Lang is way better than Python for error messages. Python can be cryptic and hard to track down. It's also not as easy to use the REPL for "practice" or "discovery" with the SQLModel setup.

1. **`:id` not added** to the Bruno path parameters (getting `method not allowed`)
2. **`count()`** fails hard: the alternative is [`first()`](https://sqlmodel.tiangolo.com/tutorial/one/) with SQLModel


## Errata

> **The major rule for writing is ... BE CONSISTENT!**
> - There's a lot of small mistakes and continuity errors ...
> - So use ⚠️ `#!` style comments for major breaking code!
> - A single source of truth for code (edits break things)

For example, pg.131:

1. `NewUser` model is mentioned but not created
2. `User` fields are not yet used
3. `User.username` is used (`curl` example) but not created
4. `users.py` is referred to as `user.py`

Also 

1. Make sure any required dependencies are introduced clearly!
    - `SQLModel` is imported, but no download is mentioned.
    - `jose` has the same problem. Which `jose` package do you mean?!
2. Some "upgrades", such as ~~`@app.on_event("startup")`~~ take time to learn
    - The app lifecycle, for example, requires [understanding](https://github.com/PacktPublishing/Building-Python-Web-APIs-with-FastAPI/issues/12#issue-2843134599) of `contextlib`.
3. `grant_type=` missing the `password` keyword in the authentication curl call.


## Tools

You're going to need the following:

### Python

- [Pydantic](https://pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [VS Code Python plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [PyRight](https://microsoft.github.io/pyright/) (CLI in [strict mode](https://github.com/jackgene/reactive-word-cloud-python/blob/b48306f94e1038c26c7c70ab56337ab26fa2b719/pyproject.toml#L21-L23), Pylance in VS Code)
- [ORM](https://sqlmodel.tiangolo.com/) of some description
    - Be extra careful with [raw SQL](https://www.youtube.com/watch?v=Cp3bXHYp-bY).

### [Bruno](https://www.usebruno.com/)

> A great API test kit for Mac.
> Much simpler than the alternatives (IMO)

The only _downsides_ to using Bruno is **you've got to manually write your documentation and tests**. FastApi comes with `/docs` and `/redoc` which are pretty handy, but I prefer Bruno's way of writing documentation. Doing things in Bruno means we can easily switch to a different API framework and keep all our tests in place.

- **[Use OAuth2](https://docs.usebruno.com/auth/oauth2/overview) with Bruno**
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

FastApi doesn't come with data migration, so it might be wise to do this manually with SQLite, or find a solid tool (or Ai) to help you. [Alembic](https://alembic.sqlalchemy.org/) seems a bit difficult. In general the advice seems to be create new (column, table) and copy data over (from old column) before dropping the old. Practice on a dummy database first, and always backup first!!

- Change the [`user version`](https://stackoverflow.com/a/998652)
- Use [ORM tools](https://docs.peewee-orm.com/en/2.10.2/peewee/playhouse.html#migrate) if you prefer
- GUIs like [Enso](https://ensoanalytics.com/) or [Ai](https://medium.com/@timothyjosephcw/enhancing-data-migration-testing-with-ai-in-2024-454537440ab3) might be helpful too!


## Paradigms

> I really don't want to use Python's OOP style very much.
> The book is a bit sloppy in places with conflicting instructions.
> Elm Lang just "feels" nicer: documentation, error messaging, and so on.

1. **`json` is preferrable to `.jinja`** (at scale)[^4] (just use Elm?)
2. **Try to avoid Python "magic"** that isn't transferable
    - Features like `@classmethod`, `response_model=` are handy but not portable
3. **Aim to keep your models, SQL, data, and code as simple as possible**
    - [Pydantic documentation](https://docs.pydantic.dev/latest/) is kind of narly and confusing. Some examples in the book are (already) outdated.
    - If you're unsure about something, possibly best to leave it out.
4. **Is it wise to use `SQLModel` classes for request body?**
    - Search `"using fastapi SQLModel as request body"` on Brave browser ...
    - Understand if it's wiser to use `BaseModel` for your request body (and separate concerns).
    - `SQLModel` is only usable if all fields in request body are provided (other than `Optional` ones). These seems suboptimal if user preferences _requires_ many fields!! Perhaps this could be handled client-side (enforce non-optional fields)?
4. For `status_code=` the book uses `status.HTTP_403_FORBIDDEN` but I'm just using the `403` code by itself, as it's cleaner. This is debatable.
5. `Depends()` is an important function that injects dependencies into our routes,
forcing our route to handle something (such as `oauth3_scheme`) first.
6. [Why use `response_model=`](https://github.com/fastapi/fastapi/discussions/8247) instead of a response type?
7. Are Pydantic types really necessary? (It depends)
8. Do you want to tightly couple your API models with your SQL model? (probably NO!)


## Elm -vs- Python

Whereas Elm has a central `Model` (generally) to work from and uses modules and functions, Python has instances of classes which (I think) are stateful. It feels like Python adds a whole lot of mess to the code base.

A good example of this is FastAPI allows [generating API examples](https://tinyurl.com/fastapi-json-schema-extra) along with your models. I feel the model and **examples should be handled separately**, as the code becomes messy. Better to let Bruno handle the documentation (and use `/docs` as-is), rather than this:

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
