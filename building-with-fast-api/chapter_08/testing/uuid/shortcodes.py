import shortuuid
import nanoid
import ksuid
import timeit

# ------------------------------------------------------------------------------
#  Test the speed of generating a unique id
# ==============================================================================
# > TLDR; Stop worrying about speed (performance can come later)
# > What's going to look best to your users? Is a timestamp useful?
#
# @ https://builtin.com/articles/timing-functions-python
# @ https://note.nkmk.me/en/python-timeit-measure/
#
# In general, for a single user, the speed really is negligable. There's not a
# huge amount of difference between them. It's miliseconds. So, use whatever
# is prettyist, shortest, whatever it is you're looking for!
#
#
# See commit `e21106494` for alternative method `perf_counter()`.
#
# `shortuuid` has 2k+ stars on Github, it's slower
# `nanoid` is older, with fewer stars, ↓ no typing (but seems stable)
# `fastnanoid` is a baby, and ↓ currently broken (see issues)
# `svix-ksuid` has few stars, timestamp (and sorting), ↓ extra dependency, longer
#
# I'm not sure how accurite the performance times are, for example:
# `perf_counter()` for a single instance gives this result
#
# 1. ksuid   -> 0.002015829999891139   (1 cycle)
# 2. nanoid  -> 2.7990000035060802e-05 (1 cycle)
# 3. shortid -> 8.074199968177709e-05  (1 cycle)
#
# When using `elapsed1 = finish1 - start1` and `print(f"time: {elapsed1:.6f} ")`.
# The times are (again) variable:
#
# 1. nanoid -> 0.000026
# 2. shortid -> 0.000074
# 3. ksuid -> 0.000465
#
# When using the `timeit` function (100 cycles, then divide by 100)
#
# 1. shortuuid -> 1.2332670003161184e-05 (reliably fast)
# 2. nanoid    -> 1.5287109999917447e-05 - 8.059499996306841e-06 (mostly high)
# 3. ksuid     -> 1.1465859997770167e-05 - 9.583279997968929e-06 (often high)
#
# NanoId is generally slower than Ksuid here.


loop = 100 # Number of times the function is run

# Return value is total time taken to run the test (not counting the setup)
# the average time per test is that number divided by the number argument,
# which defaults to 1 million! The unit value is a `Float` (for seconds)

# Eg: 3jtFC6LdSMxxdeuBaTrMnR
result = timeit.timeit(lambda: shortuuid.uuid(), number=loop)
print(shortuuid.uuid())
print(result / loop)
print("-------------------------")

# Eg: bhTKVVAAwRRmTI5HPbvNz (sometimes returns a `-` spacer)
result = timeit.timeit(lambda: nanoid.generate(), number=loop)
print(nanoid.generate())
print(result / loop)
print("-------------------------")

# Eg: 2vabSIZVJNHJnpJDMop2e0xCuMD (contains datetime/timestamp)
#     2025-04-11 15:45:22+00:00
#     1744386322.0                (why the decimal point?!)
#                                 @ https://github.com/svix/python-ksuid/issues/24
result = timeit.timeit(lambda: ksuid.Ksuid(), number=loop)
id = ksuid.Ksuid()
print(f'id: {id}, date: {id.datetime}, time: {id.timestamp}')
print(result / loop)
print("-------------------------")
base64 = ksuid.Ksuid.from_base62("2vadVZMYop8t5x49gwG5UfCjDcc")
print(f'You can convert from a string, too: {base64}')
print(f"Here's the date from that string: {base64.datetime}")
