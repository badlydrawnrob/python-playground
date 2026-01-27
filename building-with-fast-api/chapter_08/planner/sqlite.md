# SQL for the `planner.db`

> Use `sqlite-utils` to automatically populate the database with initial data.


## Export from original database:

1. `sqlite-utils planner.sqlite "select * from events" --arrays --nl` for events
2. `sqlite-utils planner.sqlite "select * from piccolo_user" --arrays --nl` for users


## Insert into new database:

1. Convert list into `INSERT` statements manually ...
2. Or `sqlite-utils insert` from `json/csv` file.
3. Run `piccolo migrations forwards user` to create the user table.
4. Run `piccolo user create` to create any users.

### Order of insertion

Piccolo will insert rows in the order of the class fields, not alphabetically.
So make sure your CSV columns are in the same order as your Piccolo table fields.

### CSV list of events

> sqlite-utils insert [DATABASE_NAME] [TABLE_NAME] [CSV_PATH] --csv

```csv
"id", "creator", "title", "image","description","location","tags"
"0a466c53-14a7-4a57-9a67-cf3122ed8c3b", 1, "Glastonbury", "https://somegood.com/song.jpg", "Ed Sheeran singing his best song 'Class A Team'!", "Live", '["music", "adults", "event"]'
"f5922d35-bec4-40f1-8d57-28cf4b6772a4", 1, "Comic Con", "https://somegood.com/comic.jpg", "A fun event for all things comics!", "Convention Center", '["comics", "sci-fi", "fantasy"]'
"7b5e11f5-47f7-4dd3-a8ae-da81fc84ebe2", 1, "Farmers Market", "https://somegood.com/market.jpg", "Fresh fruits and vegetables", "Town Square", '["food", "local", "outdoors"]'
```

### SQL list of events

> `sqlite3 planner.db`

`Event` is a reserved [keyword](https://www.sqlite.org/lang_keywords.html) in some SQL databases, so it must be quoted (SQLite doesn't use it).

```sql
INSERT INTO "event" VALUES
    ("f5922d35-bec4-40f1-8d57-28cf4b6772a4", 1, "Comic Con", "https://somegood.com/comic.jpg", "A fun event for all things comics!", "Convention Center", '["comics", "sci-fi", "fantasy"]'),
    ("7b5e11f5-47f7-4dd3-a8ae-da81fc84ebe2", 1, "Farmers Market", "https://somegood.com/market.jpg", "Fresh fruits and vegetables", "Town Square", '["food", "local", "outdoors"]'),
    ("c1f3e8b4-5f4e-4d2a-9f3e-2b6c8e4d5f6a", 1, "Tech Conference", "https://somegood.com/tech.jpg", "Latest trends in technology and innovation", "Y Combinator", '["technology", "innovation", "networking"]');
```
