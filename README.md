# Lazy Tree

[![Build Status](https://cloud.drone.io/api/badges/mvcisback/pyLazyTree/status.svg)](https://cloud.drone.io/mvcisback/pyLazyTree)
[![codecov](https://codecov.io/gh/mvcisback/DiscreteSignals/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/pyLazyTree)
[![PyPI version](https://badge.fury.io/py/lazytree.svg)](https://badge.fury.io/py/lazytree)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [View the current root.](#view-the-current-root)

<!-- markdown-toc end -->


# Installation

If you just need to use `lazytree`, you can just run:

`$ pip install lazytree`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

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
```

Conceptually a `LazyTree` object can be thought of as containing the pieces of data.

1. The `root` of the tree.
2. The data represented by the `root`, accessed via the `view` method.
3. The child subtrees - computed using `child_map` and accessed through the `.children` attribute.

For example, in our interval example, each node corresponds to an interval of `(0, 1)` and has two child subtrees.

```python
# View the current root.
assert tree.view() == tree.root

subtrees = tree.children
assert len(subtrees) == 2
```

Often, for each node in a tree, one is interested in computing a particular function. This can be done using the `map` and `view` methods. For example, below `map` each interval in the tree to it's size. This results in a new `LazyTree` object.

```python
tree2 = tree.map(lambda itvl: itvl[1] - itvl[0])  # Change view to itvl size.
assert tree2.view() == 1

# Access the root's subtrees
subtrees = tree2.children
assert len(subtrees) == 2
assert subtrees[0].root == (0, 0.5)
assert subtrees[0].view() == 0.5
```

Travesals of a `LazyTree` object are also implemented. For example,

```python
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

# Iterative Deepening Depth First Traversal
sizes = tree2.iddfs(max_depth=3)  # returns a generator.
assert list(sizes) == [1, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]

# Note, you can reset the current view.
tree3 = tree2.with_identity_view()
assert tree3.view() == tree.view()
```

Finally, one can "prune" away subtrees by labeling them as leaf nodes using the `prune` method. If you are sure that the resulting tree is finite (either due to pruning or the provided `child_map`) then one can compute the leaves of the tree.

```python
# Prune subtrees with a root of size less than 0.1.
tree4 = tree2.prune(isleaf=lambda s: s < 0.2)
sizes = tree.bfs()
assert all(s > 0.001 for s in sizes)  # Note that sizes is now finite.



# Compute leafs of tree. Careful! Could be infinite!
assert all(s == 0.125 for s in tree4.leaves())
assert len(list(tree4.leaves())) == 8
```
