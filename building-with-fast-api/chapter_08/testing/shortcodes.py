import shortuuid
import nanoid
import ksuid
import time

# ------------------------------------------------------------------------------
#  Test the speed of generating a unique id
# ==============================================================================
# @https://builtin.com/articles/timing-functions-python
#
# `shortuuid` has 2k+ stars on Github, it's slower
# `nanoid` is older, with fewer stars, ↓ no typing (but seems stable)
# `fastnanoid` is a baby, and ↓ currently broken (see issues)
# `svix-ksuid` has few stars, timestamp (and sorting), ↓ extra dependency, longer
#
# Runtime is variable but speed in order of fastest:
# 1. Ksuid() — < 1 

# Runs in 
start1 = time.perf_counter()
shortid = shortuuid.uuid()
print(shortid)
finish1 = time.perf_counter()
elapsed1 = finish1 - start1
print(f"time: {elapsed1:.6f} ")
# print("-------------------------")

start2 = time.perf_counter()
nano = nanoid.generate()
print(nano)
finish2 = time.perf_counter()
elapsed2 = finish2 - start2
print(f"time: {elapsed2:.6f} ")
# print("-------------------------")

start3 = time.perf_counter()
kid = ksuid.Ksuid()
print(kid) # base62
print(kid.datetime)
finish3 = time.perf_counter()
elapsed3 = finish3 - start3
print(f"time: {elapsed3:.6f} ")
# print("-------------------------")
