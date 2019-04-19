#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Description:
    
"""

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        """首先返回本身的node值，然后执行到yield from， c的第一次迭代是node(1)，因为是使用的yield from，
        所以会返回内部自迭代的所有值，输出本身node(1)，然后yield from列表中的值，当这个迭代器执行完毕则返回第一次的node(0)，
        继续向下执行，执行方式同上"""
        """
            print(self._children)
            [Node(1), Node(2)]
            Node(0)
            [Node(3), Node(4)]
            Node(1)
            []
            Node(3)
            []
            Node(4)
            [Node(5)]
            Node(2)
            []
            Node(5)
        """
        yield self
        for c in self:
            yield from c.depth_first()


# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for n in root.depth_first():
        print(n)
