from collections import deque
from heapq import heappush, heappop
from random import shuffle

import attr
import funcy as fn


@attr.s(frozen=True)
class LazyTree:
    root = attr.ib()
    child_map = attr.ib()
    _view = attr.ib(default=lambda x: x)
    _isleaf = attr.ib(default=lambda _: False)  # For pruning subtrees.

    def isleaf(self):
        return self._isleaf(self.view())

    @property
    def children(self):
        if self.isleaf():
            return ()

        _children = self.child_map(self.root)
        return tuple(attr.evolve(self, root=c) for c in _children)

    def view(self):
        return self._view(self.root)

    def map(self, func):
        return attr.evolve(self, view=fn.compose(func, self._view))

    def prune(self, isleaf):
        """Return a new LazyTree where child nodes satisfying
        isleaf have their subtrees pruned."""
        return attr.evolve(self, isleaf=lambda x: self._isleaf(x) or isleaf(x))

    def with_identity_view(self):
        return attr.evolve(self, view=lambda x: x)

    # Traversals

    def bfs(self):
        queue = deque([self])
        while len(queue) > 0:
            curr = queue.pop()
            yield curr.view()
            queue.extendleft(curr.children)

    def cost_guided_traversal(self, cost_map):
        queue = [(-cost_map(self.view()), self)]
        while len(queue) > 0:
            _, curr = heappop(queue)
            yield curr.view()
            for c in curr.children:
                cost = -cost_map(c.view())
                heappush(queue, (cost, c))

    def leaves(self, *, max_depth=float('inf'), randomize=False):
        stack = [(self, 0)]
        while len(stack) > 0:
            curr, depth = stack.pop()
            if len(curr.children) == 0 or depth >= max_depth:
                yield curr.view()
            else:
                depth += 1
                succs = [(c, depth) for c in curr.children]
                if randomize:
                    shuffle(succs)
                stack.extend(succs)

    def iddfs(self, max_depth=float('inf'), flatten=True, randomize=False):
        """Iterative deepening depth-first search."""
        depth = 0
        while depth <= max_depth:
            nodes = self.leaves(max_depth=depth, randomize=randomize)
            if flatten:
                yield from nodes
            else:
                yield tuple(nodes)
            depth += 1
