#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NodeTree class
@author: TOUMI Anouar
"""


class NodeTree(object):
    def __init__(self, left=None, right=None):
        """ class constructor """
        # init children node left and right
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return '%s_%s' % (self.left, self.right)
