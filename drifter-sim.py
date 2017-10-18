#!/usr/bin/python3
# Copyright © 2017 Po Huit
# This work is available under the "MIT License".
# Please see the file LICENSE in this distribution
# for license terms.

# Simulate a bunch of Drifter systems and determine connectivity.

from random import *

def sim():
    # Place the holes.
    observatories = [set() for _ in range(1206)]
    for system in range(5):
        for _ in range(30):
            obs = randrange(len(observatories))
            observatories[obs].add(system)
    # Filter out noise for efficiency.
    connections = [s for s in observatories if len(s) >= 2]
    # Goofy version of Warshall's Algorithm.
    cspan = set()
    for src in range(5):
        for dst in range(src + 1, 5):
            for c in connections:
                if src in c and dst in c:
                    for csrc, cdst in set(cspan):
                        if cdst == src:
                            cspan.add((csrc, dst))
                    cspan.add((src, dst))
    # Check connectivity.
    for system in range(4):
        if (system, system+1) not in cspan:
            return False
    return True

n = 10000
c = 0
for _ in range(n):
    if sim():
        c += 1
print(c / n)
