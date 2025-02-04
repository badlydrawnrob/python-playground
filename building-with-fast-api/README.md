# README

> A [brief overview](https://lyz-code.github.io/blue-book/fastapi/) of FastApi


## Learning method

> Coding in the [age of Ai](https://github.com/badlydrawnrob/anki/issues/92)
> Watch out for Ai hallucinations!

1. Copilot and ChatGPT (it works!)
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
3. Response models and error handling (1.7.0 — 1.7.4)
4. Templating with Jinja (1.8.0 — 1.8.2)
    — **1.8.1** for `json` version.
5. Structuring FastApi applications


## Commands

1. `uv run uvicorn api:app --port 8000 --reload` (or run from `.venv`)


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

[Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client), [Postman](https://www.postman.com/)[^3], and [Insomnia](https://insomnia.rest/) are other options.


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
    - Also take care with modules, folders, and names.[^2]
4. **`uvicorn` doesn't [allow secure `https`](https://www.uvicorn.org/deployment/#running-with-https)** (by default)
5. Using Thonny as an IDE
    - I can get the version of Python running but the other stuff is harder
6. You might want to return `html` instead of `json`. You can [do both](https://tinyurl.com/fastapi-return-html-or-json)!


## Hosting

- [AGSI](https://help.pythonanywhere.com/pages/ASGICommandLine) setup in Python Anywhere


[^1]: "I would not recommend using directory names in `.python-version` files or using a custom virtual environment name in a project."

[^2]: There's two ways to do this. Either call `uvicorn subfolder.file:app` and make sure your modules use `from subfolder.file` names, OR `cd` into the correct folder and run Uvicorn from there!

[^3]: I find Postman too flippin' complicated to use. Insomnia is another option.

[^4]: `jinja` code adds a bit more complexity to your API code. Seems great for small setups but could prove a liability with complicated forms and UI. For now, handle most of the complexity with Elm lang and look into HTMX or static site generators for blog posts and FAQs. Possibly handle `User` admin with FastApi.
