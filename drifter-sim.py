#!/usr/bin/python3
# Copyright © 2017 Po Huit
# This work is available under the "MIT License".
# Please see the file LICENSE in this distribution
# for license terms.

# Simulate a bunch of Drifter systems and determine connectivity.

# Number of wormholes per system.
holes_per_system = 27

# Number of simulations to run.
simulation_count = 10000

from random import *

total_connections = 0

def sim():
    global total_connections
    # Place the holes.
    observatories = [set() for _ in range(1206)]
    for system in range(5):
        for _ in range(holes_per_system):
            obs = randrange(len(observatories))
            observatories[obs].add(system)
    # Filter out noise for efficiency.
    connections = [s for s in observatories if len(s) >= 2]
    total_connections += len(connections)
    # Compute transitive closure for given starting system.
    def connected(i):
        closure = {i}
        running = True
        while running:
            running = False
            for c in connections:
                if c & closure and not (c <= closure):
                    closure = closure | c
                    running = True
        return closure
    # Build connectivity counts.
    unconnected = set(range(5))
    sizes = []
    while unconnected:
        target = min(unconnected)
        clique = connected(target)
        sizes.append(len(clique))
        unconnected -= clique
    return tuple(sorted(sizes, reverse=True))

configs = dict()
for _ in range(simulation_count):
    sizes = sim()
    if sizes in configs:
        configs[sizes] += 1
    else:
        configs[sizes] = 1

print(total_connections / simulation_count, "avg connections per sim")
print()
for c in sorted(configs.keys(), reverse=True):
    desc = '/'.join([str(i) for i in c])
    prob = configs[c] / simulation_count
    print(desc, "%d%%" % (round(100.0 * prob,)))
