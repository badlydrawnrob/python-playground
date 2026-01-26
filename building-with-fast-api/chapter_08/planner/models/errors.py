# ------------------------------------------------------------------------------
# Our ERROR model (API layer)
# ==============================================================================
# > See "APIs you won't hate 2" by Phil Sturgeon for more ideas.
#
# 1. Use standard HTTP error codes where possible.
# 2. Use reliable custom error codes for more detail.
#
# ⚠️ Security
# -----------
# Be vague with your error messages, especially destructive actions like `DELETE`.
# If you give away too much detail, it's canon fodder for attackers.
