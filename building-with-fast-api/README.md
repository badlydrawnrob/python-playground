# README

> A [brief overview](https://lyz-code.github.io/blue-book/fastapi/) of FastApi

## Chapters

> [Some notes](https://github.com/astral-sh/uv/issues/10543#issuecomment-2587276856) on using `uv` and `venv` setup[^1]

1. Hello World
2. Routing (1.6.0 — ...)


## Paradigms

> I really don't understand Python's OOP style very much.
> The book is a bit sloppy in places with conflicting instructions.

Whereas Elm has a central `Model` (generally) to work from and uses modules and functions, Python has instances of classes which (I think) are stateful.


## Commands

1. `uv run uvicorn api:app --port 8000 --reload` (or run from `.venv`)


## Problems

> These are annoying and compared to Elm (where everything just works), not particularly user-friendly. You'd think you could just run commands once you're set up with a `venv` (virtual environment).

1. **Module naming clashes and `venv`:**
    - `uv` commands require calling from the `venv` parent directory
    - `01` numbers cannot come first for module naming (`name_01` is ok)
2. **`uvicorn` command [won't run](https://stackoverflow.com/a/69322150)**
    - Preface it with `uv run` (equivalent to `python -m`)
    - Or, make sure you've `source .venv/bin/activate`d your environment
    - Also take care with modules, folders, and names.[^2]
3. **`uvicorn` doesn't [allow secure `https`](https://www.uvicorn.org/deployment/#running-with-https)** (by default)
4. Using Thonny as an IDE
    - I can get the version of Python running but the other stuff is harder


## Tools

You're going to need the following:

- An API test kit (such as [Bruno](https://www.usebruno.com/) or [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client))[^3]


## Hosting

- [AGSI](https://help.pythonanywhere.com/pages/ASGICommandLine) setup in Python Anywhere


[^1]: "I would not recommend using directory names in `.python-version` files or using a custom virtual environment name in a project."

[^2]: There's two ways to do this. Either call `uvicorn subfolder.file:app` and make sure your modules use `from subfolder.file` names, OR `cd` into the correct folder and run Uvicorn from there!

[^3]: I find Postman too flippin' complicated to use. Insomnia is another option.
