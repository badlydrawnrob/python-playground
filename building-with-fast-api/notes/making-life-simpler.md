# Making life simpler

> TLDR; Backend is fucking hard

And there's a lot that can go wrong. It doesn't feel as safe and solid as Elm frontend code. I've sunk enough time into FastApi now though to just stick with it and find a compatible ORM.

## Just-in-time, just-enough

It's better to foreplan just-enough, as we'll likely have to move to Postgres at some later point. Otherwise we'd use SQLite for all the things (without async)

## Pick a better language

I think I should eventually migrate to OCaml, Elixir, Roc, etc. Or use a easy query builder like PyPika.

## Don't use `async`?

> SQLite isn't setup for `async` by default either.

- Without a plugin, only ONE write operation at a time.

In fact, PeeWee is probably perfect for Sqlite if one single user Postgres is much better setup for this.

