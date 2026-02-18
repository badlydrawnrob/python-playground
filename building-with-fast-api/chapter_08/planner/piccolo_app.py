# ------------------------------------------------------------------------------
# Fruits app: settings
# ==============================================================================
# We import our table classes here and register with `APP_CONFIG`. Some functions
# (such as auto migrations) aren't supported with SQLite. Some functions (like
# auto migrations) aren't supported with SQLite.
# 
# Security
# --------
# > Your `.env` database settings should be secret!
# 
# 1. Never commit secrets to Github!
# 2. Store all passwords, keys, secrets, etc privately!
# 3. Consider tooling for `.env` settings (DevBox, etc)
# 
# Settings
# --------
# > We've changed to `python-decouple` as Pydantic settings documentation sucks,
# > and it feels harder to work with (we also don't worry about OS path now).
#
# Here are some options for `.env` settings management:
# 
# 1. Python decouple
#     - Seems to have the fewest dependencies!
#     - @ https://pypi.org/project/python-decouple/
#     - @ https://youtu.be/0_seNFCtglk?t=1282
# 2. Pydantic settings
#     - @ https://docs.pydantic.dev/2.10/migration/#basesettings-has-moved-to-pydantic-settings
#     - @ https://docs.pydantic.dev/latest/concepts/pydantic_settings/#nested-model-default-partial-updates
# 3. Environs
#     - @ https://pypi.org/project/environs/
# 4. Avoid relying on `.env` files
#     - @ https://tinyurl.com/a-note-on-env-security

from decouple import config
from planner.tables import Event
from piccolo.conf.apps import AppConfig


APP_CONFIG = AppConfig(
    app_name="planner",
    table_classes=[Event], #! Prefer explicit to `table_finder`
    migrations_folder_path=None, #! Optional. Type not currently supported
    migration_dependencies=[], # Optional
    commands=[] # Advanced use only
)

SECRET = config("SECRET_KEY")
