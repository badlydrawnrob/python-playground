import shortuuid
import nanoid
import ksuid
import timeit

# ------------------------------------------------------------------------------
#  Test the speed of generating a unique id
# ==============================================================================
# @https://builtin.com/articles/timing-functions-python
#
# See commit `e21106494` for alternative method `perf_counter()`
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
# When using `elapsed1 = finish1 - start1` and `print(f"time: {elapsed1:.6f} ")`:
#
# 1. ...
# 2. ...
# 3. ...
#
# When using the `timeit` function (100 cycles, then divide by 100)
#
# 1. shortuuid -> 1.2332670003161184e-05 (reliably fast)
# 2. nanoid    -> 1.5287109999917447e-05 - 8.059499996306841e-06 (mostly high)
# 3. ksuid     -> 1.1465859997770167e-05 - 9.583279997968929e-06 (often high)
#
# NanoId is generally slower than Ksuid here.

loop = 100 # Timeit will run function this many times

result = timeit.timeit(lambda: shortuuid.uuid(), number=loop)
print(shortuuid.uuid())
print(result / loop)
print("-------------------------")

result = timeit.timeit(lambda: nanoid.generate(), number=loop)
print(nanoid.generate())
print(result / loop)
print("-------------------------")

result = timeit.timeit(lambda: ksuid.Ksuid(), number=loop)
id = ksuid.Ksuid()
print(f'id: {id}, date:{id.datetime}')
print(result / loop)
