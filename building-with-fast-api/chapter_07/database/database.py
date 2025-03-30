from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# ------------------------------------------------------------------------------
# Our DATABASE settings
# ==============================================================================
# Pydantic's settings documentation is waaaay too confusing — the books example
# is outdated (dependeny hell) and it's not as simple to achieve. You might want
# to use an alternative, such as `python-decouple` which seems far simpler
# (although not as robust). You can find more information here:
#
# @ https://docs.pydantic.dev/2.10/migration/#basesettings-has-moved-to-pydantic-settings
# @ https://docs.pydantic.dev/latest/concepts/pydantic_settings/#nested-model-default-partial-updates
#
# @ https://pypi.org/project/python-decouple/ (an alternative to Pydantic)
# @ https://youtu.be/0_seNFCtglk?t=1282 (tutorial to use `python-decouple`)
# @ https://tinyurl.com/a-note-on-env-security (not relying on `.env` files)
#
# 🔒 SECURITY
# -----------
# > Never commit secrets to Github!!!
#
# Database passwords, Amazon S3 keys, secrets, and so on should be hidden from
# your version control. These are things that you don't want to be publically
# available in any form.

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    SECRET_KEY: Optional[str] = None #! Our functions don't allow `None` (strict)
