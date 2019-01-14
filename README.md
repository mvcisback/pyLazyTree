[![Build Status](https://travis-ci.org/mvcisback/pyLazyTree.svg?branch=master)](https://travis-ci.org/mvcisback/pyLazyTree)
[![codecov](https://codecov.io/gh/mvcisback/DiscreteSignals/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/pyLazyTree)


[![PyPI version](https://badge.fury.io/py/lazytree.svg)](https://badge.fury.io/py/lazytree)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A `LazyTree` is a triple, `(root, child_map, view)` where `root : A`
and a child map, `child_map`, which maps `a` to a (finite) list of
children `child_map : A -> List[A]` define the tree's structure and
`view : A -> B` defines what the tree represents. The default view is
the identity map, `lambda x: x`.

This structure is useful for modeling infinite (or really large) trees
where only a finite number of nodes need to be accessed. For example,
the following Binary tree represents the recursive subdivision of the
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

# View the current root.
assert tree.view() == tree.root

tree2 = tree.map(lambda itvl: itvl[1] - itvl[0])  # Change view to itvl size.
assert tree2.view() == 1

# Access the root's subtrees
subtrees = tree2.children
assert len(subtrees) == 2
assert subtrees[0].root == (0, 0.5)
assert subtrees[0].view() == 0.5

# Breadth First Search through tree.
## Note: calls .view() before returning. 
itvls = tree.bfs()  # returns a generator.
sizes = tree2.bfs()  # returns a generator.

assert next(itvls) == (0, 1)
assert next(sizes) == 1

assert next(itvls) == (0, 0.5)
assert next(sizes) == 0.5

assert next(itvls) == (0.5, 1)
assert next(sizes) == 0.5

# Cost guided traversal.
## Note: Smaller means higher priority.
sizes = tree2.cost_guided_refinement(cost=lambda x: x)
assert next(sizes)  == 1  # (0, 1)
assert next(sizes)  == 0.5  # (0, 0.5)
assert next(sizes)  == 0.25  # (0, 0.25)

# Note, you can reset the current view.
tree3 = tree2.with_identity_view()
assert tree3.view() == tree.view()

# Prune subtrees with a root of size less than 0.1.
tree4 = tree2.prune(isleaf=lambda s: s < 0.2)
sizes = tree.bfs()
assert all(s > 0.001 for s in sizes)  # Note that sizes is now finite.

# Compute leafs of tree. Careful! Could be infinite!
assert all(s == 0.125 for s in tree4.leaves())
assert len(list(tree4.leaves())) == 8
```
