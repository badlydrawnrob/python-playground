# README

> Looking back on these examples ... I feel Python is ugly.

[Elm](https://elm-lang.org/) makes so much more sense to me: the syntax, the structure, it's functional style, typed data, and so on. I'm stripping this back to the absolute essentials of Python, which is to say as little as possible to get the job done.


## Goals

1. Build a simple API
2. SQLite and Json
3. Minimal backend code
4. Minimal server setup

That's about it. I need something that interfaces with a simple database, keeping things light. It's for prototypes, and will probably be replaced by another programming language at some stage. [Roc](https://www.roc-lang.org/) looks promising, but I'm not a heavy coding guy, so might have a team by then!


## Coding style

> It doesn't feel as intuitive or consistent as Elm.

Perhaps you get shorter code at scale, but is it more readable? I'm not so sure.

- Length of a list?
    - `len([1, 2, 3])`
    - `List.length [1, 2, 3]`
- Access an element?
    - `[1, 2, 3][0]`
    - `List.elemIndex [1, 2, 3]`
- Reverse that?
    - `[1, 2, 3][-1]`
    - `List.elemIndex (List.reverse [1, 2, 3])`

It's also not at all type safe by default (and type annotations are awkward). Even the naming conventions feel messy (capitals and lowercase):

### Python

```python
from typing import List

# Requires `return` to print anything!
def ugly_types(num: List[int]) -> dict:
    { "numbers": num } 
```
```terminal
> ugly_types([1, 2, 3])
# returns nothing

```

### Elm 

```elm
type alias Numbers =
    { numbers :  List Int }

-- Returns data by default ...
niceTypes : List Int -> Numbers
niceTypes =
    Numbers
```
```terminal
> niceTypes [1, 2, 3]
```


## Questions

> Large Elm applications can become difficult to understand.

- At scale does Python become more readable?
- Perhaps Python is handy for certain applications?
- Perhaps a functional style is possible?
- Perhaps you just need to memorise syntax differences?


## Tools

- [UV in production?](https://pythonspeed.com/articles/uv-python-production/)
- [UV commands](https://docs.astral.sh/uv/reference/cli/) (a quick overview)
- [Thonny](https://thonny.org/) — a beginner IDE[^1]
- [VS Code](https://code.visualstudio.com/docs/python/python-tutorial) setup tutorial


## Handy snippets

| Command                                    | Does this                            |
| ------------------------------------------ | -------------------------------------|
| `pip install -r /path/to/requirements.txt` | Install requirements[^2]             |
| `uv init [folder-name]                     | Start `uv` project                   |
| `uv python install [version]`              | Install a Python version (or latest) |
| `uv python list`                           | List all Python versions installed   |
| `uv python pin`                            | Create a `.python-version` file      |
| `uv venv --python python3.11 [my_env]`     | Create/Download virtual environment  |
| `source my_env/bin/activate`               | Activate virtual environment         |
| `deactivate`                               | Deactivate (exit) venv               |
| `uv add [package]`                         | Download and install a package       |
| `uv tree`                                  | List all dependencies (as a tree)    |
| `uv run [command]`                         | Run the server, run a file, etc      |
| `uv sync`                                  | Sets up a project's "stuff"[^3]      |
| `uv run uvicorn src.main:app --reload`     | Run command for subfolder file[^4]   |


[^1]: You can't run this app while there's a virtual environment running in the terminal. You can set the virtual environment by going to `Tools -> Options ... -> Interpreter -> Python executable` and selecting the path or symlink in your `venv-folder-name`.

[^2]: If you're using stock Python commands, you'll probably need to preface with `python3 -m`, such as `python3 -m pip install [package]`. If you're using `uv` you don't need to worry about this (just use `uv run` etc). You also won't need to worry about `PATH` or any of that shit (I think `uv` does that for you).

[^3]: From scratch. Environment, dependencies, and so on. I think this needs a `pyproject.toml` file (and maybe a `.python-version` file). Lookup the docs for more info.

[^4]: It seems that the `uv` command **must** be run from the parent directory that the virtual server lives in. You also need to use the `module-folder.dot_format.py` to call a [subfolder's file](https://stackoverflow.com/a/62934660).
