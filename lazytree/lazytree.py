from collections import deque
from heapq import heappush, heappop

import attr
import funcy as fn


@attr.s(frozen=True)
class LazyTree:
    root = attr.ib()
    child_map = attr.ib()
    _view = attr.ib(default=lambda x: x)

    @property
    @fn.memoize
    def children(self):
        _children = self.child_map(self.root)
        return tuple(attr.evolve(self, root=c) for c in _children)

    def view(self):
        return self._view(self.root)

    def map(self, func):
        return attr.evolve(self, view=fn.compose(func, self._view))

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
