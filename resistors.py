#!/usr/bin/env python3

import pprint
import argparse
from itertools import permutations, combinations
from itertools import combinations_with_replacement as combinations_r

parser = argparse.ArgumentParser(description='Given a set of resistors, find the combination closest to the desired value')
parser.add_argument('-d', '--desired',
                    type=int,
                    help='desired value in ohms')
parser.add_argument('-r', '--resistors',
                    type=int,
                    nargs='+',
                    required=True,
                    help='given set of resistors')
args = parser.parse_args()

class Resistor:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return '{0:0.0f}'.format(self.value)

  def __repr__(self):
    return str(self)

  def __add__(self, other):
    # series
    return Resistor(self.value + other.value)

  def __mul__(self, other):
    # parralel
    return Resistor((self.value * other.value)
                    / (self.value + other.value))

  def __eq__(self, other):
    return self.value == other.value

  def __lt__(self, other):
    return self.value < other.value

  def __hash__(self, other):
    return self.value.__hash__()


def multireduce(operators, sequence):
  accumulator = sequence[0]
  path = '{}'.format(accumulator)

  if len(sequence) == 1:
    return accumulator, path

  for op, el in zip(operators, sequence[1:]):
    if op == '|':
      accumulator *= el
    elif op == '+':
      accumulator += el

    path += ' {} {}'.format(op, el)
  path += ' = {}'.format(accumulator)

  return accumulator, path

def find_closest(desired, paths):
  closest = paths[0]
  
  for path in paths:
    if abs(desired - path[0].value) < abs(desired - closest[0].value):
      closest = path

  return closest

resistors = [Resistor(x) for x in args.resistors]

opcombs = []
for i in range(1, len(resistors) + 1):
  combs = []
  for c in combinations_r(['+', '|'], i):
    combs += list(set(permutations(c)))
  opcombs.append(combs)

paths = []
for i in range(1, len(resistors) + 1):
  for c in combinations(resistors, i):
    if len(c) > 1:
      for opcomb in opcombs[i - 2]:
        paths.append(multireduce(opcomb, c))

if args.desired:
  print('Closest to {}: {}'.format(args.desired,
                                   find_closest(args.desired, paths)))
else:
  pprint.pprint(sorted(paths))
