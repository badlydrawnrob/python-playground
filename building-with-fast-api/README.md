# README

> A [brief overview](https://lyz-code.github.io/blue-book/fastapi/) of FastApi


## Learning method

> Coding in the [age of Ai](https://github.com/badlydrawnrob/anki/issues/92)
> Watch out for Ai hallucinations!

1. Copilot and ChatGPT
2. Ai generated flashcards (human in the loop)
3. Memorable examples (storify)
4. Readability (simple language, <s>academic writing</s>)

Alongside my general process of: read, make notes (per chapter), condense notes, talk to your Ai study partner, generate flashcards, files or programs. For now, I'll limit the Ai to only giving me a fun example of the code (and not structuring the full Anki card's field data).

"Give me a fun example for scaffolded learning on ____"
"Give it to me as [draw!, missing, simple] data"


## Chapters

> [Some notes](https://github.com/astral-sh/uv/issues/10543#issuecomment-2587276856) on using `uv` and `venv` setup[^1]

1. Hello World
2. Routing (1.6.0 — 1.6.6)


## Paradigms

> I really don't understand Python's OOP style very much.
> The book is a bit sloppy in places with conflicting instructions.

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


## Commands

1. `uv run uvicorn api:app --port 8000 --reload` (or run from `.venv`)


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
    - Also take care with modules, folders, and names.[^2]
4. **`uvicorn` doesn't [allow secure `https`](https://www.uvicorn.org/deployment/#running-with-https)** (by default)
5. Using Thonny as an IDE
    - I can get the version of Python running but the other stuff is harder
6. You might want to return `html` instead of `json`. You can [do both](https://tinyurl.com/fastapi-return-html-or-json)!


## Tools

You're going to need the following:

- An API test kit (such as [Bruno](https://www.usebruno.com/) or [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client))[^3]


## Hosting

- [AGSI](https://help.pythonanywhere.com/pages/ASGICommandLine) setup in Python Anywhere


[^1]: "I would not recommend using directory names in `.python-version` files or using a custom virtual environment name in a project."

[^2]: There's two ways to do this. Either call `uvicorn subfolder.file:app` and make sure your modules use `from subfolder.file` names, OR `cd` into the correct folder and run Uvicorn from there!

[^3]: I find Postman too flippin' complicated to use. Insomnia is another option.
