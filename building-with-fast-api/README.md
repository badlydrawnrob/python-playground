# README

## Paradigms

> I really don't understand Python's OOP style very much.

Whereas Elm has a central `Model` (generally) to work from and uses modules and functions, Python has instances of classes which (I think) are stateful.

## Problems

> These are annoying and compared to Elm (where everything just works), not particularly user-friendly. You'd think you could just run commands once you're set up with a `venv` (virtual environment).

1. `uvicorn` command [won't run](https://stackoverflow.com/a/69322150)
    - Preface it with `uv run` (equivalent to `python -m`)
2. Using Thonny as an IDE
    - I can get the version of Python running but the other stuff is harder

## Tools

You're going to need the following:

- An API test kit (such as [Bruno](https://www.usebruno.com/) or [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client))[^1]


[^1]: I find Postman too flippin' complicated to use. Insomnia is another option.
