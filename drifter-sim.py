#!/usr/bin/python3
# Copyright © 2017 Po Huit
# This work is available under the "MIT License".
# Please see the file LICENSE in this distribution
# for license terms.

# Simulate a bunch of Drifter systems and determine connectivity.

from random import *

total_connections = 0

def sim():
    global total_connections
    # Place the holes.
    observatories = [set() for _ in range(1206)]
    for system in range(5):
        for _ in range(30):
            obs = randrange(len(observatories))
            observatories[obs].add(system)
    # Filter out noise for efficiency.
    connections = [s for s in observatories if len(s) >= 2]
    total_connections += len(connections)
    # Transitive closure
    closure = {0}
    running = True
    while running:
        running = False
        for c in connections:
            if c & closure and not (c <= closure):
                closure = closure | c
                running = True
    # Check connectivity.
    return closure == set(range(5))

n = 10000
c = 0
for _ in range(n):
    if sim():
        c += 1
print(c / n, total_connections / n)
