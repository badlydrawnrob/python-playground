# README

> Looking back on these examples ... I feel Python is ugly.

[Elm](https://elm-lang.org/) makes so much more sense to me: the syntax, the structure, it's functional style, typed data, and so on. I'm stripping this back to the absolute essentials of Python, which is to say as little as possible to get the job done.


## Goals

1. Build a simple API
2. SQLite and Json
3. Minimal backend code
4. Minimal server setup

That's about it. I need something that interfaces with a simple database, keeping things light. It's for prototypes, and will probably be replaced by another programming language at some stage. [Roc](https://www.roc-lang.org/) looks promising, but I'm not a heavy coding guy, so might have a team by then![^]


## On writing ...

> Some writing has:
> 1. Minor or major errors in the code[^2]
> 2. Outdated dependencies (how many does yours have?)
> 3. A high reading level (needlessly computer sciency)
> 4. Academic language (or verbose terminology)
> 5. Not enough visuals (or poorly labelled ones)
> 6. Not enough examples (or poorly framed ones)

In general I believe that beginners (and even intermediates) should stick to languages that are easy to setup, painless to learn, which instil good habits. I'm not sure Python is one of those languages!

Python suffered from [bad documentation](http://xahlee.info/python/python_doc.html) in years past. It's definitely improved: more accessible resources and writing styles than the early 2000s, but I _still_ have trouble following some function and package docs. APIs that are academic, verbose, or difficult to read; computer sciency writing when all you want to do is quickly scan an example to get shit done. I could say the same for API and language design (why so complicated?).

Learning Elm (and to some extent, Racket) has spoiled me. Installing and getting started is easy; learning materials increase in difficulty, gradually, as your experience grows (Racket's [teachpacks](https://download.racket-lang.org/docs/5.1/html/teachpack/index.html) are great); documentation and packages get standardised with helpful examples, rather than a wall of a API function parameters and types.

It baffles me why some programming languages are "clever" but impenetrable. The test of any great teacher is to explain things to a few levels: beginners grab the gist of the idea, while more advanced stuff is available, but hidden from view to avoid confusion. I aim to write and explain _as simply as possible_ with _just enough_ information for them to get the job done but I often get it wrong ...

- Writing about too many learning points in the same article
- Tangental information that deviates from the learning point
- Laundry lists of unfocused or poorly written comments
- A lot of questions going unanswered (which might not be needed anyway)
- Not letting the code do the talking, where comments are overkill

My [anki programming tool](https://github.com/badlydrawnrob/anki) is a good case in point. It's a time consuming process, but I often rewrite my flashcards (sometimes 3-4 times) so at-a-glance they make perfect sense, and stick better. That's an evolving process. There's something to be said for having a tight _learning frame_ — at the micro level (per card), and the macro level (cognitive strain) — anyone who's tried to learn two languages, or a bunch of "in process" books that never get finished could attest to that.

1. Have a learning frame of things I "will" and "wont" learn
2. Try to stick to a core-competency unless you're a good polygot
3. Understand the tradeoffs of learning something new (especially as you age!)

Aim for simple language and minimal terminology. Stick the 5 finger rule when picking packages. Support well-written, single-purpose, useful articles and tools, because it's not an easy thing to do and we should be promoting that more!


## Coding style

> It doesn't feel as intuitive or consistent as Elm.
> Python's main benefit is it's shorter learning curve.

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

It's also not at all type safe by default (and type annotations are awkward). Even the naming conventions feel messy (capitals and lowercase)! Here are some examples and comparisons for Python versus Elm Lang.

### Python

> [Declaration order](https://stackoverflow.com/a/758197) matters in Python! You might also want to [strongly type](https://talks.jackleow.com/strongly-typed) your code. It's also important to understand "[why functional programming](https://dev.to/cherryramatis/ending-the-war-or-continuing-it-lets-bring-functional-programming-to-oop-codebases-3mhd) over object-oriented?"?

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

### Other paradigm differences

> These can be avoided wherever necessary

1. `Class()`es and `Class.method()`s (rather than plain functions).
2. Stateful applications (rather than stateless and functional)
3. A `list` can be _mutable_, and changed _anywhere_ in the program. That's bad!
4. [`**Kwargs`](https://www.geeksforgeeks.org/args-kwargs-python/) and other Python magic.
5. The concept of [`self`](https://how.dev/answers/what-is-self-in-python) (a pretty dumb idea in my opinion)
6. Declaration order can be important (Pydantic nested class should come before it's use).


## The compiler
### The most important part of a language?

> **Elm has FAR superior types and error messaging**, which really save you when refactoring.
> Python by default, doesn't. Python's error messaging makes you crazy!

For example, with Python:

1. Typing is ugly and off by default.
2. Concepts like `None` and `Optional` require a different mindset to `Maybe`.
3. **A good REPL and helpful error messages are a god-send for refactoring.**
4. Python magic like `@decorators` and `extra='keyword arguments` don't exist in Haskell.

Take this piece of code, for example:

```python
simple_loop(l: list, id: int) -> bool:
    for item in l:
        if todo["id"] == id:
            return True
        else:
            return "False"
```
```terminal
> simple_loop([], 1)
> simple_loop([{"id": "string"}, 1])
'False'
```

There's a ton of problems with this:

1. `None` is implicitly returned, without an error
2. Different return types are allowed (this will break things)
3. `{"id": "string"}` should fail, but doesn't.
4. Dictionary could literally be `Any` type, with any combination of types.
5. In order to _enforce_ typing, more setup is involved.

### Elm to the rescue!

> All of these problems are fixed by default!

With Elm no need for any complicated setup, just:

1. [Install](https://guide.elm-lang.org/install/elm.html) Elm (simply)
2. `elm repl` to open the interactive repl
3. All you gotta do is code!

Here's what our code looks like now:

```elm
simpleFun l i =
    List.map (\list -> list.id == i) l

> simpleFun [] 1
[] : List Bool
```

An example Elm error message looks like this; it infers the types, spots that
`1 == "string"` is impossible, and suggests a fix:

```elm
simpleFun [{id = "string"}] 1
```
```terminal
-- TYPE MISMATCH ---------------------------------------------------------- REPL

The 2nd argument to `simpleFun` is not what I expect:

6|   simpleFun [{id = "string"}] 1
                                 ^
This argument is a number of type:

    number

But `simpleFun` needs the 2nd argument to be:

    String

Hint: I always figure out the argument types from left to right. If an argument
is acceptable, I assume it is “correct” and move on. So the problem may actually
be in one of the previous arguments!

Hint: Try using String.fromInt to convert it to a string?
```


## Questions

> Large Elm applications can become difficult to understand.

- At scale does Python become more readable?
- Perhaps Python is handy for certain applications?
- Perhaps a functional style is possible?
- Perhaps you just need to memorise syntax differences?


## Courses

- [Imperial College London](https://python.pages.doc.ic.ac.uk/2021/materials.html) course 
([example](https://python.pages.doc.ic.ac.uk/lessons/core05/07-style/03-docstring.html) chapter)


## Tools

- [UV in production?](https://pythonspeed.com/articles/uv-python-production/)
- [UV commands](https://docs.astral.sh/uv/reference/cli/) (a quick overview)
- [Thonny](https://thonny.org/) — a beginner IDE[^3]
- [VS Code](https://code.visualstudio.com/docs/python/python-tutorial) setup tutorial


## Handy snippets

| Command                                    | Does this                            |
| ------------------------------------------ | -------------------------------------|
| `activate`                                 | `source .venv/bin/activate` alias in `.zshrc` file |
| `pip freeze`                               | A list of currently installed packages |
| `pip install -r /path/to/requirements.txt` | Install requirements[^4]             |
| `uv init [folder-name]`                    | Start `uv` project                   |
| `uv python install [version]`              | Install a Python version (or latest) |
| `uv python list`                           | List all Python versions installed   |
| `uv python pin`                            | Create a `.python-version` file      |
| `uv venv --python python3.11 [my_env]`     | Create/Download virtual environment  |
| `source my_env/bin/activate`               | Activate virtual environment         |
| `deactivate`                               | Deactivate (exit) venv               |
| `uv add [package]`                         | Download and install a package       |
| `uv tree`                                  | List all dependencies (as a tree)    |
| `uv run [command]`                         | Run the server, run a file, etc      |
| `uv sync`                                  | Sets up a project's "stuff"[^5]      |
| `uv run uvicorn src.main:app --reload`     | Run command for subfolder file[^6]   |


[^1]: Personally, I'd prefer someone else to handle the heavy-lifting for some areas of the program. Ideally a stable and well-documented package, or have someone build it for me. Some areas of Python programs have a LOT of moving parts, and I'd prefer to stick to areas I'm good at (ui, ux, marketing, etc).

[^2]: This is likely to happen when you're making regular changes to the book. But you've really got to have a good editor (or using Ai) to triple check your changes for continuity errors. For the beginner, it's highly likely they'll get stuck, and there's nothing in the book to keep them right other than context and the student's initiative.

[^3]: You can't run this app while there's a virtual environment running in the terminal. You can set the virtual environment by going to `Tools -> Options ... -> Interpreter -> Python executable` and selecting the path or symlink in your `venv-folder-name`.

[^4]: If you're using stock Python commands, you'll probably need to preface with `python3 -m`, such as `python3 -m pip install [package]`. If you're using `uv` you don't need to worry about this (just use `uv run` etc). You also won't need to worry about `PATH` or any of that shit (I think `uv` does that for you).

[^5]: From scratch. Environment, dependencies, and so on. I think this needs a `pyproject.toml` file (and maybe a `.python-version` file). Lookup the docs for more info.

[^6]: It seems that the `uv` command **must** be run from the parent directory that the virtual server lives in. You also need to use the `module-folder.dot_format.py` to call a [subfolder's file](https://stackoverflow.com/a/62934660).
