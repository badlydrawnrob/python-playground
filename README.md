# README

> Looking back on these examples ... I feel Python is ugly.

[Elm](https://elm-lang.org/) makes so much more sense to me: the syntax, the structure, it's functional style, typed data, and so on. I'm stripping this back to the absolute essentials of Python, which is to say as little as possible to get the job done.


## Questions

- Perhaps Python is handy for certain applications?
- Perhaps a functional style is possible?
- Perhaps you just need to memorise syntax differences?


## Goals

1. Build a simple API
2. SQLite and Json
3. Minimal backend code
4. Minimal server setup

That's about it. I need something that interfaces with a simple database, keeping things light. It's for prototypes, and will probably be replaced by another programming language at some stage. [Roc](https://www.roc-lang.org/) looks promising, but I'm not a heavy coding guy, so might have a team by then!


## Tools

- [UV in production?](https://pythonspeed.com/articles/uv-python-production/)
- [Thonny](https://thonny.org/) — a beginner IDE[^1]
- [VS Code](https://code.visualstudio.com/docs/python/python-tutorial) setup tutorial


## Handy snippets

| Command                                    | Does this                           |
| ------------------------------------------ | ------------------------------------|
| `pip install -r /path/to/requirements.txt` | Install requirements[^2]            |
| `uv init [folder-name]                     | Start `uv` project                  |
| `uv venv --python python3.11 my_env`       | Create/Download virtual environment |
| `source my_env/bin/activate`               | Activate virtual environment        |
| `deactivate`                               | Deactivate (exit) venv              |
| `uv add [package]`                         | Download and install a package      |
| `uv tree`                                  | List all dependencies (as a tree)   |
| `uv run [command]`                         | Run the server, run a file, etc     |


[^1]: You can't run this app while there's a virtual environment running in the terminal. You can set the virtual environment by going to `Tools -> Options ... -> Interpreter -> Python executable` and selecting the path or symlink in your `venv-folder-name`.

[^2]: If you're using stock Python commands, you'll probably need to preface with `python3 -m`, such as `python3 -m pip install [package]`. If you're using `uv` you don't need to worry about this (just use `uv run` etc). You also won't need to worry about `PATH` or any of that shit (I think `uv` does that for you).

