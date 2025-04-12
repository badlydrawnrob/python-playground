from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# ------------------------------------------------------------------------------
# Our DATABASE settings
# ==============================================================================
# > 🔒 SECURITY: Never commit secrets to Github!!!
# > Passwords, Amazon S3 keys, secrets, etc shouldn't go in version control
#
# Pydantic's settings documentation is waaaay too confusing — the books example
# is outdated (dependency hell) and it's not as simple to achieve. There's other
# options, such as `python-decouple` which seems far simpler (although not as
# robust). More information here:
#
# @ https://docs.pydantic.dev/2.10/migration/#basesettings-has-moved-to-pydantic-settings
# @ https://docs.pydantic.dev/latest/concepts/pydantic_settings/#nested-model-default-partial-updates
#
# @ https://pypi.org/project/python-decouple/ (an alternative to Pydantic)
# @ https://youtu.be/0_seNFCtglk?t=1282 (tutorial to use `python-decouple`)
# @ https://tinyurl.com/a-note-on-env-security (not relying on `.env` files)
#
# Notes
# -----
# > Fucking programming is so annoying ..
#
# 1. For some reason, dictionaries aren't allowed in `.env` files ...
#    - So serialize  (convert) dictionary to a `json` string
#    - And decode with `json` where it's needed 
#    - Make sure negative numbers are valid in JSON

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DATABASE: Optional[str] = None
    PRAGMA_SETTINGS: Optional[str] = None #! `.env` files don't do dictionaries (1)
    SECRET_KEY: Optional[str] = None #! Our functions don't allow `None` (strict)
