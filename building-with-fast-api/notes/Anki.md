# Anki knowledge

## Terminology

> The difference between Elm type modules,
> and Python classes, methods, stateful stuff.

You can rip a lot of this stuff from the book, but put it in very simple terms. Perhaps your Ai can help you do this, in the form of flashcards for simplicity?

- Basic Git terminology
- A class instance (such as `FastAPI()`)
- Basic syntax differences
    - `function()` calls and arguments
    - Typing (just a taste)
    - Python [comments](https://realpython.com/python-comments-guide/)
- The `app` variable (I guess this holds the state)
- Models (Elm has one master model)
- Decorators
- A route and route handler (with images)
    - what is a path, query params, urls
    - what is a request, request body, response body
    - RESTful elements and actions
    - Code responses (does not exist) etc


## Chapter 02: Routing

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
-- Take care with your `' "` quotes!
curl -X POST \
"http://localhost:8000/todo" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{ "id": 1, "item": "First to-do is to finish this book!" }'

-- Check it worked
curl http://localhost:8000/todo
``` 
