# Anki knowledge

There's quite a lot of minor (and perhaps major) errors in this book, so you've got to take care to double check the code's validity.

## Notes

1. For some examples, better to have a snippet ...
    - And link to the full file examples (e.g: `Msg` unpacking `Maybe` once)
    - This assures that the card viewing experience is pleasant, without too much awkward scrolling etc ... but may mean viewing on desktop instead.
2. If you already know something reasonably well (and have study notes) ...
    - It's OK to skip it and let the code speak for itself.
    - However, if you forget in future, a link to notes would be helpful.


## Terminology

> The difference between Elm type modules,
> and Python classes, methods, stateful stuff.
> **Errors and types are not as good and language design is worse**

You can rip a lot of this stuff from the book, but put it in very simple terms. Perhaps your Ai can help you do this, in the form of flashcards for simplicity?

- Basic Git terminology
- Declaration order (Python nested class requires a strict order)
- Returning values (unlike Elm you must `return value` or else `None`)
- **Lists and mutability** (the functions will change the `list` instance)
    - We NEVER have to worry about this in Elm Lang.
- **Python [named keyword arguments](https://treyhunner.com/2018/04/keyword-arguments-in-python/)**
- A class instance (such as `FastAPI()`)
    - FastApi implicitly builds the `ToDo(attributes="...")` class
    - Path(..., KWARGS) and [what the fuck is ellipses](https://tinyurl.com/pydantic-wtf-is-elipsis)?
- Basic syntax differences
    - `function()` calls and arguments
    - Typing (just a taste)
    - Python [comments](https://realpython.com/python-comments-guide/)
- The `app` variable (I guess this holds the state)
- Models (Elm has one master model)
    - See also Pydantics `BaseModel` class
    - Nested classes
- Decorators
- A route and route handler (with images)
    - what is a path, query params, urls
    - what is a request, request body, response body, response header
    - RESTful elements and actions
    - Code responses (does not exist) and ERROR handling etc
- Schemas and models (with validation)
    - Auth tokens and CSRF etc
    - Sanitize the user generated input data
    - Avoiding malicious code (such as sql/js injection)
- Errors
    - `raise` (short circuits the rest of the code, throws error)
- [Pydantic](https://medium.com/@marcnealer/a-practical-guide-to-using-pydantic-8aafa7feebf6)
    - Adding constraints (regex, Annotated, etc)
    - Are named arguments order dependant?
- **Structuring applications**
    - And best practices for comments, packages, etc
    - To an intermediate level.


## Setup

1. `requirements.txt`
2. `uv` basic commands

## Routing

> You can use an app like Bruno instead of Curl.
> Here's some [curl usage commands](https://gist.github.com/subfuzion/08c5d85437d5d4f00e58#curl-usage).
> Curl is a `GET` by default.

```terminal
> source .venv/bin/activate
> (venv)

-- Open a new terminal window
> (venv) curl http://localhost:8000
{"message":"Hello Buddy!"}
> (venv) curl http://localhost:8000/todo
{"todos":[]}
```

Adding an entry to the to-do list

```terminal
# Take care with your `' "` quotes!
curl -X POST \
"http://localhost:8000/todo" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{ "id": 1, "item": "First to-do is to finish this book!" }'

# Later chapter
-d '{ "id": 1, "item": { "item": "Water the plants", "status": "Done" } }'

# Check it worked
curl http://localhost:8000/todo
``` 
