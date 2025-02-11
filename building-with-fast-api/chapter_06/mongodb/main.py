# ------------------------------------------------------------------------------
# A PLANNER app (MongoDB)
# ==============================================================================
# > **TL;DR:**
# > I have limited time and limited capacity for learning new technologies, and
# > SQL is solid and reliable. My focus is on prototyping and I found the setup of
# > MongoDB to be unpleasant. I won't be using it in the near future, so will avoid
# > it's use for the rest of the book.
#
# ⚠️ You can safely avoid this chapter and further chapter code examples if you
# prefer to stick with SQLite or another SQL database. For my purposes, I'm keen
# to learn how to prototype apps to validate their business model, and therefore
# want to keep the learning experience light and easy(ish). My early experiences
# with MongoDB don't fill me with much confidence, especially getting it setup on
# a Mac, and I hold quite a bit of stock in a language (or frameworks) documentation
# marketing materials, and how it "feels" to interact with the website.
#
# - MongoDB seems to have a few different offerings and as such can feel a bit
#   overwhelming to look at. It's also said to be slower than SQLite for small sites.
# - SQLite is more old-school looking, but is widely used and everything feels
#   right at your finger tips. There are a lot of good books including "Teach
#   yourself SQL in 10 minutes" on SQL, it's boring (meaning well tested) and
#   seems to fit my purposes well enough.
#   
#   @ https://forta.com/books/0135182794/ (Teach Yourself SQL)
#
#
# Notes
# -----
# WARNING: Tightly coupling your SQL models with your API design may not be the 
# best way to go. Many say it's better to keep these two separate.
#
# Questions
# ---------
# 1. `await` keyword is used a lot. Is this needed for other ORMs?
# 2. `class Database` starts to use `BaseSettings` and methods
#    - How can this be done in a functional style (with SQLite or Postgres)
# 3. Motor is also required, but isn't mentioned as a `pip` install ...
#    - At this point I'm stopping the learning, as I don't see any real advantage
#      to coding a database in this fashion, and MongoDB was quite painful to get
#      setup. AVOID!
#    - @ https://tinyurl.com/mongodb-motor-required
