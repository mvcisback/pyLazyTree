[![Build Status](https://travis-ci.org/mvcisback/pyLazyTree.svg?branch=master)](https://travis-ci.org/mvcisback/pyLazyTree)
[![codecov](https://codecov.io/gh/mvcisback/DiscreteSignals/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/pyLazyTree)


[![PyPI version](https://badge.fury.io/py/lazytree.svg)](https://badge.fury.io/py/lazytree)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A `LazyTree` is a triple, `(root, child_map, view)` where `root : A`
and a child map, `child_map`, which maps `a` to a (finite) list of
children `child_map : A -> List[A]` define the tree's structure and
`view : A -> B` defines what the tree represents. The default view is
the identity map, `lambda x: x`.

Example: Binary tree representing the recursive subdivision of the
interval [0, 1].

```python
from lazytree import LazyTree

def split(itvl):
    lo, hi = itvl
    mid = lo + (hi - lo)/2
    return (lo, mid), (mid, hi)

tree = LazyTree(
    root=(0, 1),  # Initial Itvl
    child_map=split  # Itvl -> [Itvl]
)

tree.map(lambda itvl: sum(itvl) / 2)  # Change view to average itvl.

tree2 = LazyTree(
    root=(2, 3),  # Initial Itvl
    child_map=split  # Itvl -> [Itvl]
)
```
