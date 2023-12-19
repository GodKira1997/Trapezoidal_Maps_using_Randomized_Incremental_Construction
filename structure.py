"""
file: structure.py
description: This program holds all the classes required for the trapezoidal
map.
language: python3
author: Anurag Kallurwar, ak6491@rit.edu
author: Neel Chaudhary, nc5834@rit.edu
"""


import math
import sys
from enum import Enum


class Point:
    """
    This class holds the point coordinates and required methods
    """
    __slots__ = "id", "x", "y", "visited"
    id: str
    x: float
    y: float
    visited: bool

    # Methods
    def __init__(self, x, y, id = 'P'):
        """
        Constructor
        :param x: x-coordinate
        :param y: y-coordinate
        :param id: name of Point
        """
        self.x = x
        self.y = y
        self.id = id
        self.visited = False

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id + "({:.3f}".format(self.x) + ",{:.3f})".format(
            self.y)


class Segment:
    """
    This class holds the line segment and required methods
    """
    __slots__ = "id", "start", "end", "A", "B", "C"
    id: str
    start: Point
    end: Point
    A: float
    B: float
    C: float

    # Methods
    def __init__(self, start: Point, end: Point, id = "S"):
        """
        Constructor
        :param start: left Point object
        :param end: right Point object
        :param id: Name of segnent
        """
        self.start = start
        self.end = end
        self.id = id
        # Ax + By + C = 0
        self.A = start.y - end.y
        self.B = end.x - start.x
        self.C = start.x * end.y - end.x * start.y

    def calculate_y(self, x):
        """
        Calculate y for x value on the segment
        :param x: x value
        :return:
        """
        return (-self.C - (self.A * x)) / self.B

    def is_above(self, point: Point):
        """
        Check if Point is above segment
        :param point: Point object
        :return: True or False
        """
        result_y = self.calculate_y(point.x)
        if point.y > result_y:
            return True
        return False

    def __repr__(self):
        return self.id + "[ " + repr(self.start) + " , " + repr(self.end) + " ]"

    def __str__(self):
        return self.id + "[ " + str(self.start) + " , " + str(self.end) + " ]"


class Trapezoid:
    """
    This class holds the trapezoid and required methods
    """
    __slots__ = "top", "bottom", "left", "right", "id"
    top: Segment
    bottom: Segment
    left: Point
    right: Point
    id: str

    # Methods
    def __init__(self, top: Segment, bottom: Segment, left = None, right =
    None):
        """
        Constructor
        :param top: Top Segment object
        :param bottom: Bottom Segment object
        :param left: Left Point
        :param right: Right Point
        """
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.id = 'T'

    def contains_point(self, point: Point):
        """
        Check if the point lies inside Trapezoid
        :param segment: Point object
        :return: True or False
        """
        if self.left.x <= point.x < self.right.x:
            return not self.top.is_above(point) and self.bottom.is_above(point)
        return False

    def contains_segment(self, segment: Segment):
        """
        Check if the segment lies inside Trapezoid fully or partially
        :param segment: Segment object
        :return: True or False
        """
        if self.contains_point(segment.start) or self.contains_point(
                segment.end):
            return True
        result_y = segment.calculate_y(self.left.x)
        if result_y is not None:
            intersection = Point(self.left.x, result_y, 'I')
            if self.contains_point(intersection):
                return True
        return False

    def __str__(self):
        return self.id + " {Top=" + str(self.top) + ", Bottom=" + str(
            self.bottom) + ", Left=" + str(self.left) + ", Right=" + str(
            self.right) + "}"

    def __repr__(self):
        return self.id + " {Top=" + repr(self.top) + ", Bottom=" + repr(
            self.bottom) + ", Left=" + repr(self.left) + ", Right=" + repr(
            self.right) + "}"


class Type(Enum):
    """
    This class holds the enumerated values for type of bound
    """
    POINT = -1
    SEGMENT = 0
    TRAPEZOID = 1
    NONE = math.inf


class TreeNode():
    """
    This class is the node of the Tree representing the Trapezoidal Map
    """
    __slots__ = "id", "value", "leftChild", "rightChild", "parents"

    # Methods
    def __init__(self, value, leftChild = None, rightChild = None):
        """
        Constructor
        :param value: object of Point / Segment / Trapezoid
        :param leftChild: left child node
        :param rightChild: right child node
        """
        self.value = value
        self.parents = []
        if isinstance(self.value, Point):
            self.value.visited = True
        self.set_left_child(leftChild)
        self.set_right_child(rightChild)

    def get_type(self):
        """
        gets the type of value in node
        :return: Enum Type
        """
        if isinstance(self.value, Point):
            return Type.POINT
        if isinstance(self.value, Segment):
            return Type.SEGMENT
        if isinstance(self.value, Trapezoid):
            return Type.TRAPEZOID
        return Type.NONE

    def is_leaf(self):
        """
        Check if the node is leaf node or trapezoidal node
        :return: True or False
        """
        if self.get_type() == Type.TRAPEZOID:
            return True
        return False

    def set_left_child(self, node = None):
        """
        Set the left child
        :param node: child node
        :return: None
        """
        self.leftChild = node
        if node is None:
            return
        if self not in node.parents:
            node.parents.append(self)

    def set_right_child(self, node = None):
        """
        Set the right child
        :param node: child node
        :return: None
        """
        self.rightChild = node
        if node is None:
            return
        if self not in node.parents:
            node.parents.append(self)

    def update_node(self, node):
        """
        Update current TreeNode with new node
        :param node: Tree node
        :return: True or False
        """
        if not self.parents:
            return False
        for parent in self.parents:
            if parent.leftChild == self:
                parent.set_left_child(node)
            else:
                parent.set_right_child(node)
        return True

    def __str__(self):
        return "NODE: " + str(self.value)

    def __repr__(self):
        return "NODE: " + str(self.value) + " | LEFT:[ " + repr(self.leftChild)\
               + " ] | RIGHT:[ " + repr(self.rightChild) + " ]"
